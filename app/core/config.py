from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Task Manager API"
    APP_VERSION: str = "0.1.0"

    # SECURITY: default False — DEBUG=True deve ser explícito no .env de dev
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5432/taskmanager"
    TEST_DATABASE_URL: str = "postgresql://postgres:postgres123@localhost:5432/taskmanager_test"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()