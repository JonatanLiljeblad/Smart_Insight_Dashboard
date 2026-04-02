from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PROJECT_NAME: str = "Smart Insights Dashboard API"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/smartinsights"
    REDIS_URL: str = "redis://localhost:6379/0"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]


settings = Settings()
