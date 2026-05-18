import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app_config import load_config, mask_secret
from inventory_manager import filter_vulnerable_servers, load_inventory
from log_parser import parse_failed_ssh_attempts
from redis_utils import (
    add_suspicious_ip,
    get_cached_json,
    list_suspicious_ips,
    redis_ping,
    set_cached_json,
)


config = load_config()

INVENTORY_PATH = "data/inventory.csv"
AUTH_LOG_PATH = "data/auth.log"
STORAGE_DIR = Path(config.storage_dir)
STORAGE_FILE = STORAGE_DIR / "entries.jsonl"

app = FastAPI(
    title="Python Sysadmin Toolkit API",
    description="API REST para exponer funciones del toolkit de administración de sistemas.",
    version="1.0.4",
)


class StorageEntryCreate(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    source: str = Field(default="api", min_length=1, max_length=100)


class StorageEntry(StorageEntryCreate):
    id: int
    created_at: str


def normalize_limit(limit: int) -> int:
    if limit < 1:
        return 1

    if limit > 100:
        return 100

    return limit


def ensure_storage_dir() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def read_storage_entries() -> list[dict[str, Any]]:
    ensure_storage_dir()

    if not STORAGE_FILE.exists():
        return []

    entries: list[dict[str, Any]] = []

    with open(STORAGE_FILE, "r", encoding="utf-8") as storage_file:
        for line in storage_file:
            clean_line = line.strip()

            if not clean_line:
                continue

            entries.append(cast(dict[str, Any], json.loads(clean_line)))

    return entries


def append_storage_entry(entry_data: StorageEntryCreate) -> StorageEntry:
    entries = read_storage_entries()

    new_entry = StorageEntry(
        id=len(entries) + 1,
        message=entry_data.message,
        source=entry_data.source,
        created_at=datetime.now(UTC).isoformat(),
    )

    ensure_storage_dir()

    with open(STORAGE_FILE, "a", encoding="utf-8") as storage_file:
        storage_file.write(json.dumps(new_entry.model_dump(), ensure_ascii=False) + "\n")

    return new_entry


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "python-sysadmin-toolkit",
        "environment": config.app_env,
    }


@app.get("/runtime-config")
def get_runtime_config() -> dict[str, str | int]:
    return {
        "app_env": config.app_env,
        "storage_dir": config.storage_dir,
        "redis_host": config.redis_host,
        "redis_port": config.redis_port,
        "redis_password": mask_secret(config.redis_password),
    }


@app.get("/redis/health")
def get_redis_health() -> dict[str, str]:
    if redis_ping():
        return {
            "status": "ok",
            "redis": "connected",
        }

    return {
        "status": "error",
        "redis": "not_connected",
    }


@app.get("/inventory")
def get_inventory(limit: int = 20) -> dict[str, Any]:
    safe_limit: int = normalize_limit(limit)

    try:
        inventory = load_inventory(INVENTORY_PATH)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    records = cast(
        list[dict[str, Any]],
        inventory.head(safe_limit).to_dict(orient="records"),
    )

    return {
        "total_servers": len(inventory),
        "limit": safe_limit,
        "items": records,
    }


@app.get("/inventory/vulnerable")
def get_vulnerable_inventory(limit: int = 20) -> dict[str, Any]:
    safe_limit: int = normalize_limit(limit)

    try:
        inventory = load_inventory(INVENTORY_PATH)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    vulnerable_servers = filter_vulnerable_servers(inventory)

    records = cast(
        list[dict[str, Any]],
        vulnerable_servers.head(safe_limit).to_dict(orient="records"),
    )

    return {
        "total_vulnerable_servers": len(vulnerable_servers),
        "limit": safe_limit,
        "items": records,
    }


@app.get("/ssh/failed-ips")
def get_failed_ssh_ips() -> dict[str, Any]:
    unique_ips, failed_ip_counts = parse_failed_ssh_attempts(AUTH_LOG_PATH)

    return {
        "unique_ip_count": len(unique_ips),
        "failed_ip_counts": failed_ip_counts,
    }


@app.get("/ssh/failed-ips/cache")
def get_failed_ssh_ips_cached() -> dict[str, Any]:
    cache_key = "cache:ssh_failed_ips"
    cached_data = get_cached_json(cache_key)

    if cached_data is not None:
        cached_data["cache"] = "hit"
        return cached_data

    unique_ips, failed_ip_counts = parse_failed_ssh_attempts(AUTH_LOG_PATH)

    data: dict[str, Any] = {
        "unique_ip_count": len(unique_ips),
        "failed_ip_counts": failed_ip_counts,
        "cache": "miss",
    }

    set_cached_json(cache_key, data, ttl_seconds=300)

    return data


@app.post("/redis/suspicious-ips/{ip}")
def report_suspicious_ip(ip: str) -> dict[str, Any]:
    created = add_suspicious_ip(ip)

    return {
        "ip": ip,
        "stored": True,
        "new_entry": created,
    }


@app.get("/redis/suspicious-ips")
def get_suspicious_ips() -> dict[str, Any]:
    ips = list_suspicious_ips()

    return {
        "total": len(ips),
        "items": ips,
    }


@app.post("/storage/entries")
def create_storage_entry(entry_data: StorageEntryCreate) -> StorageEntry:
    return append_storage_entry(entry_data)


@app.get("/storage/entries")
def list_storage_entries() -> dict[str, Any]:
    entries = read_storage_entries()

    return {
        "total_entries": len(entries),
        "storage_file": str(STORAGE_FILE),
        "items": entries,
    }
