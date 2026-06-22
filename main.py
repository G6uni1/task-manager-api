from fastapi import FastAPI
from app.api.tasks import router as tasks_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models import Task  # 🆕 importar o model

# Cria as tabelas automaticamente (temporário — Alembic assume isso na ETAPA 14)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(tasks_router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Task Manager API"}