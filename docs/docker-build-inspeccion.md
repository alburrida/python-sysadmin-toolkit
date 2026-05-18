# Build, ejecución e inspección de la imagen propia

## Construcción de la imagen

La imagen del backend se construyó con:

```bash
docker build -t python-sysadmin-toolkit:1.0 .
```

Posteriormente se realizó una segunda construcción tras un cambio menor en el código:

```bash
docker build --progress=plain -t python-sysadmin-toolkit:1.1 .
```

El objetivo era observar el comportamiento de la caché de Docker.

## Caché de Docker

Para aprovechar la caché se copió primero el archivo `requirements.txt` y se instalaron las dependencias antes de copiar el resto del código.

```Dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

Al modificar solo código Python y no cambiar `requirements.txt`, Docker puede reutilizar la capa de instalación de dependencias. Esto mejora el rendimiento del build.

La salida del build con caché se guardó en:

```text
docs/docker-build-cache-test.txt
```

## Ejecución de la imagen

La imagen se ejecutó con:

```bash
docker run -d --name sysadmin-api -p 8000:8000 python-sysadmin-toolkit:1.1
```

Esto publica el puerto `8000` del contenedor en el puerto `8000` del host.

## Prueba de endpoints

Endpoint de salud:

```bash
curl http://localhost:8000/health
```

Inventario:

```bash
curl "http://localhost:8000/inventory?limit=3"
```

IPs SSH fallidas:

```bash
curl http://localhost:8000/ssh/failed-ips
```

Swagger UI automático:

```text
http://localhost:8000/docs
```

## Tamaño de imagen

El tamaño de la imagen se comprobó con:

```bash
docker images python-sysadmin-toolkit
```

La salida se guardó en:

```text
docs/docker-image-size.txt
```

## Inspección de la imagen

La imagen se inspeccionó con:

```bash
docker image inspect python-sysadmin-toolkit:1.0
```

La salida JSON se guardó en:

```text
docs/docker-own-image-inspect.json
```

## Análisis de capas

Las capas se analizaron con:

```bash
docker history python-sysadmin-toolkit:1.0
```

La salida se guardó en:

```text
docs/docker-image-history.txt
```

## Técnicas de optimización

Para reducir el tamaño y mejorar el rendimiento de la imagen se han aplicado varias técnicas:

- Uso de imagen base ligera `python:3.11-alpine`.
- Uso de `.dockerignore` para excluir archivos innecesarios.
- Copia previa de `requirements.txt` para aprovechar la caché.
- Uso de `pip install --no-cache-dir` para evitar guardar cachés de instalación.
- Exclusión de carpetas como `venv/`, `.git/`, `docs/`, `tests/` y cachés de Python.

Una mejora adicional sería separar dependencias de desarrollo y producción, evitando instalar herramientas como `pytest`, `mypy` o `pandas-stubs` dentro de la imagen final.
