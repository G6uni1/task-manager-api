from fastapi import FastAPI
from app.api.tasks import router as tasks_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Incluindo o roteador de tarefas
app.include_router(tasks_router)


@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Task Manager API"}