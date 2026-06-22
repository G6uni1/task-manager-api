from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """
    Mixin reutilizável — adiciona created_at e updated_at
    em qualquer Model que herdar dele.

    Nota: updated_at usa server_default no banco e onupdate no lado
    Python (SQLAlchemy emite func.now() em cada UPDATE).
    Para garantir atualização em updates diretos no banco, adicione
    um trigger PostgreSQL (ver alembic/versions/).
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )