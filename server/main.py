from fastapi import FastAPI, HTTPException

from core.sdk import ACTIONDISPATCHER

app = FastAPI()

@app.get("/api/data/{sNameTab}")
def read_item(sNameTab: str):
    form = ACTIONDISPATCHER.getClassByName(f'{sNameTab}')
    if form:
        return form.List().getData()
    raise HTTPException(status_code=404, detail=f"Таблица {sNameTab} не найдена")