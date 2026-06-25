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
    # Cria o enum apenas se não existir
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE priority AS ENUM ('low', 'medium', 'high');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Cria a tabela apenas se não existir
    op.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT false,
            priority priority NOT NULL DEFAULT 'medium',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            PRIMARY KEY (id)
        );
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_tasks_id ON tasks (id);
    """)

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
        DROP TRIGGER IF EXISTS tasks_updated_at ON tasks;
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