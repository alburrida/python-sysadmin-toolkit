import os
from dataclasses import dataclass
from typing import Any

import requests

from log_parser import parse_failed_ssh_attempts


@dataclass
class ThreatIntelResult:
    ip: str
    attempts: int
    country: str
    organization: str


def get_ip_info(ip: str) -> tuple[str, str]:
    """
    Consulta información básica de una IP usando IPinfo.

    Si existe la variable de entorno IPINFO_TOKEN, usa la API Lite oficial.
    Si no existe, intenta usar el endpoint clásico de ipinfo.io.
    """
    token: str | None = os.getenv("IPINFO_TOKEN")

    try:
        if token:
            url: str = f"https://api.ipinfo.io/lite/{ip}"
            response = requests.get(
                url,
                params={"token": token},
                timeout=5,
            )
        else:
            url = f"https://ipinfo.io/{ip}/json"
            response = requests.get(url, timeout=5)

        response.raise_for_status()

        data: dict[str, Any] = response.json()

        country: str = str(
            data.get("country")
            or data.get("country_code")
            or "Desconocido"
        )

        organization: str = str(
            data.get("as_name")
            or data.get("org")
            or data.get("asn")
            or "Desconocida"
        )

        return country, organization

    except requests.RequestException as error:
        print(f"Error consultando la IP {ip}: {error}")
        return "Error API", "Error API"


def build_threat_report(log_path: str) -> list[ThreatIntelResult]:
    """
    Genera una lista con IP, intentos fallidos, país y organización.
    """
    _, failed_ip_counts = parse_failed_ssh_attempts(log_path)

    report: list[ThreatIntelResult] = []

    for ip, attempts in failed_ip_counts.items():
        country, organization = get_ip_info(ip)

        report.append(
            ThreatIntelResult(
                ip=ip,
                attempts=attempts,
                country=country,
                organization=organization,
            )
        )

    return sorted(report, key=lambda item: item.attempts, reverse=True)


def print_threat_report(log_path: str) -> None:
    """
    Muestra una tabla simple con inteligencia básica de IPs sospechosas.
    """
    report: list[ThreatIntelResult] = build_threat_report(log_path)

    if not report:
        print("No hay IPs sospechosas para consultar.")
        return

    print("\n=== Informe de inteligencia de amenazas ===")
    print(f"Archivo analizado: {log_path}")
    print()
    print(f"{'IP atacante':<18} {'Intentos':<10} {'País':<20} {'Organización'}")
    print("-" * 80)

    for item in report:
        print(
            f"{item.ip:<18} "
            f"{item.attempts:<10} "
            f"{item.country:<20} "
            f"{item.organization}"
        )
