from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio

from core.sdk import current_session_id

from webapp.logic import registrSignal, set_main_loop
from webapp.api.projectEndPoint import router as roputerProject
from webapp.api.staticEndPoint import router as staticProject

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код при старте (вместо @app.on_event("startup"))
    loop = asyncio.get_running_loop()
    set_main_loop(loop)
    print("✅ Main loop сохранен для синхронных сигналов")
    
    yield  # Здесь работает приложение
    
    # Код при завершении (вместо @app.on_event("shutdown"))
    print("🛑 Приложение завершается")

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="webapp/web/static"), name="static")
app.include_router(staticProject)
app.include_router(roputerProject)
registrSignal()



@app.middleware("http")
async def session_context_middleware(request: Request, call_next):
    # 1. Достаем куку ПРЯМО из request. Никаких зависимостей Cookie() не нужно!
    session_id = request.cookies.get("session_id", "default")
    
    # 2. Устанавливаем контекст
    token = current_session_id.set(session_id)
    
    try:
        response = await call_next(request)
    finally:
        current_session_id.reset(token)
        
    return response





def runServer():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
