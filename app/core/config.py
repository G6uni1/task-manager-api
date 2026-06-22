from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Task Manager API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/taskmanager"

    class Config:
        env_file = ".env"         
        case_sensitive = True      


settings = Settings()