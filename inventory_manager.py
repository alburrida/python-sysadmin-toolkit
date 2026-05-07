from pathlib import Path

import pandas as pd
from pandas import DataFrame


def load_inventory(csv_path: str = "data/inventory.csv") -> DataFrame:
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"No existe el inventario: {csv_path}")

    return pd.read_csv(csv_path)


def filter_vulnerable_servers(inventory: DataFrame) -> DataFrame:
    windows_filter = inventory["operating_system"].str.contains(
        "Windows Server",
        case=False,
        na=False,
    )

    low_ram_filter = inventory["ram_gb"] < 4

    return inventory[windows_filter | low_ram_filter]


def count_servers_by_department(inventory: DataFrame) -> DataFrame:
    grouped = (
        inventory.groupby("department")
        .size()
        .reset_index(name="server_count")
        .sort_values(by="server_count", ascending=False)
    )

    return grouped


def print_inventory_summary(csv_path: str = "data/inventory.csv") -> None:
    try:
        inventory: DataFrame = load_inventory(csv_path)
    except FileNotFoundError as error:
        print(error)
        return

    vulnerable_servers: DataFrame = filter_vulnerable_servers(inventory)
    servers_by_department: DataFrame = count_servers_by_department(inventory)

    print("\n=== Resumen de inventario de red ===")
    print(f"Archivo cargado: {csv_path}")
    print(f"Total de servidores: {len(inventory)}")
    print(f"Servidores vulnerables o antiguos: {len(vulnerable_servers)}")

    print("\n=== Primeros servidores filtrados ===")
    print(
        vulnerable_servers[
            [
                "hostname",
                "ip",
                "operating_system",
                "ram_gb",
                "department",
                "environment",
            ]
        ]
        .head(15)
        .to_string(index=False)
    )

    print("\n=== Servidores por departamento ===")
    print(servers_by_department.to_string(index=False))


if __name__ == "__main__":
    print_inventory_summary()
