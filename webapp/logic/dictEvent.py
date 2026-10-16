from core.sdk import formEvent, typeEvent, ACTIONDISPATCHER
from webapp.logic.dataClass import PutData
from webapp.logic import get_session, get_form, get_open_form
from webapp.logic.var import current_request, templates
from typing import Any

PATH_PARTIALS = 'partials/'

# 1. Выносим повторяющиеся HTML-шаблоны
TPL_WITH_TITLE = '{dataHtml}\n<title id="page-title" hx-swap-oob="true">{formCaption}</title>'
TPL_SIMPLE = '{dataHtml}'


def selected_app(event: formEvent) -> PutData:
    context = {
        # Исправлена опечатка: mata -> meta
        "meta_app": ACTIONDISPATCHER.getModulesConfig(),
        "isMain": False
    }
    return PutData(name_template=f"{PATH_PARTIALS}selectProject.html", context=context)


# 2. Исправлено название функции: bace -> base
def get_base_context(event: formEvent) -> dict:
    session = get_session()
    return {
        "active_form":event.form,
        "open_forms": get_open_form(),
        "meta_main_menu": session.main_menu_form.getInfoMeta(), 
        "main_menu": session.main_menu_form._get_parent_name(), 
        "isRenderMainMenu": event.type == typeEvent.openApp,
        "isRenderFormLine": event.type != typeEvent.refresh, 
    }


def open_and_refresh_form(event: formEvent) -> PutData:
    session = get_session()
    oper_form_object = get_form(event.form)
    session.active_form = event.form
    meta_form = oper_form_object.getInfoMeta()
    if '/' in event.form:
        form_name = f'form/{meta_form['metaForm']['typeForm']}'
    else:
        form_name = 'formOpenFrom'
        
    name_template = f"{PATH_PARTIALS}{form_name}.html"
    
    context = {
        "data": oper_form_object.getData(),
        "meta": meta_form,
        "open_forms": get_open_form(),
    } | get_base_context(event)

    return PutData(name_template=name_template, context=context)


def oper_app(event: formEvent) -> PutData:
    context = get_base_context(event)
    return PutData(name_template=f"{PATH_PARTIALS}formOpenFrom.html", context=context)


dataForEvent: dict[typeEvent, dict[str, Any]] = {
    typeEvent.openForm: {'data': open_and_refresh_form, 'templates': TPL_WITH_TITLE},
    typeEvent.refresh:  {'data': open_and_refresh_form, 'templates': TPL_SIMPLE},
    typeEvent.openApp:  {'data': oper_app,              'templates': TPL_WITH_TITLE},
    typeEvent.closeApp: {'data': selected_app,          'templates': TPL_SIMPLE},
}