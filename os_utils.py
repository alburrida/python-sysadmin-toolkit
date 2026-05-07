import shutil
import subprocess


def check_ping(ip: str) -> bool:
    """
    Ejecuta un ping simple a una IP o dominio.
    Devuelve True si responde y False si falla.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

        return result.returncode == 0

    except FileNotFoundError:
        print("Error: el comando ping no está disponible en el sistema.")
        return False


def get_disk_usage(path: str) -> tuple[float, float, float, float]:
    """
    Devuelve el uso de disco de una ruta.

    Retorna:
    total_gb, used_gb, free_gb, free_percent
    """
    total, used, free = shutil.disk_usage(path)

    total_gb: float = total / (1024 ** 3)
    used_gb: float = used / (1024 ** 3)
    free_gb: float = free / (1024 ** 3)
    free_percent: float = (free / total) * 100

    return total_gb, used_gb, free_gb, free_percent


def is_disk_space_low(path: str, threshold_percent: float = 20.0) -> bool:
    """
    Devuelve True si el espacio libre está por debajo del porcentaje indicado.
    """
    try:
        _, _, _, free_percent = get_disk_usage(path)
        return free_percent < threshold_percent

    except FileNotFoundError:
        print(f"Error: la ruta {path} no existe.")
        return False
