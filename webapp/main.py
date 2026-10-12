from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from core.sdk import ACTIONDISPATCHER, eventSignal

app = FastAPI()
templates = Jinja2Templates(directory="webapp/templates")

app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

def handler(sender, **kwargs):
    print(kwargs.get('fromEvent'))

eventSignal.connect(handler)


@app.get("/{sNameTab}/{sForm}")
async def oper_form(sNameTab: str, sForm: str, request: Request):
    class_ = ACTIONDISPATCHER.getClassByName(f"{sNameTab}")
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            return templates.TemplateResponse(
                request=request,
                name=f"partials/{sForm.lower()}.html",
                context={
                    "data": form.getData(),
                    "meta": form.getInfoMeta(),
                    "url": f"{sForm}",
                },
            )
        raise HTTPException(
            status_code=404, detail=f"Отображение {sForm} таблицы {sNameTab} не найдено"
        )
    raise HTTPException(status_code=404, detail=f"Таблица {sNameTab} не найдена")


@app.get("/{sNameTab}/{sForm}/action/{oper}")
async def action_oper(sNameTab: str, sForm: str, oper: str, request: Request):
    class_ = ACTIONDISPATCHER.getClassByName(f"{sNameTab}")
    if class_:
        form = class_._getFormByName(sForm)()
        if form:
            if oper in form.getSetterAndOperName():
                form.get_oper_handler()[oper]()
                return Response(content="", status_code=200)
    raise HTTPException(
        status_code=404, detail=f"В таблице {sNameTab} не найдена опрерация {oper}"
    )


def runServer():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
