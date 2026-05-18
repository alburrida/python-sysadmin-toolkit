from __future__ import annotations

import json
from typing import Any, cast

import redis
from redis.exceptions import RedisError

from app_config import load_config


def get_redis_client() -> redis.Redis[str]:
    config = load_config()

    return redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password,
        decode_responses=True,
    )


def redis_ping() -> bool:
    try:
        client = get_redis_client()
        return bool(client.ping())
    except RedisError:
        return False


def get_cached_json(key: str) -> dict[str, Any] | None:
    try:
        client = get_redis_client()
        cached_value = client.get(key)

        if cached_value is None:
            return None

        return cast(dict[str, Any], json.loads(cached_value))

    except (RedisError, json.JSONDecodeError):
        return None


def set_cached_json(key: str, value: dict[str, Any], ttl_seconds: int = 300) -> None:
    try:
        client = get_redis_client()
        client.setex(key, ttl_seconds, json.dumps(value, ensure_ascii=False))
    except RedisError:
        return


def add_suspicious_ip(ip: str) -> bool:
    try:
        client = get_redis_client()
        result = client.sadd("suspicious_ips", ip)
        return bool(result)
    except RedisError:
        return False


def list_suspicious_ips() -> list[str]:
    try:
        client = get_redis_client()
        ips = client.smembers("suspicious_ips")
        return sorted(list(ips))
    except RedisError:
        return []
