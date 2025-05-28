import logging

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class CacheSettings(BaseModel):
    autocomplete_cache_maxsize: int
    autocomplete_cache_ttl: int
    weather_cache_maxsize: int
    weather_cache_ttl: int


class Settings(BaseSettings):
    secret_key: str
    session_type: str = Field(
        default="filesystem",
        description="Тип хранения сессий. Доступные варианты: 'filesystem', 'redis', 'memcached'.",
        examples=["filesystem", "redis", "memcached"],
    )
    geolocator_user_agent: str = Field(
        default="weather_app",
        description="User agent для геолокатора Nominatim.",
    )
    cache: CacheSettings = Field(
        default_factory=lambda: CacheSettings(
            autocomplete_cache_maxsize=1000,
            autocomplete_cache_ttl=86400,
            weather_cache_maxsize=1000,
            weather_cache_ttl=600,
        ),
        description="Настройки кэша для приложения.",
    )
    """Значения по умолчанию для кэша:
    - `autocomplete_cache_maxsize`: 1000
    - `autocomplete_cache_ttl`: 86400 (1 день)
    - `weather_cache_maxsize`: 1000
    - `weather_cache_ttl`: 600 (10 минут)
    """
    database_path: str = Field(
        default="data",
        description="Путь к базе данных SQLite для хранения истории запросов.",
    )
    """Путь к базе данных SQLite для хранения истории запросов. По умолчанию 'weather.db'."""
    logs_dir: str = Field(
        default="logs", description="Директория для хранения логов приложения."
    )
    """Директория для хранения логов приложения. По умолчанию 'logs'."""
    debug: bool = Field(
        default=False,
        description="Enable debug mode for the application",
    )
    """DEBUG-режим приложения. По умолчанию False. При включенном режиме можно посмотреть настройки приложения через эндпоинт `/settings`."""

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
        env_prefix="WEATHER__",
        env_file=(".env", ".env.prod", ".env.dev"),
    )


settings = Settings()
