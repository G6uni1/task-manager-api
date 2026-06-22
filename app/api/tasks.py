from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("/")
def list_tasks():
    return {"message": "Lista de tarefas (placeholder)"}


@router.post("/")
def create_task():
    return {"message": "Tarefa criada (placeholder)"}