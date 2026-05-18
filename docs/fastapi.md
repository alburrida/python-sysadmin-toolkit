# API REST con FastAPI

Para poder dockerizar el toolkit y exponerlo como servicio web, se ha añadido una API REST sencilla usando FastAPI.

## Archivo principal

La API se encuentra en:

```text
api_main.py
```

## Endpoints disponibles

### Estado del servicio

```http
GET /health
```

Devuelve el estado básico de la aplicación.

### Inventario

```http
GET /inventory
```

Devuelve un resumen del inventario de servidores cargado desde `data/inventory.csv`.

Permite limitar resultados:

```http
GET /inventory?limit=3
```

### Inventario vulnerable

```http
GET /inventory/vulnerable
```

Devuelve servidores Windows Server o equipos con menos de 4 GB de RAM.

### IPs SSH fallidas

```http
GET /ssh/failed-ips
```

Devuelve las IPs detectadas en intentos SSH fallidos y el número de intentos por IP.

## Ejecución local

```bash
uvicorn api_main:app --host 0.0.0.0 --port 8000
```

## Swagger UI

FastAPI genera documentación automática en:

```text
http://localhost:8000/docs
```

## Motivo de uso

FastAPI permite convertir el toolkit de administración en un servicio web. Esto facilita su despliegue en Docker y su posterior exposición mediante NGINX como proxy inverso.
