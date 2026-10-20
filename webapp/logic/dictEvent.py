from core.sdk import formEvent, typeEvent, ACTIONDISPATCHER
from webapp.logic.dataClass import PutData
from webapp.logic import get_session, get_form, get_open_form
from webapp.logic.var import current_request, templates
from webapp.logic.sessionManager import remove_from
from typing import Any

PATH_PARTIALS = 'partials/'

# 1. Выносим повторяющиеся HTML-шаблоны
TPL_SIMPLE = '{dataHtml}'
TPL_TITLE = '<title id="page-title" hx-swap-oob="true">{formCaption}</title>'
TPL_FORM_BAR_MAIN_MENU = '<div id="main_menu_form_bar" hx-swap-oob="true">{form_bar}</div>'

def get_form_bar():
    context = {
        "open_forms": get_open_form(),
        "active_form": get_session().active_form,
        "main_menu": get_session().main_menu_form._get_parent_name()
    }
    print('form_bar_context', context)
    return PutData(name_template=f"{PATH_PARTIALS}formbar.html"
                   , context=context
                   , caption_form=get_session().main_menu_form.object.metaInfo.caption)

def selected_app(event: formEvent) -> PutData:
    context = {
        "meta_app": ACTIONDISPATCHER.getModulesConfig(),
        "isMain": False
    }
    return PutData(name_template=f"{PATH_PARTIALS}selectProject.html"
                   , context=context
                   , caption_form='Выбор приложений')

def open_and_refresh_form(event: formEvent) -> PutData:
    oper_form_object = get_form(event.form, event.formObject)
    meta_form = oper_form_object.getInfoMeta()
    form_name = f'{meta_form['metaForm']['typeForm']}'

    get_session().active_form = oper_form_object._get_full_name()

    name_template = f"{PATH_PARTIALS}form/{form_name}.html"

    context = {
        "data": oper_form_object.getData(),
        "meta": meta_form,
    }

    if meta_form['metaForm']['typeForm'] == 'list':
        context['id_row'] = oper_form_object.object.active_row

    return PutData(name_template=name_template
                   , context=context
                   , caption_form=oper_form_object.object.metaInfo.caption)

def close_form(event: formEvent) -> PutData:
    name_form = remove_from(event.form)
    if name_form == '':
        print("ОТКРЫТЫХ ВКЛАДОК НЕТ")
        get_session().open_form = {}
        get_session().active_form = None
        return PutData(name_template=None
                       , context=None
                       , caption_form=get_session().main_menu_form.object.metaInfo.caption)

    event.form = name_form
    return open_and_refresh_form(event)

def oper_app(event: formEvent) -> PutData:
    session = get_session()
    context = {
        'meta_main_menu': session.main_menu_form.getInfoMeta(),
        'main_menu': session.main_menu_form._get_parent_name(),
        'active_form': None,
        'open_forms': {}
    }
    return PutData(name_template=f"{PATH_PARTIALS}/form/mainmenu.html"
                   , context=context
                   , caption_form=get_session().main_menu_form.object.metaInfo.caption)


dataForEvent: dict[typeEvent, dict[str, Any]] = {
    typeEvent.openForm:  {'data': open_and_refresh_form, 'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU},
    typeEvent.refresh:   {'data': open_and_refresh_form, 'templates': TPL_SIMPLE},
    typeEvent.openApp:   {'data': oper_app,              'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU},
    typeEvent.closeApp:  {'data': selected_app,          'templates': TPL_SIMPLE},
    typeEvent.closeForm: {'data': close_form, 'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU}
}