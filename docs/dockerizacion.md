# Dockerización del toolkit Python

## Objetivo

El toolkit de administración se ha convertido en una API REST con FastAPI y se ha dockerizado para poder ejecutarlo como un contenedor reproducible.

## Archivos creados

```text
Dockerfile
.dockerignore
api_main.py
```

## Dockerfile

El Dockerfile usa la imagen base oficial:

```Dockerfile
FROM python:3.11-alpine
```

Se utiliza Alpine porque es una imagen ligera, adecuada para reducir el tamaño final del contenedor.

El directorio de trabajo se define con:

```Dockerfile
WORKDIR /app
```

Primero se copia `requirements.txt`:

```Dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

Esto permite aprovechar la caché de Docker. Si cambia el código pero no cambian las dependencias, Docker no necesita reinstalar todos los paquetes.

Después se copia el resto del proyecto:

```Dockerfile
COPY . .
```

La API escucha internamente en el puerto 8000:

```Dockerfile
EXPOSE 8000
```

El comando de arranque ejecuta Uvicorn:

```Dockerfile
CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## .dockerignore

El archivo `.dockerignore` evita copiar al contexto de build archivos innecesarios o sensibles.

Entradas importantes:

```text
venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.git/
.env
reports/*.xlsx
docs/
tests/
```

Esto reduce el tamaño del contexto de build, evita subir secretos y mejora la limpieza de la imagen.

## Build de la imagen

La imagen se construye con:

```bash
docker build -t python-sysadmin-toolkit:1.0 .
```

## Ejecución del contenedor

El contenedor se ejecuta con:

```bash
docker run -d --name sysadmin-api -p 8000:8000 python-sysadmin-toolkit:1.0
```

El puerto 8000 del host queda conectado con el puerto 8000 del contenedor.

## Prueba de endpoints

Estado del servicio:

```bash
curl http://localhost:8000/health
```

Inventario:

```bash
curl "http://localhost:8000/inventory?limit=3"
```

Servidores vulnerables:

```bash
curl "http://localhost:8000/inventory/vulnerable?limit=3"
```

IPs SSH fallidas:

```bash
curl http://localhost:8000/ssh/failed-ips
```

## Swagger UI

FastAPI genera documentación automática en:

```text
http://localhost:8000/docs
```

## Análisis de capas

Las capas de la imagen se analizan con:

```bash
docker history python-sysadmin-toolkit:1.0
```

La salida se ha guardado en:

```text
docs/docker-image-history.txt
```

## Optimización

La imagen puede optimizarse usando `.dockerignore`, copiando primero `requirements.txt`, usando `--no-cache-dir` en pip y empleando una imagen base ligera como Alpine.

En proyectos más grandes también se podría separar un archivo de dependencias de producción para evitar instalar herramientas de desarrollo como `pytest`, `mypy` o stubs de tipado dentro de la imagen final.

## Verificación de ejecución real en Docker

Se comprobó que la API estaba respondiendo desde el contenedor y no desde Uvicorn local.

```bash
docker ps
```

Salida relevante:

```text
sysadmin-api   python-sysadmin-toolkit:1.0   0.0.0.0:8000->8000/tcp
```

Prueba del endpoint de salud:

```bash
curl http://localhost:8000/health
```

Resultado:

```json
{"status":"ok","service":"python-sysadmin-toolkit"}
```

