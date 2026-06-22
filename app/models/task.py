import enum
from typing import Optional
from sqlalchemy import String, Text, Boolean, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.models.base import TimestampMixin


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        # server_default garante o padrão mesmo em INSERTs via SQL puro,
        # enquanto default cobre INSERTs feitos pelo SQLAlchemy
        default=False,
        server_default="false",
        nullable=False,
    )

    priority: Mapped[Priority] = mapped_column(
        # create_type=False: o tipo enum já é criado pela migration do Alembic;
        # sem isso o SQLAlchemy tenta criar novamente e lança ProgrammingError
        SAEnum(Priority, name="priority", create_type=False),
        default=Priority.medium,
        server_default=Priority.medium.value,
        nullable=False,
    )