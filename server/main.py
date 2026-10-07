from fastapi import FastAPI, HTTPException

from core.sdk import ACTIONDISPATCHER

app = FastAPI()

@app.get("/api/data/{sNameTab}")
def read_item(sNameTab: str):
    form = ACTIONDISPATCHER.action(f'{sNameTab}.List')
    if form:
        return form.getData()
    raise HTTPException(status_code=404, detail=f"Таблица {sNameTab} не найдена")