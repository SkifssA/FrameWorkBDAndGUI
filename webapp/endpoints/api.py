from fastapi import APIRouter, Request

from core.sdk import SESSION_STAGE
from webapp.logic.procEvent import getHtmlForm

router = APIRouter(prefix='/api')

@router.get('/{nameObj}/rows')
def rows_table(request: Request, nameObj:str):
    if x:=SESSION_STAGE.get_app()._children.get_form(nameObj):
        return x.getData()

@router.get('/meta/{nameObj}')
def rows_table(request: Request, nameObj:str):
    if x:=SESSION_STAGE.get_app()._children.get_form(nameObj):
        return getHtmlForm('component/form.html', {'itemCh': x.getInfoMeta()}, InStr=False)
        
