"""create_tasks_table

Revision ID: e6ba00e91f93
Revises: 
Create Date: 2026-06-22 17:51:44.990447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e6ba00e91f93'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cria o enum de prioridade
    priority_enum = sa.Enum('low', 'medium', 'high', name='priority')
    priority_enum.create(op.get_bind(), checkfirst=True)

    # Cria a tabela tasks
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', name='priority'), nullable=False, server_default='medium'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)

    # Trigger para atualizar updated_at automaticamente no banco
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER tasks_updated_at
        BEFORE UPDATE ON tasks
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS tasks_updated_at ON tasks;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column;")
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    sa.Enum(name='priority').drop(op.get_bind(), checkfirst=True)