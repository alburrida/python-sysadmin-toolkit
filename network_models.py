from dataclasses import dataclass


@dataclass
class NetworkDevice:
    hostname: str
    ip: str
    mac: str

    def audit_device(self) -> list[str]:
        return [
            "Comprobar que el dispositivo está inventariado.",
            "Verificar que la IP y la MAC coinciden con el inventario.",
            "Revisar que no existan servicios innecesarios expuestos.",
        ]


@dataclass
class Router(NetworkDevice):
    routing_protocol: str
    firmware_version: str

    def audit_device(self) -> list[str]:
        return [
            "Cambiar credenciales por defecto del router.",
            "Comprobar que el firmware está actualizado.",
            "Desactivar administración remota si no es necesaria.",
            "Revisar reglas de firewall y NAT.",
            f"Verificar configuración del protocolo de routing: {self.routing_protocol}.",
        ]


@dataclass
class Server(NetworkDevice):
    operating_system: str
    critical_service: str

    def audit_device(self) -> list[str]:
        return [
            "Comprobar actualizaciones de seguridad del sistema.",
            "Revisar usuarios con privilegios administrativos.",
            "Verificar que el servicio crítico está monitorizado.",
            "Comprobar logs de acceso y errores.",
            f"Validar hardening básico para {self.operating_system}.",
        ]


def print_device_audit(device: NetworkDevice) -> None:
    print("\n=== Auditoría de dispositivo ===")
    print(f"Hostname: {device.hostname}")
    print(f"IP: {device.ip}")
    print(f"MAC: {device.mac}")
    print("\nDirectrices de seguridad:")

    for index, guideline in enumerate(device.audit_device(), start=1):
        print(f"{index}. {guideline}")


def demo_network_audit() -> None:
    devices: list[NetworkDevice] = [
        Router(
            hostname="router-core-01",
            ip="192.168.56.1",
            mac="00:11:22:33:44:55",
            routing_protocol="OSPF",
            firmware_version="1.2.8",
        ),
        Server(
            hostname="srv-web-01",
            ip="192.168.56.20",
            mac="AA:BB:CC:DD:EE:01",
            operating_system="Ubuntu Server 24.04",
            critical_service="Nginx",
        ),
        Server(
            hostname="srv-db-01",
            ip="192.168.56.30",
            mac="AA:BB:CC:DD:EE:02",
            operating_system="Debian 12",
            critical_service="PostgreSQL",
        ),
    ]

    for device in devices:
        print_device_audit(device)
