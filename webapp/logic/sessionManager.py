from webapp.logic.validate import validateOpenClass

from core.sdk import current_session_id

from webapp.logic.dataClass import Session

user_sessions: dict[str, Session] = {}

def get_open_form()->list[dict]:
    forms_data = user_sessions.get(get_session_id(), {})
    return [{'caption': f_object.getInfoMeta()['metaForm']['caption'],
             'nameClass': f_name[:f_name.find('/')], 
             'nameForm': f_name[f_name.find('/')+1:], 
             'name': f_name} \
             for f_name, f_object in forms_data.open_form.items()]

def get_form(form_name:str):
    session = get_session()    
    isMainMenu = len(x:=form_name.split('/')) > 1
    if isMainMenu:
        if not any(f == form_name for f in session.open_form.keys()):
            sNameTab, sForm = x
            session.open_form[form_name] = validateOpenClass(sNameTab=sNameTab, sForm=sForm, session_id=get_session())

        return session.open_form[form_name]

    return session.main_menu_form

def remove_from(form_name:str)->str:
    keys = list(get_session().open_form.keys())
    idx = keys.index(form_name)

    get_session().open_form.pop(form_name)

    if len(get_session().open_form) <= idx:
        idx -= 1

    return list(get_session().open_form.keys())[idx] if idx >= 0 else ""

def get_main_menu(sNameMainMenu: str):
    session = get_session()
    if session.main_menu_form is None:
        session.main_menu_form = validateOpenClass(sNameMainMenu, get_session_id())

    return session.main_menu_form

def get_session()->Session:
    session_id = get_session_id()
    if session_id not in user_sessions:
        user_sessions[session_id] = Session(id=session_id, open_form={})

    return user_sessions[session_id]

def get_session_id():
    return current_session_id.get()
