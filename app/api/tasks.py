from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService

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
    """
    Cria uma nova tarefa com os dados fornecidos.

    - **title**: Título da tarefa (obrigatório)
    - **description**: Descrição detalhada (opcional)
    - **priority**: Prioridade — low, medium ou high (padrão: medium)
    """
    service = TaskService(db)
    return service.create(task_data)


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
    """
    Retorna a lista de tarefas com paginação.

    - **skip**: Quantos registros pular (padrão: 0)
    - **limit**: Quantos registros retornar (padrão: 10)
    """
    service = TaskService(db)
    return service.get_all(skip, limit)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Buscar tarefa por ID",
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Retorna uma tarefa específica pelo ID.

    - **task_id**: ID da tarefa
    """
    service = TaskService(db)
    return service.get_by_id(task_id)


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
    """
    Atualiza os dados de uma tarefa existente.

    - **task_id**: ID da tarefa a ser atualizada
    - Envie apenas os campos que deseja alterar
    """
    service = TaskService(db)
    return service.update(task_id, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar uma tarefa",
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Remove uma tarefa permanentemente.

    - **task_id**: ID da tarefa a ser removida
    """
    service = TaskService(db)
    service.delete(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)