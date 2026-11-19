from fastapi.templating import Jinja2Templates
from contextvars import ContextVar
from fastapi import Request
from webapp.logic.setup_jinja import sutup_jinja

current_request: ContextVar[Request] = ContextVar("request")

templates = Jinja2Templates(directory="webapp/web/templates")
sutup_jinja(templates)