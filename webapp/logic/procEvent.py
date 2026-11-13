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
            typeEvent.openApp: {'metod': self.openApp}    
        }

    def get_str_by_event(self, event:formEvent):
        """Метод для получение готовой стоки html"""
        return self.proc_event[event.type]['metod'](event)

    def openApp(self, event:formEvent)->str:
        form = SESSION_STAGE.get_main_menu(event.form)
        return getHtmlForm('component/mainmenu.html', {'items_for_main_menu': form.getInfoMeta()})


PROC_EVENT = ProcEvent()