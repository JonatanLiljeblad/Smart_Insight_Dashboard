from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_PLACEHOLDER_SECRETS = {"change-me-in-production", "changeme", "secret", ""}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # General
    PROJECT_NAME: str = "Smart Insights Dashboard API"

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/smartinsights"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS — accepts a JSON list or comma-separated string
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: object) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v  # type: ignore[return-value]

    # Auth
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    REFRESH_TOKEN_COOKIE_SECURE: bool = False
    REFRESH_TOKEN_COOKIE_SAMESITE: str = "lax"

    @field_validator("JWT_SECRET", mode="after")
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if v.lower() in _PLACEHOLDER_SECRETS:
            import warnings
            warnings.warn(
                "JWT_SECRET is using a placeholder value. "
                "Set a strong secret via environment variable before deploying.",
                stacklevel=2,
            )
        return v

    @field_validator("REFRESH_TOKEN_COOKIE_SAMESITE", mode="after")
    @classmethod
    def validate_same_site(cls, v: str) -> str:
        normalized = v.lower()
        allowed = {"lax", "strict", "none"}
        if normalized not in allowed:
            raise ValueError(
                f"REFRESH_TOKEN_COOKIE_SAMESITE must be one of {sorted(allowed)}"
            )
        return normalized


settings = Settings()
