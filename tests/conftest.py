import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from main import app

# Banco de dados exclusivo para testes
TEST_DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/taskmanager_test"

engine_test = create_engine(TEST_DATABASE_URL)

SessionTest = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


def override_get_db():
    """Substitui o banco real pelo banco de testes."""
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()


# Sobrescreve a dependência get_db nos testes
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria as tabelas antes dos testes e remove depois."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def client():
    """Retorna o TestClient para os testes."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_database():
    """Limpa as tabelas antes de cada teste."""
    yield
    db = SessionTest()
    try:
        db.execute(__import__("sqlalchemy").text("DELETE FROM tasks"))
        db.commit()
    finally:
        db.close()