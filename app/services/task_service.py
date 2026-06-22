from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.exceptions import NotFoundException


class TaskService:

    def __init__(self, db: Session):
        self.db = db

    def create(self, task_data: TaskCreate) -> Task:
        """Cria uma nova tarefa no banco."""
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_all(self, skip: int = 0, limit: int = 10) -> list[Task]:
        """Retorna todas as tarefas com paginação."""
        return self.db.query(Task).offset(skip).limit(limit).all()

    def get_by_id(self, task_id: int) -> Task:
        """Busca uma tarefa pelo ID ou lança NotFoundException."""
        db_task = self.db.query(Task).filter(Task.id == task_id).first()

        if not db_task:
            raise NotFoundException("Tarefa", task_id)

        return db_task

    def update(self, task_id: int, task_data: TaskUpdate) -> Task:
        """Atualiza os campos enviados de uma tarefa existente."""
        db_task = self.get_by_id(task_id)

        updated_fields = task_data.model_dump(exclude_unset=True)

        for field, value in updated_fields.items():
            setattr(db_task, field, value)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: int) -> None:
        """Remove uma tarefa do banco."""
        db_task = self.get_by_id(task_id)
        self.db.delete(db_task)
        self.db.commit()