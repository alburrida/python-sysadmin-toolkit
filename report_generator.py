from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from inventory_manager import (
    count_servers_by_department,
    filter_vulnerable_servers,
    load_inventory,
)


def build_summary_dataframe(
    inventory: DataFrame,
    vulnerable_servers: DataFrame,
    servers_by_department: DataFrame,
) -> DataFrame:
    summary_data: list[dict[str, str | int]] = [
        {
            "metric": "Total de servidores",
            "value": len(inventory),
        },
        {
            "metric": "Servidores vulnerables o antiguos",
            "value": len(vulnerable_servers),
        },
        {
            "metric": "Departamentos analizados",
            "value": len(servers_by_department),
        },
        {
            "metric": "Fecha de generación",
            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    ]

    return pd.DataFrame(summary_data)


def generate_excel_report(
    csv_path: str = "data/inventory.csv",
    output_dir: str = "reports",
) -> str:
    inventory: DataFrame = load_inventory(csv_path)
    vulnerable_servers: DataFrame = filter_vulnerable_servers(inventory)
    servers_by_department: DataFrame = count_servers_by_department(inventory)
    summary: DataFrame = build_summary_dataframe(
        inventory,
        vulnerable_servers,
        servers_by_department,
    )

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    current_month: str = datetime.now().strftime("%Y_%m")
    output_path: str = f"{output_dir}/inventory_report_{current_month}.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary.to_excel(
            writer,
            sheet_name="Resumen",
            index=False,
            freeze_panes=(1, 0),
        )

        vulnerable_servers.to_excel(
            writer,
            sheet_name="Servidores_filtrados",
            index=False,
            freeze_panes=(1, 0),
        )

        servers_by_department.to_excel(
            writer,
            sheet_name="Por_departamento",
            index=False,
            freeze_panes=(1, 0),
        )

    return output_path


def print_excel_report_result(csv_path: str = "data/inventory.csv") -> None:
    try:
        output_path: str = generate_excel_report(csv_path)
    except FileNotFoundError as error:
        print(error)
        return

    print("\n=== Informe Excel generado ===")
    print(f"Archivo origen: {csv_path}")
    print(f"Archivo generado: {output_path}")


if __name__ == "__main__":
    print_excel_report_result()
