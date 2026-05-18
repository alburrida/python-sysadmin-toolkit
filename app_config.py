import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    storage_dir: str
    redis_host: str
    redis_port: int
    redis_password: str


def load_config() -> AppConfig:
    redis_port_text: str = os.getenv("REDIS_PORT", "6379")

    try:
        redis_port = int(redis_port_text)
    except ValueError:
        redis_port = 6379

    return AppConfig(
        app_env=os.getenv("APP_ENV", "development"),
        storage_dir=os.getenv("STORAGE_DIR", "storage"),
        redis_host=os.getenv("REDIS_HOST", "redis"),
        redis_port=redis_port,
        redis_password=os.getenv("REDIS_PASSWORD", ""),
    )


def mask_secret(secret: str) -> str:
    if not secret:
        return "not_set"

    if len(secret) <= 4:
        return "****"

    return f"{secret[:2]}***{secret[-2:]}"
