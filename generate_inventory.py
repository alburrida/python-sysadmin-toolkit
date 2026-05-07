import csv
import random
from pathlib import Path

from faker import Faker


fake = Faker("es_ES")


OPERATING_SYSTEMS: list[str] = [
    "Windows Server 2012",
    "Windows Server 2016",
    "Windows Server 2019",
    "Windows Server 2022",
    "Ubuntu Server 22.04",
    "Ubuntu Server 24.04",
    "Debian 12",
    "Rocky Linux 9",
]

DEPARTMENTS: list[str] = [
    "IT",
    "Finance",
    "HR",
    "Operations",
    "Security",
    "Development",
    "Management",
]

ENVIRONMENTS: list[str] = [
    "production",
    "staging",
    "testing",
    "development",
]

RAM_OPTIONS: list[int] = [2, 4, 8, 16, 32, 64]
CPU_OPTIONS: list[int] = [2, 4, 8, 16]


def generate_private_ip() -> str:
    return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def generate_inventory(output_path: str = "data/inventory.csv", rows: int = 1000) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fieldnames: list[str] = [
        "hostname",
        "ip",
        "mac",
        "operating_system",
        "ram_gb",
        "cpu_cores",
        "department",
        "environment",
        "owner",
    ]

    with open(output_path, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for index in range(1, rows + 1):
            department: str = random.choice(DEPARTMENTS)

            writer.writerow(
                {
                    "hostname": f"srv-{department.lower()}-{index:04d}",
                    "ip": generate_private_ip(),
                    "mac": fake.mac_address(),
                    "operating_system": random.choice(OPERATING_SYSTEMS),
                    "ram_gb": random.choice(RAM_OPTIONS),
                    "cpu_cores": random.choice(CPU_OPTIONS),
                    "department": department,
                    "environment": random.choice(ENVIRONMENTS),
                    "owner": fake.name(),
                }
            )

    print(f"Inventario generado correctamente en {output_path}")
    print(f"Filas generadas: {rows}")


if __name__ == "__main__":
    generate_inventory()
