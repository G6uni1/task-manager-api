from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.tasks import router as tasks_router
from app.api.errors import (
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import AppException
from app.models import Task

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(tasks_router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Task Manager API"}