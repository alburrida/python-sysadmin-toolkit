import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from inventory_manager import filter_vulnerable_servers, load_inventory
from log_parser import parse_failed_ssh_attempts


INVENTORY_PATH = "data/inventory.csv"
AUTH_LOG_PATH = "data/auth.log"
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "storage"))
STORAGE_FILE = STORAGE_DIR / "entries.jsonl"

app = FastAPI(
    title="Python Sysadmin Toolkit API",
    description="API REST para exponer funciones del toolkit de administración de sistemas.",
    version="1.0.2",
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
