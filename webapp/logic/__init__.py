from fastapi.templating import Jinja2Templates
from .validate import validateOpenClass
from .sessionManager import get_open_form, get_form, remove_from, get_main_menu, get_session
from .putEvent import get_session_queue, registrSignal

templates = Jinja2Templates(directory="webapp/web/templates")

__all__ = [
    "validateOpenClass"
    , "get_open_form"    
    , "get_form"    
    , "remove_from"  
    , "get_main_menu"  
    , "get_session"

    , "get_session_queue"
    , "registrSignal"

    , "templates"    
]