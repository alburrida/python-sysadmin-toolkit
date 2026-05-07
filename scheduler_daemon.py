import time
from datetime import datetime

import schedule

from report_generator import generate_excel_report


def run_report_job() -> None:
    print(f"[{datetime.now()}] Ejecutando generación automática de informe...")

    try:
        output_path: str = generate_excel_report("data/inventory.csv")
        print(f"[{datetime.now()}] Informe generado correctamente: {output_path}")

    except FileNotFoundError as error:
        print(f"[{datetime.now()}] Error: {error}")


def main() -> None:
    print("Demonio iniciado. Generará un informe Excel cada hora.")
    print("Pulsa CTRL + C para detenerlo.")

    schedule.every().hour.do(run_report_job)

    run_report_job()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
