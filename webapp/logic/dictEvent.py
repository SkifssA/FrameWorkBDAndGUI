from core.sdk import formEvent, typeEvent, ACTIONDISPATCHER, SESSION_STAGE, BaseSubClass
from webapp.logic.dataClass import PutData
from webapp.logic.var import current_request, templates
from typing import Any

# 1. Выносим повторяющиеся HTML-шаблоны
TPL_SIMPLE = '{dataHtml}'
TPL_TITLE = '<title id="page-title" hx-swap-oob="true">{formCaption}</title>'
TPL_FORM_BAR_MAIN_MENU = '<div id="main_menu_form_bar" hx-swap-oob="true">{form_bar}</div>'
TPL_FORM_BAR_CH = '<div id="forms-bar-ch-{parent}" hx-swap-oob="true">{form_bar_ch}</div>'

def get_form_bar():
    context = {
        "open_forms": SESSION_STAGE.get_open_form(),
        "active_form": SESSION_STAGE.get_active_form_name(),
        "main_menu": SESSION_STAGE.get_main_menu()._get_parent_name()
    }

    return PutData(name_template=f"partials/form_bar_main_menu.html"
                   , context=context
                   , caption_form=SESSION_STAGE.get_main_menu().metaInfo.caption)

def get_form_bar_ch(event: formEvent):
    f = SESSION_STAGE.get_active_form()
    context = {
        "meta": f.getInfoMeta(),
        "active_form_ch": event.form
    }

    if (x:=event.form.split('.')[-1]) in f.children.keys():
        f.active_ch = list(f.children.keys()).index(x)

    return PutData(name_template=f"partials/form_bar_ch.html"
                   , context=context
                   , caption_form=SESSION_STAGE.get_main_menu().metaInfo.caption)

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
    oper_form_object = SESSION_STAGE.get_form(w[0], event.formObject)
    oper_form_object = oper_form_object._get_children(event.form)
    SESSION_STAGE.set_active_form(w[0])
    name_template, context = get_template_and_context(oper_form_object)

    return PutData(name_template=name_template
                   , context=context
                   , caption_form=oper_form_object.metaInfo.caption)

def getHtmlForm(form):
    name_template, context = get_template_and_context(form)
    return templates.TemplateResponse(
                request=current_request.get(),
                name=name_template,
                context=context,
            ).body.decode('utf-8')

def get_template_and_context(form:BaseSubClass)->tuple[str, dict[str, Any]]:
    active_form = SESSION_STAGE.get_active_form()
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
    elif form.getInfoMeta()['metaForm']['typeForm'] == 'card':
            context['idItem'] = form.getData()[0]['id']

    if form.childrenMeta['bottom'] != []:
        active_form_ch = form.childrenMeta['bottom'][form.active_ch]['metaForm']['name']
        context['active_form_ch'] = active_form_ch
        context['formChBottom'] = getHtmlForm(active_form._get_children(active_form_ch))

    if form.childrenMeta['right'] != []:
        for i in form.childrenMeta['right']:
            context['formChRight'] += getHtmlForm(active_form._get_children(i['metaForm']['name'])) + '\n'

    if form.childrenMeta['left'] != []:
        for i in form.childrenMeta['left']:
            context['formChLeft'] += getHtmlForm(active_form._get_children(i['metaForm']['name'])) + '\n'

    return (name_template, context)


def refresh_form(event: formEvent)->PutData:
    w = event.form.split('.')
    oper_form_object = SESSION_STAGE.get_form(w[0], event.formObject)
    oper_form_object = oper_form_object._get_children(event.form)
    meta_form = oper_form_object.getInfoMeta()
    typeForm = meta_form['metaForm']['typeForm'].lower()
    SESSION_STAGE.set_active_form(w[0])

    name_template = f"form/{typeForm}.html"
    
    context = {
        "data": oper_form_object.getData(),
        "meta": meta_form
    }

    if typeForm == 'list':
        context['id_row'] = oper_form_object.active_row

    return PutData(name_template=name_template
                   , context=context
                   , caption_form=oper_form_object.metaInfo.caption)

def close_form(event: formEvent) -> PutData:
    name_form = SESSION_STAGE.remove_from(event.form)
    if name_form == '':
        SESSION_STAGE.set_active_form({})
        return PutData(name_template=None
                       , context=None
                       , caption_form=SESSION_STAGE.get_main_menu().metaInfo.caption)

    event.form = name_form
    return open_form(event)

def oper_app(event: formEvent) -> PutData:
    mm = SESSION_STAGE.get_main_menu()
    context = {
        'meta_main_menu': mm.getInfoMeta(),
        'main_menu': mm._get_parent_name(),
        'active_form': None,
        'open_forms': {}
    }
    return PutData(name_template=f"/form/mainmenu.html"
                   , context=context
                   , caption_form=mm.metaInfo.caption)


dataForEvent: dict[typeEvent, dict[str, Any]] = {
    typeEvent.openForm:      {'data': open_form,             'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU},
    typeEvent.open_form_ch:  {'data': open_form,             'templates': TPL_SIMPLE + TPL_FORM_BAR_CH},
    typeEvent.refresh:       {'data': refresh_form,          'templates': TPL_SIMPLE},
    typeEvent.openApp:       {'data': oper_app,              'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU},
    typeEvent.closeApp:      {'data': selected_app,          'templates': TPL_SIMPLE},
    typeEvent.closeForm:     {'data': close_form,            'templates': TPL_SIMPLE + TPL_TITLE + TPL_FORM_BAR_MAIN_MENU}
}