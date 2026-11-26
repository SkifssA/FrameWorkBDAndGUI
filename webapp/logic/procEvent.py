import json

from core.sdk import formEvent, typeEvent, SESSION_STAGE

from webapp.logic.var import current_request, templates

def getHtmlForm(name_template, context, InStr: bool=True):
    t = templates.TemplateResponse(
                request=current_request.get(),
                name=name_template,
                context=context,
            )
    if not InStr: return t

    return t.body.decode('utf-8')

class ProcEvent:
    def __init__(self):
        self.proc_event = {
            typeEvent.openApp: {'metod': self.openApp},  
            typeEvent.switchTab: {'metod': self.switchTab},  
            typeEvent.openForm: {'metod': self.openForm},
            typeEvent.refresh: {'metod': self.refresh}    
        }

    def get_str_by_event(self, event:formEvent):
        """Метод для получение готовой стоки html"""
        return self.proc_event[event.type]['metod'](event)

    def openApp(self, event:formEvent)->tuple[str, str]:
        return event.personType, getHtmlForm('component/mainmenu.html', {'app': event.form.getInfoMeta()})

    def openForm(self, event:formEvent)->tuple[str, str]:
        return event.personType, getHtmlForm('component/tab.html', {'itemCh': event.form.getInfoMeta()})

    def refresh(self, event:formEvent)->tuple[str, str]:
        return event.personType, getHtmlForm('component/form.html', {'itemCh': event.form.getInfoMeta()})

    def switchTab(self, event:formEvent)->tuple[str, str]:
        return event.personType, json.dumps({'panel': event.form.full_name()})


PROC_EVENT = ProcEvent()