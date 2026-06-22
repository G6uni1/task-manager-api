from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova tarefa",
)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Listar todas as tarefas",
)
def list_tasks(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Buscar tarefa por ID",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com id {task_id} não encontrada",
        )

    return db_task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Atualizar uma tarefa",
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
   
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com id {task_id} não encontrada",
        )

    # Pega apenas os campos que foram enviados pelo usuário
    updated_fields = task_data.model_dump(exclude_unset=True)

    # Atualiza apenas os campos recebidos
    for field, value in updated_fields.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    return db_task