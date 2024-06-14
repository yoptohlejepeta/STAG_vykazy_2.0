"""Settings aplikace.

Načtení konfigurace z proměnných prostředí.
"""

from pydantic import AnyHttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LogfireSettings(BaseSettings):
    """Nastavení logování do Logfire."""

    token: SecretStr
    project_name: str


class StagSettings(BaseSettings):
    """STAG proměnné."""

    login: AnyHttpUrl


class Settings(BaseSettings):
    """Souhrn nastavení."""

    logfire: LogfireSettings | None = None
    stag: StagSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        arbitrary_types_allowed=True,
        env_nested_delimiter="__",
    )


settings = Settings()
