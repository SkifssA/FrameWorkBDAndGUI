from webapp.logic.validate import validateOpenClass

from webapp.logic.dataClass import Session

user_sessions: dict[str, Session] = {}

def get_open_form(session_id: str)->list[dict]:
    forms_data = user_sessions.get(session_id, {})
    return [{'caption': f_object.getInfoMeta()['metaForm']['caption'],
             'nameClass': f_name[:f_name.find('/')], 
             'nameForm': f_name[f_name.find('/')+1:], 
             'name': f_name} \
             for f_name, f_object in forms_data.open_form]

def get_form(session_id: str, form_name:str):
    session = get_session(session_id)

    if not any(f == form_name for f in session.keys()):
        sNameTab, sForm = form_name.split('/')
        session.open_form[form_name] = validateOpenClass(sNameTab=sNameTab, sForm=sForm, session_id=session_id)

    return session.open_form[form_name]

def remove_from(session_id:str, form_name:str):
    if session_id in user_sessions:
        user_sessions[session_id].open_form = {f_name:f_data for f_name, f_data in user_sessions[session_id].open_form if f_name != form_name}

def get_main_menu(session_id: str, sNameMainMenu: str):
    session = get_session(session_id)

    if session.main_menu_form is None:
        session.main_menu_form = validateOpenClass(sNameMainMenu, session_id)

    return session.main_menu_form

def get_session(session_id: str)->Session:
    if session_id not in user_sessions:
        user_sessions[session_id] = Session(id=session_id, open_form={})

    return user_sessions[session_id]
