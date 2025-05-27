import logging
from pathlib import Path

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
    session_type: str
    geolocator_user_agent: str
    cache: CacheSettings
    database_path: str
    logs_dir: str = Field(default="logs")
    debug: bool = Field(
        default=False, description="Enable debug mode for the application"
    )

    def __init__(self, **kwargs):
        """Инициализирует настройки и логирует содержимое файлов окружения.

        Args:
            **kwargs: Дополнительные параметры для передачи в BaseSettings.
        """
        super().__init__(**kwargs)
        logger.info("Loaded settings: %s", self.model_dump())
        for env_file in self.model_config["env_file"]:
            if Path(env_file).exists():
                with Path(env_file).open("r") as f:
                    logger.info("Content of %s:\n%s", env_file, f.read())
            else:
                logger.warning("File %s not found", env_file)

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
        # env_nested_delimiter="__",
        env_prefix="WEATHER__",
        env_file=(".env", ".env.dev"),
    )


settings = Settings()
