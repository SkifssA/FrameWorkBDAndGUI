from core.sdk import formEvent, typeEvent, ACTIONDISPATCHER
from webapp.logic.dataClass import PutData
from webapp.logic import get_session, get_form, get_open_form
from webapp.logic.var import current_request, templates
from webapp.logic.sessionManager import remove_from
from typing import Any

# 1. Выносим повторяющиеся HTML-шаблоны
TPL_SIMPLE = '{dataHtml}'
TPL_TITLE = '<title id="page-title" hx-swap-oob="true">{formCaption}</title>'
TPL_FORM_BAR_MAIN_MENU = '<div id="main_menu_form_bar" hx-swap-oob="true">{form_bar}</div>'
TPL_FORM_BAR_CH = '<div id="forms-bar-ch-{parent}" hx-swap-oob="true">{form_bar_ch}</div>'

def get_form_bar():
    context = {
        "open_forms": get_open_form(),
        "active_form": get_session().active_form,
        "main_menu": get_session().main_menu_form._get_parent_name()
    }

    if get_session().active_form:
        meta_form = get_form(get_session().active_form)
        if meta_form.getInfoMeta()['metaForm']['typeForm'] == 'card':
            context['idItem'] = meta_form.getData()[0]['id']

    return PutData(name_template=f"partials/form_bar_main_menu.html"
                   , context=context
                   , caption_form=get_session().main_menu_form.object.metaInfo.caption)

def get_form_bar_ch(event: formEvent):
    f = get_form(get_session().active_form)
    context = {
        "meta": f.getInfoMeta(),
        "active_form_ch": event.form
    }

    if event.form.split('.')[-1] in f.children.keys():
        f.active_ch = list(f.children.keys()).index(event.form.split('.')[-1]) + 1

    return PutData(name_template=f"partials/form_bar_ch.html"
                   , context=context
                   , caption_form=get_session().main_menu_form.object.metaInfo.caption)

def selected_app(event: formEvent) -> PutData:
    context = {
        "meta_app": ACTIONDISPATCHER.getModulesConfig(),
        "isMain": False
    }
    return PutData(name_template=f"partials/selectProject.html"
                   , context=context
                   , caption_form='Выбор приложений')

def open_form(event: formEvent) -> PutData:
    w = event.form.split('.')
    oper_form_object = get_form(w[0], event.formObject)
    oper_form_object = oper_form_object._get_children(event.form)
    meta_form = oper_form_object.getInfoMeta()

    get_session().active_form = w[0]

    name_template = f"form/baseForm.html"
    
    context = {
        "data": oper_form_object.getData(),
        "meta": meta_form,
        "active_form_ch": None,
        "formChBottom": '',
        "formChLeft": '',
        "formChRight": ''
    }

    if oper_form_object.childrenMeta['bottom'] != [] :
        active_form_ch = oper_form_object.childrenMeta['bottom'][oper_form_object.active_ch-1]['metaForm']['name']
        context['active_form_ch'] = active_form_ch
        context['formChBottom'] = getHtmlForm(oper_form_object._get_children('.'.join(active_form_ch.split('.')[-2:])), oper_form_object)

    if oper_form_object.childrenMeta['right'] != [] :
        for i in oper_form_object.childrenMeta['right']:
            context['formChRight'] += getHtmlForm(oper_form_object._get_children('.'.join(i['metaForm']['name'].split('.')[-2:])), oper_form_object) + '\n'
    
    if oper_form_object.childrenMeta['left'] != [] :
        for i in oper_form_object.childrenMeta['left']:
            context['formChLeft'] += getHtmlForm(oper_form_object._get_children('.'.join(i['metaForm']['name'].split('.')[-2:])), oper_form_object) + '\n'

    if meta_form['metaForm']['typeForm'] == 'list':
        context['id_row'] = oper_form_object.active_row

    return PutData(name_template=name_template
                   , context=context
                   , caption_form=oper_form_object.object.metaInfo.caption)

def refresh_form(event: formEvent)->PutData:
    w = event.form.split('.')
    oper_form_object = get_form(w[0], event.formObject)
    oper_form_object = oper_form_object._get_children(event.form)
    meta_form = oper_form_object.getInfoMeta()
    typeForm = meta_form['metaForm']['typeForm'].lower()
    get_session().active_form = w[0]

    name_template = f"form/{typeForm}.html"
    
    context = {
        "data": oper_form_object.getData(),
        "meta": meta_form
    }

    if typeForm == 'list':
        context['id_row'] = oper_form_object.active_row

    return PutData(name_template=name_template
                   , context=context
                   , caption_form=oper_form_object.object.metaInfo.caption)

def getHtmlForm(form, mainForm):

    name_template = f"form/baseForm.html"

    context = {
        "data": form.getData(),
        "meta": form.getInfoMeta(),
        "metaCh": list(i.getInfoMeta() for i in form.children.values()),
        "active_form_ch": None,
        "formChBottom": '',
        "formChLeft": '',
        "formChRight": ''
    }

    if form.getInfoMeta()['metaForm']['typeForm'] == 'list':
        context['id_row'] = form.active_row

    if form.childrenMeta['bottom'] != [] :
        active_form_ch = form.childrenMeta['bottom'][form.active_ch-1]['metaForm']['name']
        context['active_form_ch'] = active_form_ch
        context['formChBottom'] = getHtmlForm(mainForm._get_children(active_form_ch), mainForm)

    if form.childrenMeta['right'] != [] :
        for i in form.childrenMeta['right']:
            context['formChRight'] += getHtmlForm(mainForm._get_children(i['metaForm']['name']), mainForm) + '\n'

    if form.childrenMeta['left'] != [] :
        for i in form.childrenMeta['left']:
            context['formChLeft'] += getHtmlForm(mainForm._get_children(i['metaForm']['name']), mainForm) + '\n'

    return templates.TemplateResponse(
                request=current_request.get(),
                name=name_template,
                context=context,
            ).body.decode('utf-8')

def close_form(event: formEvent) -> PutData:
    name_form = remove_from(event.form)
    if name_form == '':
        get_session().open_form = {}
        return PutData(name_template=None
                       , context=None
                       , caption_form=get_session().main_menu_form.object.metaInfo.caption)

    event.form = name_form
    return open_form(event)

def oper_app(event: formEvent) -> PutData:
    session = get_session()
    context = {
        'meta_main_menu': session.main_menu_form.getInfoMeta(),
        'main_menu': session.main_menu_form._get_parent_name(),
        'active_form': None,
        'open_forms': {}
    }
    return PutData(name_template=f"/form/mainmenu.html"
                   , context=context
                   , caption_form=get_session().main_menu_form.object.metaInfo.caption)


dataForEvent: dict[typeEvent, dict[str, Any]] = {
    typeEvent.openForm:      {'data': open_form,             'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU},
    typeEvent.open_form_ch:  {'data': open_form,             'templates': TPL_SIMPLE + TPL_FORM_BAR_CH},
    typeEvent.refresh:       {'data': refresh_form,          'templates': TPL_SIMPLE},
    typeEvent.openApp:       {'data': oper_app,              'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU},
    typeEvent.closeApp:      {'data': selected_app,          'templates': TPL_SIMPLE},
    typeEvent.closeForm:     {'data': close_form,            'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU}
}