# Task Manager API

API RESTful para gerenciamento de tarefas construída com FastAPI e PostgreSQL.

## Tecnologias

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2
- pytest

## Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/task-manager-api.git
cd task-manager-api

# Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

## Configuração do Banco

```bash
# Crie o banco de dados
psql -U postgres -c "CREATE DATABASE taskmanager;"

# Rode as migrations
alembic upgrade head
```

## Executando

```bash
uvicorn main:app --reload
```

Acesse a documentação em: http://localhost:8000/docs

## Testes

```bash
# Crie o banco de testes
psql -U postgres -c "CREATE DATABASE taskmanager_test;"

# Rode os testes
pytest tests/ -v
```

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | /tasks/ | Criar tarefa |
| GET | /tasks/ | Listar tarefas |
| GET | /tasks/{id} | Buscar por ID |
| PUT | /tasks/{id} | Atualizar tarefa |
| DELETE | /tasks/{id} | Deletar tarefa |
| GET | /health | Health check |