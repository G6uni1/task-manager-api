from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Task Manager API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    DATABASE_URL: str = "postgresql+pg8000://postgres:postgres123@localhost:5432/taskmanager"
    TEST_DATABASE_URL: str = "postgresql+pg8000://postgres:postgres123@localhost:5432/taskmanager_test"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def database_url_fixed(self) -> str:
        """Corrige o prefixo da URL para pg8000."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+pg8000://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+pg8000://", 1)
        return url


settings = Settings()