from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import asyncio
import logging
import os
from starlette.middleware.sessions import SessionMiddleware
import uuid

from core.sdk import current_session_id

from webapp.logic import registrSignal, set_main_loop, current_request
from webapp.endpoints.projectEndPoint import router as roputerProject
from webapp.endpoints.staticEndPoint import router as staticProject

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код при старте (вместо @app.on_event("startup"))
    loop = asyncio.get_running_loop()
    set_main_loop(loop)
    logger.debug("Main loop сохранен для синхронных сигналов")
    
    yield  # Здесь работает приложение
    
    # Код при завершении (вместо @app.on_event("shutdown"))
    logger.debug("Приложение завершается")

app = FastAPI(lifespan=lifespan)

# 1. НАСТРОЙКА БЕЗОПАСНОСТИ
# ⚠️ В реальности бери из .env файла! Например: SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = os.getenv("SESSION_SECRET", "super-secret-key-change-in-production-123!")

app.mount("/static", StaticFiles(directory="webapp/web/static"), name="static")
app.include_router(staticProject)
app.include_router(roputerProject)
registrSignal()


@app.middleware("http")
async def session_context_middleware(request: Request, call_next):
    # 1. Достаем куку ПРЯМО из request. Никаких зависимостей Cookie() не нужно!
    # 1. Пытаемся получить ID сессии из данных cookie
    session_id = request.session.get("session_id")
    
    # 2. Если его нет (пользователь зашел впервые или cookie истекла)
    if not session_id:
        # Генерируем уникальный ID для этого сеанса
        session_id = str(uuid.uuid4())
        # Сохраняем его в сессию. 
        # SessionMiddleware автоматически запишет это в cookie клиенту!
        request.session["session_id"] = session_id
    
    # 2. Устанавливаем контекст
    token_session_id = current_session_id.set(session_id)
    token_request = current_request.set(request)
    
    try:
        response = await call_next(request)
    finally:
        current_session_id.reset(token_session_id)
        current_request.reset(token_request)
        
    return response

# Подключаем middleware сессий
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="my_web_app_session", # Имя cookie
    max_age=60 * 60 * 24 * 7,            # Время жизни: 7 дней
    same_site="lax",                     # Защита от CSRF
    https_only=os.getenv("ENV") == "prod" # В продакшене только HTTPS
)



def runServer():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
