from fastapi.templating import Jinja2Templates
from contextvars import ContextVar
from fastapi import Request

current_request: ContextVar[Request] = ContextVar("request")

templates = Jinja2Templates(directory="webapp/web/templates")