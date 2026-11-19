from fastapi import APIRouter, Request

from core.sdk import SESSION_STAGE

router = APIRouter(prefix='/api')

@router.get('/{nameObj}/rows')
def rows_table(request: Request, nameObj:str):
    if x:=SESSION_STAGE.get_app()._children.get_form(nameObj):
        return x.getData()
