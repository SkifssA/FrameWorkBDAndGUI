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
            typeEvent.openForm: {'metod': self.openForm}    
        }

    def get_str_by_event(self, event:formEvent):
        """Метод для получение готовой стоки html"""
        return self.proc_event[event.type]['metod'](event)

    def openApp(self, event:formEvent)->str:
        form = SESSION_STAGE.get_app(event.form.split('-')[0])
        return getHtmlForm('component/mainmenu.html', {'app': form.getInfoMeta()})

    def openForm(self, event:formEvent)->str:
        from webapp.logic.build_client_config import build_table_config_from_meta
        return getHtmlForm('component/tab.html', 
                           {
                               'table_config': build_table_config_from_meta(event.formObject.getInfoMeta())
                               ,'table_id': event.form
                               ,'itemCh': event.formObject.getInfoMeta()
                            })

    def switchTab(self, event:formEvent)->str:
        return json.dumps({'panel': event.form})


PROC_EVENT = ProcEvent()