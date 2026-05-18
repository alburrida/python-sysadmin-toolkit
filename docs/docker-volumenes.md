# Gestión de datos persistentes con volúmenes Docker

## Contenedores efímeros

Los contenedores Docker son efímeros. Esto significa que los cambios realizados dentro del sistema de archivos interno del contenedor se pierden si el contenedor se elimina y se crea uno nuevo desde la imagen original.

Para conservar datos se utilizan volúmenes o bind mounts.

## Modificación de la API

Se ha modificado la API FastAPI para guardar entradas en un archivo dentro del contenedor:

```text
/app/storage/entries.jsonl
```

Endpoints añadidos:

```http
POST /storage/entries
GET /storage/entries
```

El endpoint `POST /storage/entries` escribe una entrada en el archivo persistente.  
El endpoint `GET /storage/entries` lista las entradas almacenadas.

## Volumen nombrado

Se creó un volumen nombrado:

```bash
docker volume create sysadmin-api-storage
```

El contenedor se ejecutó montando ese volumen en `/app/storage`:

```bash
docker run -d \
  --name sysadmin-api \
  -p 8000:8000 \
  -v sysadmin-api-storage:/app/storage \
  python-sysadmin-toolkit:1.2
```

## Prueba de persistencia

Se creó una entrada con:

```bash
curl -X POST http://localhost:8000/storage/entries \
  -H "Content-Type: application/json" \
  -d '{"message":"Primera entrada persistente en volumen Docker","source":"curl"}'
```

Después se comprobó con:

```bash
curl http://localhost:8000/storage/entries
```

Luego se eliminó el contenedor:

```bash
docker rm -f sysadmin-api
```

Y se recreó usando el mismo volumen:

```bash
docker run -d \
  --name sysadmin-api \
  -p 8000:8000 \
  -v sysadmin-api-storage:/app/storage \
  python-sysadmin-toolkit:1.2
```

Al consultar de nuevo:

```bash
curl http://localhost:8000/storage/entries
```

la entrada seguía existiendo. Esto demuestra que los datos no estaban guardados en el contenedor, sino en el volumen Docker.

## Volumen nombrado frente a bind mount

Un volumen nombrado está gestionado por Docker. Es útil para datos persistentes de aplicaciones y bases de datos, porque Docker decide su ubicación interna y facilita su administración con la CLI.

Un bind mount enlaza una ruta concreta del host con una ruta del contenedor. Es útil durante desarrollo, cuando se quiere editar código o archivos desde el sistema anfitrión y ver los cambios dentro del contenedor.

## Gestión de volúmenes con CLI

Comandos utilizados:

```bash
docker volume create sysadmin-api-storage
docker volume ls
docker volume inspect sysadmin-api-storage
```

La inspección del volumen se guardó en:

```text
docs/docker-volume-inspect.json
```
