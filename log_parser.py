from collections.abc import Iterable


def extract_ip_from_failed_line(line: str) -> str | None:
    """
    Extrae la IP de una línea de auth.log con intento SSH fallido.
    Devuelve None si la línea no es un fallo SSH válido.
    """
    clean_line: str = line.strip()

    if "Failed password" not in clean_line:
        return None

    parts: list[str] = clean_line.split()

    if "from" not in parts:
        return None

    from_index: int = parts.index("from")
    ip_index: int = from_index + 1

    if ip_index >= len(parts):
        return None

    return parts[ip_index]


def count_failed_ips(lines: Iterable[str]) -> dict[str, int]:
    """
    Cuenta cuántas veces aparece cada IP en intentos SSH fallidos.
    """
    failed_ips: dict[str, int] = {}

    for line in lines:
        ip: str | None = extract_ip_from_failed_line(line)

        if ip is None:
            continue

        failed_ips[ip] = failed_ips.get(ip, 0) + 1

    return failed_ips


def parse_failed_ssh_attempts(file_path: str) -> tuple[set[str], dict[str, int]]:
    """
    Lee un archivo auth.log línea a línea y devuelve:
    - un set con IPs únicas
    - un diccionario con el número de fallos por IP
    """
    try:
        with open(file_path, "r", encoding="utf-8") as log_file:
            failed_ip_counts: dict[str, int] = count_failed_ips(log_file)

    except FileNotFoundError:
        print(f"Error: no existe el archivo {file_path}.")
        return set(), {}

    unique_ips: set[str] = set(failed_ip_counts.keys())

    return unique_ips, failed_ip_counts


def print_failed_ssh_report(file_path: str) -> None:
    """
    Muestra por consola un resumen de IPs con intentos SSH fallidos.
    """
    unique_ips, failed_ip_counts = parse_failed_ssh_attempts(file_path)

    if not failed_ip_counts:
        print("No se han encontrado intentos SSH fallidos.")
        return

    print("\n=== Informe de intentos SSH fallidos ===")
    print(f"Archivo analizado: {file_path}")
    print(f"IPs únicas detectadas: {len(unique_ips)}")
    print("\nIP atacante          Intentos")
    print("-----------------------------")

    for ip, attempts in sorted(failed_ip_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"{ip:<20} {attempts}")
