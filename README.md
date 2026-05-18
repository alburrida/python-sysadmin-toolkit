# Python Sysadmin Toolkit Dockerizado

Kit de herramientas para administración de sistemas desarrollado en Python y dockerizado con Docker Compose.

El proyecto comenzó como un toolkit CLI para automatización de sistemas, análisis de logs SSH, procesamiento de inventarios y generación de informes Excel. Posteriormente se amplió con una API REST en FastAPI y una infraestructura basada en Docker Compose con Redis y NGINX como proxy inverso.

## Tecnologías utilizadas

- Python 3
- FastAPI
- Uvicorn
- Pandas
- OpenPyXL
- Requests
- Faker
- Redis
- Docker
- Docker Compose v2
- NGINX
- Pytest
- Mypy
- Schedule

## Arquitectura Docker

```text
Cliente / Navegador
        |
        | HTTP 80 / HTTPS 443
        v
+-------------------+
| NGINX Proxy       |
| sysadmin-proxy    |
+-------------------+
        |
        | Red interna Docker
        v
+-------------------+
| FastAPI Backend   |
| backend:8000      |
+-------------------+
        |
        | Red interna Docker
        v
+-------------------+
| Redis             |
| redis:6379        |
+-------------------+
```

El backend no publica el puerto `8000` directamente al host.  
Redis tampoco publica el puerto `6379`.  
El único punto de entrada público es NGINX mediante los puertos `80` y `443`.

## Servicios Docker Compose

El archivo `docker-compose.yml` define tres servicios:

```text
backend  -> API FastAPI del toolkit
redis    -> servicio Redis protegido con contraseña
proxy    -> NGINX como proxy inverso
```

También se definen:

```text
sysadmin_net     -> red bridge interna
backend_storage  -> volumen persistente de la API
redis_data       -> volumen persistente de Redis
```

## Estructura principal del proyecto

```text
.
├── api_main.py
├── app_config.py
├── redis_utils.py
├── Dockerfile
├── docker-compose.yml
├── nginx
│   ├── nginx.conf
│   └── certs
│       └── local.crt
├── static
│   └── status.txt
├── data
│   ├── auth.log
│   └── inventory.csv
├── docs
├── tests
├── requirements.txt
├── .env.example
└── README.md
```

## Variables de entorno

El proyecto usa un archivo `.env` local que no se sube a GitHub.

Crear el archivo desde la plantilla:

```bash
cp .env.example .env
```

Ejemplo:

```text
APP_ENV=development
STORAGE_DIR=/app/storage
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=change_me
```

El archivo `.env` está ignorado por Git para evitar subir secretos.

## Despliegue con Docker Compose

Levantar toda la infraestructura:

```bash
docker compose up -d --build
```

Ver estado de los servicios:

```bash
docker compose ps
```

Resultado esperado:

```text
backend   healthy
redis     healthy
proxy     healthy
```

Detener la infraestructura:

```bash
docker compose down
```

## Acceso a la aplicación

La aplicación se accede mediante NGINX.

Comprobar estado:

```bash
curl -k https://localhost/health
```

Comprobar Redis desde la API:

```bash
curl -k https://localhost/redis/health
```

Consultar inventario:

```bash
curl -k "https://localhost/inventory?limit=3"
```

Consultar servidores vulnerables:

```bash
curl -k "https://localhost/inventory/vulnerable?limit=3"
```

Consultar IPs fallidas SSH con caché Redis:

```bash
curl -k https://localhost/ssh/failed-ips/cache
```

Probar archivo estático servido por NGINX:

```bash
curl -k https://localhost/static/status.txt
```

## Swagger UI

FastAPI genera documentación automática en:

```text
https://localhost/docs
```

Al usar un certificado autofirmado local, el navegador puede mostrar una advertencia de seguridad. Es normal en esta práctica.

## Endpoints principales

```text
GET  /health
GET  /runtime-config
GET  /inventory
GET  /inventory/vulnerable
GET  /ssh/failed-ips
GET  /ssh/failed-ips/cache
GET  /redis/health
POST /redis/suspicious-ips/{ip}
GET  /redis/suspicious-ips
POST /storage/entries
GET  /storage/entries
```

## Redis

Redis se usa para:

- Comprobar conectividad desde el backend.
- Cachear el resultado del parseo de logs SSH.
- Guardar IPs sospechosas en un SET llamado `suspicious_ips`.

Comprobar Redis desde dentro del contenedor:

```bash
docker compose exec redis redis-cli -a redis_dev_password_123 ping
```

Listar IPs sospechosas almacenadas:

```bash
docker compose exec redis redis-cli -a redis_dev_password_123 SMEMBERS suspicious_ips
```

## Volúmenes

El proyecto usa volúmenes Docker para persistencia:

```text
backend_storage -> datos generados por la API
redis_data      -> datos internos de Redis
```

Esto permite conservar datos aunque los contenedores se eliminen y se vuelvan a crear.

## NGINX

NGINX actúa como proxy inverso.

Funciones configuradas:

- Publicación de puertos `80` y `443`.
- Redirección de HTTP a HTTPS.
- Proxy hacia el backend FastAPI.
- Cabeceras de proxy.
- Servicio de archivos estáticos.
- Rate limiting básico.
- Certificado autofirmado local.

La configuración está en:

```text
nginx/nginx.conf
```

## Healthchecks

Los tres servicios tienen healthchecks:

```text
redis   -> redis-cli ping
backend -> GET /health interno
proxy   -> nginx -t
```

Las dependencias están configuradas para que:

```text
backend espere a redis healthy
proxy espere a backend healthy
```

## Uso CLI del toolkit original

El proyecto conserva el menú interactivo original:

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

Funciones de automatización del sistema operativo:

- `check_ping(ip)`
- `get_disk_usage(path)`
- `is_disk_space_low(path)`

### log_parser.py

Analiza logs SSH tipo `auth.log`, extrae IPs de intentos fallidos, elimina duplicados con `set` y cuenta intentos por IP.

### network_models.py

Define modelos de red usando programación orientada a objetos:

- `NetworkDevice`
- `Router`
- `Server`

### threat_intel.py

Consulta información externa de IPs sospechosas usando `requests`.

### generate_inventory.py

Genera un inventario ficticio con servidores usando `csv`, `random` y `faker`.

### inventory_manager.py

Carga el inventario con Pandas, filtra servidores Windows Server o con menos de 4 GB de RAM y agrupa equipos por departamento.

### report_generator.py

Genera un informe Excel mensual en la carpeta `reports`.

### scheduler_daemon.py

Ejecuta automáticamente la generación del informe Excel cada hora usando `schedule`.

### api_main.py

Expone el toolkit mediante una API REST con FastAPI.

### redis_utils.py

Centraliza la conexión con Redis y las operaciones de caché y SET de IPs sospechosas.

## Comandos útiles de Docker

Levantar infraestructura:

```bash
docker compose up -d --build
```

Ver servicios:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f
```

Reiniciar backend:

```bash
docker compose restart backend
```

Reconstruir solo backend:

```bash
docker compose build backend
docker compose up -d backend
```

Escalar backend:

```bash
docker compose up -d --scale backend=2
```

Volver a una instancia:

```bash
docker compose up -d --scale backend=1
```

Ver consumo de recursos:

```bash
docker stats
```

Ver espacio usado por Docker:

```bash
docker system df
```

Limpieza segura sin borrar volúmenes:

```bash
docker system prune -f
```

## Pruebas unitarias

Ejecutar tests:

```bash
pytest
```

Resultado esperado:

```text
4 passed
```

## Comprobación de tipos

Ejecutar mypy:

```bash
python -m mypy sys_toolkit.py os_utils.py log_parser.py network_models.py threat_intel.py generate_inventory.py inventory_manager.py report_generator.py scheduler_daemon.py tests/test_toolkit.py api_main.py app_config.py redis_utils.py
```

Resultado esperado:

```text
Success: no issues found in 13 source files
```

## Documentación técnica

La carpeta `docs/` contiene la documentación técnica de la práctica:

```text
docker-teoria.md
docker-instalacion.md
docker-cli.md
dockerfile-capas.md
dockerizacion.md
docker-build-inspeccion.md
docker-redes.md
docker-volumenes.md
docker-compose.md
docker-env.md
nginx-teoria.md
nginx-configuracion.md
redis-integracion.md
docker-healthchecks.md
docker-gestion-avanzada.md
python-sysadmin.md
pytest-output.txt
```

También incluye evidencias de ejecución, inspecciones JSON, salidas de comandos y pruebas realizadas.

## Seguridad

El archivo `.env` no se sube al repositorio.

La clave privada del certificado local tampoco se sube:

```text
nginx/certs/*.key
```

Redis no publica el puerto `6379` al host.

El backend no publica el puerto `8000` al host.

El tráfico externo entra únicamente por NGINX.

## Entregable

El proyecto incluye:

- Dockerfile optimizado.
- Docker Compose con backend, Redis y NGINX.
- NGINX como proxy inverso.
- HTTPS local con certificado autofirmado.
- Rate limiting básico.
- Red interna Docker.
- Volúmenes persistentes.
- Variables de entorno con `.env.example`.
- Healthchecks.
- API REST con FastAPI.
- Redis como caché y almacenamiento de IPs sospechosas.
- Documentación técnica completa.
- README profesional.
