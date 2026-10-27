import time
import uuid

from webapp.logic.validate import validateOpenClass

from core.sdk import current_session_id

from webapp.logic.dataClass import Session, Tab

user_sessions: dict[str, Session] = {}

SESSION_TTL_SEC = 60 * 60          # мёртвые сессии вычищаются через час покоя
MAX_SESSIONS = 1000                # жёсткий потолок, защита от утечки памяти


def _evict_dead_sessions():
    """Удаляет сессии, к которым долго не обращались (утечка memory fix)."""
    now = time.time()
    dead = [sid for sid, s in user_sessions.items() if now - s.last_seen > SESSION_TTL_SEC]
    for sid in dead:
        user_sessions.pop(sid, None)
    if len(user_sessions) > MAX_SESSIONS:
        oldest = sorted(user_sessions.values(), key=lambda s: s.last_seen)
        for s in oldest[:len(user_sessions) - MAX_SESSIONS]:
            user_sessions.pop(s.id, None)


def get_open_form()->list[dict]:
    return [{'caption': f_object.getInfoMeta()['metaForm']['caption'],
             'nameClass': f_name[:f_name.find('/')], 
             'nameForm': f_name[f_name.find('/')+1:], 
             'name': f_name} \
             for f_name, f_object in get_session().open_form.items()]

def get_form(form_name:str, default=None):
    session = get_session()    
    isMainMenu = len(x:=form_name.split('/')) > 1
    if isMainMenu:
        if not any(f == form_name for f in session.open_form.keys()):
            if default:
                default.object.refresh()
                session.open_form[form_name] = default
            else:
                sNameTab, sForm = x
                session.open_form[form_name] = validateOpenClass(sNameTab=sNameTab, sForm=sForm, session_id=session)

        return session.open_form[form_name]

    return session.main_menu_form

def remove_from(form_name:str)->str:
    session = get_session()
    keys = list(session.open_form.keys())

    if form_name not in keys:          # уже закрыта — не падаем, тихо выходим
        return session.active_form or ""

    idx = keys.index(form_name)
    session.open_form.pop(form_name)

    if len(session.open_form) <= idx:
        idx -= 1

    nxt = list(session.open_form.keys())[idx] if idx >= 0 else ""
    session.active_form = nxt          # синхронизируем активную форму с фактом закрытия
    return nxt


# ---------- Табы (абстракция «окно») ----------

def create_tab(form_name: str = "", parent_tab_id: str | None = None) -> Tab:
    """Открывает новое окно (таб). form_name='' — таб только с главным меню."""
    session = get_session()
    tab = Tab(tab_id=uuid.uuid4().hex[:8], form_name=form_name, parent_tab_id=parent_tab_id)
    session.tabs[tab.tab_id] = tab
    if parent_tab_id and (parent := session.tabs.get(parent_tab_id)):
        parent.child_tab_ids.append(tab.tab_id)
    session.active_tab_id = tab.tab_id
    return tab


def get_active_tab() -> Tab | None:
    session = get_session()
    return session.tabs.get(session.active_tab_id) if session.active_tab_id else None


def close_tab(tab_id: str) -> str | None:
    """Закрывает таб вместе со всеми дочерними; возвращает id следующего активного таба."""
    session = get_session()
    tab = session.tabs.pop(tab_id, None)
    if not tab:
        return None

    for child_id in list(tab.child_tab_ids):
        close_tab(child_id)

    if parent := session.tabs.get(tab.parent_tab_id):
        if tab_id in parent.child_tab_ids:
            parent.child_tab_ids.remove(tab_id)

    if session.active_tab_id == tab_id:
        session.active_tab_id = tab.parent_tab_id or next(iter(session.tabs), None)
    return session.active_tab_id


def get_main_menu(sNameMainMenu: str):
    session = get_session()
    if session.main_menu_form is None:
        session.main_menu_form = validateOpenClass(sNameMainMenu, get_session_id())

    return session.main_menu_form

def get_session()->Session:
    session_id = get_session_id()
    if session_id not in user_sessions:
        _evict_dead_sessions()
        user_sessions[session_id] = Session(id=session_id, open_form={})

    session = user_sessions[session_id]
    session.last_seen = time.time()
    return session

def get_session_id():
    return current_session_id.get()
