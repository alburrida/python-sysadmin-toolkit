from typing import Callable

from generate_inventory import generate_inventory
from inventory_manager import print_inventory_summary
from log_parser import print_failed_ssh_report
from network_models import demo_network_audit
from os_utils import check_ping, get_disk_usage, is_disk_space_low
from report_generator import print_excel_report_result
from threat_intel import print_threat_report


def show_menu() -> None:
    print("\n=== Python Sysadmin Toolkit ===")
    print("1. Comprobar conectividad por ping")
    print("2. Comprobar espacio libre en disco")
    print("3. Analizar logs SSH")
    print("4. Auditar dispositivos de red")
    print("5. Consultar inteligencia de amenazas")
    print("6. Generar inventario CSV")
    print("7. Procesar inventario de red")
    print("8. Generar informe Excel")
    print("0. Salir")


def run_ping_check() -> None:
    ip: str = input("Introduce una IP o dominio: ").strip()

    if not ip:
        print("No has introducido ninguna IP o dominio.")
        return

    if check_ping(ip):
        print(f"{ip} responde correctamente.")
    else:
        print(f"{ip} no responde o no es accesible.")


def run_disk_check() -> None:
    path: str = input("Introduce la ruta a comprobar [/]: ").strip()

    if not path:
        path = "/"

    total_gb, used_gb, free_gb, free_percent = get_disk_usage(path)

    print(f"\nRuta analizada: {path}")
    print(f"Total: {total_gb:.2f} GB")
    print(f"Usado: {used_gb:.2f} GB")
    print(f"Libre: {free_gb:.2f} GB")
    print(f"Porcentaje libre: {free_percent:.2f}%")

    if is_disk_space_low(path):
        print("ALERTA: el espacio libre está por debajo del 20%.")
    else:
        print("Estado correcto: hay espacio suficiente.")


def run_log_analysis() -> None:
    file_path: str = input("Ruta del archivo auth.log [data/auth.log]: ").strip()

    if not file_path:
        file_path = "data/auth.log"

    print_failed_ssh_report(file_path)


def run_network_audit() -> None:
    demo_network_audit()


def run_threat_intel() -> None:
    file_path: str = input("Ruta del archivo auth.log [data/auth.log]: ").strip()

    if not file_path:
        file_path = "data/auth.log"

    print_threat_report(file_path)


def run_generate_inventory() -> None:
    rows_text: str = input("Número de servidores a generar [1000]: ").strip()

    if not rows_text:
        rows = 1000
    else:
        try:
            rows = int(rows_text)
        except ValueError:
            print("Número no válido. Se generarán 1000 servidores.")
            rows = 1000

    generate_inventory("data/inventory.csv", rows)


def run_inventory_processing() -> None:
    csv_path: str = input("Ruta del inventario CSV [data/inventory.csv]: ").strip()

    if not csv_path:
        csv_path = "data/inventory.csv"

    print_inventory_summary(csv_path)


def run_excel_report() -> None:
    csv_path: str = input("Ruta del inventario CSV [data/inventory.csv]: ").strip()

    if not csv_path:
        csv_path = "data/inventory.csv"

    print_excel_report_result(csv_path)


def exit_program() -> None:
    print("Saliendo del toolkit...")


def main() -> None:
    actions: dict[str, Callable[[], None]] = {
        "1": run_ping_check,
        "2": run_disk_check,
        "3": run_log_analysis,
        "4": run_network_audit,
        "5": run_threat_intel,
        "6": run_generate_inventory,
        "7": run_inventory_processing,
        "8": run_excel_report,
        "0": exit_program,
    }

    while True:
        show_menu()
        choice: str = input("Selecciona una opción: ").strip()

        action: Callable[[], None] | None = actions.get(choice)

        if action is None:
            print("Opción no válida.")
            continue

        action()

        if choice == "0":
            break


if __name__ == "__main__":
    main()
