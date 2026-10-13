from contextvars import ContextVar

current_session_id: ContextVar[str] = ContextVar("session_id", default="anonymous")