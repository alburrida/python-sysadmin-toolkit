# Python Sysadmin Toolkit

Kit de herramientas para administración de sistemas desarrollado en Python.

El proyecto incluye automatización básica del sistema operativo, análisis de logs SSH, modelado de dispositivos de red con programación orientada a objetos, consulta de inteligencia de amenazas mediante API externa, procesamiento masivo de inventarios con Pandas, generación de informes Excel y pruebas unitarias con pytest.

## Tecnologías utilizadas

- Python 3
- Pandas
- OpenPyXL
- Requests
- Faker
- Pytest
- Schedule
- Mypy
- Subprocess
- Shutil

## Estructura del proyecto

```text
.
├── data
│   ├── auth.log
│   └── inventory.csv
├── docs
│   ├── pytest-output.txt
│   └── python-sysadmin.md
├── generate_inventory.py
├── inventory_manager.py
├── log_parser.py
├── network_models.py
├── os_utils.py
├── report_generator.py
├── reports
│   └── inventory_report_2026_05.xlsx
├── scheduler_daemon.py
├── sys_toolkit.py
├── tests
│   └── test_toolkit.py
└── threat_intel.py
```

## Instalación

Crear entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Uso principal

Ejecutar el menú interactivo:

```bash
python sys_toolkit.py
```

Opciones disponibles:

```text
1. Comprobar conectividad por ping
2. Comprobar espacio libre en disco
3. Analizar logs SSH
4. Auditar dispositivos de red
5. Consultar inteligencia de amenazas
6. Generar inventario CSV
7. Procesar inventario de red
8. Generar informe Excel
0. Salir
```

## Scripts principales

### os_utils.py

Contiene funciones para automatización del sistema operativo.

- `check_ping(ip)`: ejecuta un ping mediante `subprocess`.
- `get_disk_usage(path)`: obtiene uso de disco.
- `is_disk_space_low(path)`: detecta si queda menos del 20% libre.

### log_parser.py

Analiza logs SSH tipo `auth.log`.

Extrae IPs de intentos fallidos, elimina duplicados mediante `set` y cuenta intentos por IP con diccionarios.

### network_models.py

Define modelos de red usando programación orientada a objetos.

Incluye:

- `NetworkDevice`
- `Router`
- `Server`

Cada clase aplica su propia auditoría mediante polimorfismo.

### threat_intel.py

Consulta información externa de IPs sospechosas usando `requests` e IPinfo.

Muestra IP atacante, número de intentos, país y organización.

### generate_inventory.py

Genera un inventario ficticio con al menos 1000 servidores usando `csv`, `random` y `faker`.

### inventory_manager.py

Carga el inventario con Pandas, filtra servidores Windows Server o con menos de 4 GB de RAM y agrupa equipos por departamento.

### report_generator.py

Genera un informe Excel mensual en la carpeta `reports`.

Incluye hojas de resumen, servidores filtrados y conteo por departamento.

### scheduler_daemon.py

Ejecuta automáticamente la generación del informe Excel cada hora usando `schedule`.

## Pruebas

Ejecutar tests:

```bash
pytest
```

Salida documentada en:

```text
docs/pytest-output.txt
```

Resultado obtenido:

```text
4 passed
```

## Comprobación de tipos

Ejecutar mypy:

```bash
python -m mypy sys_toolkit.py os_utils.py log_parser.py network_models.py threat_intel.py generate_inventory.py inventory_manager.py report_generator.py scheduler_daemon.py tests/test_toolkit.py
```

Resultado obtenido:

```text
Success: no issues found in 10 source files
```

## Archivos generados

- `data/auth.log`: log SSH simulado.
- `data/inventory.csv`: inventario ficticio de servidores.
- `reports/inventory_report_2026_05.xlsx`: informe Excel generado.
- `docs/pytest-output.txt`: salida documentada de las pruebas unitarias.

## Autor

Práctica de automatización y análisis de redes con Python para administración de sistemas.
