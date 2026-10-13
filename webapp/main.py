from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from webapp.logic import registrSignal
from webapp.api.projectEndPoint import router as roputerProject
from webapp.api.staticEndPoint import router as staticProject

app = FastAPI()
app.mount("/static", StaticFiles(directory="webapp/web/static"), name="static")
app.include_router(roputerProject)
app.include_router(staticProject)
registrSignal()


def runServer():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
