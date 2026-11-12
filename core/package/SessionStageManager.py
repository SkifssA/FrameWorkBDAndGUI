from core.dataClass.session import Session
from core.context import current_session_id
from core.package.ModuleManagerPkg import ACTIONDISPATCHER
from core.dataClass.formRef import FormRef
from core.emptySubClass.base import Base

def validateOpenClass(sNameTab:str, sForm:str = 'Default')->Base:
    class_ = ACTIONDISPATCHER.getClassByName(f"{sNameTab}")
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            return form
        raise AttributeError(f"Отображение {sForm} класса {sNameTab} не найдено")
    raise AttributeError(f"Класс {sNameTab} не найден")

class SessionStageManager:
    def __init__(self):
        self._module:list[str] = []
        self._class:dict[str, type] = {}
        self.session_cach:dict[str, Session] = {}

    def _get_session(self)->Session:
        """Получить текущую сессию"""
        id_session = current_session_id.get()
        if id_session not in self.session_cach:
            self.session_cach[id_session] = Session(id=id_session)

        return self.session_cach[id_session]

    def get_obj(self, nameForm):
        return self._get_session()._load_obj.get_group(nameForm)

    def get_all_obj(self):
        return self._get_session()._load_obj.all_items

    def set_list_obj(self, name, lObj):
        current = self._get_session()._load_obj.get_group(name)
    
        # Добавляем только уникальные объекты (по id или другому ключу)
        existing_ids = {obj.id for obj in current if hasattr(obj, 'id')}
        
        for obj in lObj:
            if not hasattr(obj, 'id') or obj.id not in existing_ids:
                current.append(obj)
                if hasattr(obj, 'id'):
                    existing_ids.add(obj.id)
        
        self._get_session()._load_obj.add_to_group(current, name)

    def get_queue(self):
        return self._get_session().queue

    def get_main_menu(self, sNameMainMenu:str=None)->Base:
        """Получить главное меню"""
        session = self._get_session()
        if sNameMainMenu:
            session.main_menu_form = validateOpenClass(sNameMainMenu)

        return session.main_menu_form

    def get_active_form_name(self):
        return self._get_session().active_form

    def get_active_form(self):
        return self.get_form(self.get_active_form_name())

    def set_active_form(self, value:str):
        self._get_session().active_form = value

    def get_open_form(self)->list[dict]:
        """Получение открытых форм"""
        return [{'caption': f_object.getInfoMeta()['metaForm']['caption'],
                'nameClass': f_name[:f_name.find('/')], 
                'nameForm': f_name[f_name.find('/')+1:], 
                'name': f_name} \
                for f_name, f_object in self._get_session().open_form.items()]

    def set_open_form(self, value: dict):
        self._get_session().open_form = value

    def get_form(self, form_name:str, default=None)->Base:
        """Получение формы"""
        session = self._get_session()  
        isMainMenu = (x:=FormRef.createByStr(form_name)).subClsName
        if isMainMenu:
            if not any(f == form_name for f in session.open_form.keys()):
                if default:
                    default.refresh()
                    session.open_form[form_name] = default
                else:
                    session.open_form[form_name] = validateOpenClass(sNameTab=x.clsName, sForm=x.subClsName)
            return session.open_form[form_name]
        return session.main_menu_form

    def remove_from(self, form_name:str)->str:
        """Удаление форм"""
        session = self._get_session()
        keys = list(session.open_form.keys())
        idx = keys.index(form_name)
        session.open_form.pop(form_name)
        if len(session.open_form) <= idx:
            idx -= 1
        return list(session.open_form.keys())[idx] if idx >= 0 else ""

    def commit(self):
        from core.empty.logic import EmptyLogic
        for listObj in self._get_session()._load_obj.values():
            for obj in listObj:
                EmptyLogic().commit(obj)

SESSION_STAGE = SessionStageManager()