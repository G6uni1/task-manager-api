from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.task import Priority


class TaskBase(BaseModel):
    """Campos compartilhados entre Create e Update."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Título da tarefa",
        examples=["Estudar FastAPI"],
    )
    description: Optional[str] = Field(
        None,
        description="Descrição detalhada da tarefa",
        examples=["Estudar por 2 horas"],
    )
    priority: Priority = Field(
        Priority.medium,
        description="Prioridade da tarefa",
        examples=["medium"],
    )


class TaskCreate(TaskBase):
    """Schema para criação de tarefa — recebido no POST."""
    pass


class TaskUpdate(BaseModel):
    """Schema para atualização — todos os campos são opcionais."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Título da tarefa",
    )
    description: Optional[str] = Field(
        None,
        description="Descrição da tarefa",
    )
    completed: Optional[bool] = Field(
        None,
        description="Status de conclusão",
    )
    priority: Optional[Priority] = Field(
        None,
        description="Prioridade da tarefa",
    )


class TaskResponse(TaskBase):
    """Schema de resposta — o que a API devolve ao usuário."""
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}