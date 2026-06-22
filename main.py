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


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    # SECURITY: debug=True expõe stack traces completos nas respostas de erro.
    # Mantemos False em produção; o .env de dev pode setar DEBUG=True apenas
    # para o echo do SQLAlchemy (ver database.py), não para o FastAPI.
    debug=False,
)

# CORS — ajuste allowed_origins conforme os domínios do seu front-end
_origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A ordem importa: handlers mais específicos antes do genérico
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(tasks_router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Task Manager API", "version": settings.APP_VERSION}


@app.get("/health")
def health_check():
    """Endpoint para health checks de load balancers / containers."""
    return {"status": "ok"}