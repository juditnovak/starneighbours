import logging
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "StarNeighbours"

    app_client_id: str | None = os.environ.get("GITHUB_CLIENT_ID")
    app_client_secret: str | None = os.environ.get("GITHUB_CLIENT_SECRET")

    cache_server: str = os.environ.get("REDIS_HOST", "localhost")
    cache_ttl: int = 3600
    log_level: int = logging.DEBUG


settings = Settings()


def auth_on() -> bool:
    return bool(settings.app_client_id) and bool(settings.app_client_secret)
