from typing import Any, cast

from fastapi import FastAPI, HTTPException

from inventory_manager import filter_vulnerable_servers, load_inventory
from log_parser import parse_failed_ssh_attempts


INVENTORY_PATH = "data/inventory.csv"
AUTH_LOG_PATH = "data/auth.log"

app = FastAPI(
    title="Python Sysadmin Toolkit API",
    description="API REST para exponer funciones del toolkit de administración de sistemas.",
    version="1.0.0",
)


def normalize_limit(limit: int) -> int:
    if limit < 1:
        return 1

    if limit > 100:
        return 100

    return limit


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
