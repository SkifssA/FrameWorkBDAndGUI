from fastapi import HTTPException

from core.sdk import ACTIONDISPATCHER

def validateOpenClass(sNameTab:str, session_id:str, sForm:str = 'Default'):
    class_ = ACTIONDISPATCHER.getClassByName(f"{sNameTab}")
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            return form
        raise HTTPException(
                status_code=404, detail=f"Отображение {sForm} класса {sNameTab} не найдено"
            )
    raise HTTPException(status_code=404, detail=f"Класс {sNameTab} не найден")
