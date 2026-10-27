"""Тесты новой модели сессий: изоляция, табы (окна), eviction, remove_from."""
import time

import pytest

from core.context import current_session_id
from webapp.logic.dataClass import Session, Tab
import webapp.logic.sessionManager as sm


@pytest.fixture(autouse=True)
def clean_sessions():
    sm.user_sessions.clear()
    yield
    sm.user_sessions.clear()


@pytest.fixture
def session_a():
    current_session_id.set("user-A")
    return sm.get_session()


def test_middleware_issues_unique_session_cookie():
    """Первый запрос без куки должен получить Set-Cookie с уникальным session_id."""
    from starlette.testclient import TestClient
    from fastapi import FastAPI

    probe = FastAPI()

    @probe.get("/probe")
    def _p():
        return {"sid": current_session_id.get()}

    # импортируем middleware-функцию из приложения проекта и навешиваем на probe
    import webapp.main as wm
    probe.middleware("http")(wm.session_context_middleware.__wrapped__
                             if hasattr(wm.session_context_middleware, "__wrapped__")
                             else wm.session_context_middleware)

    client = TestClient(probe)
    r1 = client.get("/probe")
    assert r1.status_code == 200
    sid1 = r1.json()["sid"]
    assert sid1 != "default" and len(sid1) == 32
    assert "session_id" in r1.cookies

    # повторный запрос с кукой сохраняет идентификатор
    r2 = client.get("/probe", cookies={"session_id": sid1})
    assert r2.json()["sid"] == sid1


def test_sessions_are_isolated(session_a):
    current_session_id.set("user-B")
    session_b = sm.get_session()
    assert session_a is not session_b
    assert set(sm.user_sessions) == {"user-A", "user-B"}


def test_tab_create_close_and_cascade(session_a):
    t1 = sm.create_tab("Anime/List")
    t2 = sm.create_tab("Anime/Card", parent_tab_id=t1.tab_id)

    assert session_a.active_tab_id == t2.tab_id
    assert t1.child_tab_ids == [t2.tab_id]

    # закрытие дочернего возвращает фокус родителю
    assert sm.close_tab(t2.tab_id) == t1.tab_id
    assert session_a.active_tab_id == t1.tab_id

    # закрытие родителя каскадно убивает дочерние
    t3 = sm.create_tab("X/Y", parent_tab_id=t1.tab_id)
    sm.close_tab(t1.tab_id)
    assert t1.tab_id not in session_a.tabs
    assert t3.tab_id not in session_a.tabs


def test_close_unknown_tab_is_noop(session_a):
    assert sm.close_tab("nope") is None


def test_remove_from_closed_form_does_not_raise(session_a):
    session_a.open_form["A/B"] = object()
    assert sm.remove_from("A/B") == ""
    # повторное закрытие уже закрытой формы не бросает ValueError
    assert sm.remove_from("A/B") == ""


def test_eviction_of_dead_sessions(session_a):
    current_session_id.set("user-B")
    sm.get_session()
    session_a.last_seen = time.time() - sm.SESSION_TTL_SEC - 1  # «протухла»
    sm._evict_dead_sessions()
    assert "user-A" not in sm.user_sessions
    assert "user-B" in sm.user_sessions


def test_get_session_touches_last_seen(session_a):
    session_a.last_seen = 0
    sm.get_session()
    assert session_a.last_seen > time.time() - 5
