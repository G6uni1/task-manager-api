# -*- coding: utf-8 -*-
import os
import pytest

os.environ["PGCLIENTENCODING"] = "utf8"
os.environ["PYTHONIOENCODING"] = "utf-8"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from main import app
from app.core.config import settings

engine_test = create_engine(settings.TEST_DATABASE_URL)

SessionTest = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


def override_get_db():
    db = SessionTest()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_database():
    yield
    db = SessionTest()
    try:
        db.execute(text("DELETE FROM tasks"))
        db.commit()
    finally:
        db.close()