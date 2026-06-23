from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.tasks import router as tasks_router
from app.api.errors import (
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.core.config import settings
from app.core.exceptions import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Executado na inicialização e encerramento da aplicação."""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} iniciado!")
    yield
    print("👋 Aplicação encerrada.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=False,
    lifespan=lifespan,
)

_origins = ["*"]  # Em produção, substitua pelo domínio real do seu front

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(tasks_router)


@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à Task Manager API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}