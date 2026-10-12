import sys
from pathlib import Path

import pytest

# Добавляем корень проекта в sys.path, чтобы работали импорты `core.*` и `module.*`
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture()
def monkeypatch_sql(monkeypatch):
    """Перехватывает ASQL/ATSQL (реальная БД в тестах не нужна).

    ВАЖНО: core.DB.SQLLogic импортирует функции по именам (`from core.DB.Turso
    import ASQL, ATSQL`), поэтому патчим именно пространство имён SQLLogic.
    Возвращает список перехваченных вызовов.
    """
    calls = []

    def fake_asql(sql, parameters=None):
        calls.append({"sql": sql, "parameters": parameters})
        return {"columns": [], "data": []}

    def fake_atsql(sql, parameters=None):
        calls.append({"sql": sql, "parameters": parameters})
        return 1

    monkeypatch.setattr("core.DB.SQLLogic.ASQL", fake_asql)
    monkeypatch.setattr("core.DB.SQLLogic.ATSQL", fake_atsql)
    return calls
