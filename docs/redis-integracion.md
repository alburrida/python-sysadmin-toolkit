# Integración con Redis: caché y almacenamiento

## Objetivo

Se ha integrado Redis con la API FastAPI para usarlo como sistema de caché y almacenamiento de IPs sospechosas.

Redis se ejecuta como servicio independiente dentro de Docker Compose y no expone su puerto al host.

## Cliente Redis en Python

Se ha instalado la librería cliente de Redis:

```text
redis
```

También se añadió soporte de tipos:

```text
types-redis
```

La conexión se centraliza en:

```text
redis_utils.py
```

## Conexión mediante service discovery

El backend se conecta a Redis usando el nombre del servicio de Docker Compose:

```text
redis
```

Este valor viene de la variable de entorno:

```text
REDIS_HOST=redis
```

Docker Compose resuelve ese nombre usando su DNS interno.

## Endpoint de estado Redis

Se ha añadido:

```http
GET /redis/health
```

Respuesta obtenida:

```json
{"status":"ok","redis":"connected"}
```

## Caché del parseo de logs

Se ha añadido un endpoint que usa Redis como caché para los resultados del parseo de logs SSH:

```http
GET /ssh/failed-ips/cache
```

Funcionamiento:

1. La API busca la clave `cache:ssh_failed_ips` en Redis.
2. Si existe, devuelve el resultado con `cache: hit`.
3. Si no existe, parsea `data/auth.log`, guarda el resultado en Redis y devuelve `cache: miss`.
4. La caché usa un TTL de 300 segundos.

## IPs sospechosas con SET de Redis

Se han añadido endpoints para reportar y listar IPs sospechosas:

```http
POST /redis/suspicious-ips/{ip}
GET /redis/suspicious-ips
```

Redis almacena estas IPs en un `SET` llamado:

```text
suspicious_ips
```

El uso de un SET evita duplicados automáticamente.

## Verificación con redis-cli

Se verificaron los datos entrando al contenedor Redis:

```bash
docker compose exec redis redis-cli -a redis_dev_password_123 SMEMBERS suspicious_ips
```

También se comprobó la clave de caché:

```bash
docker compose exec redis redis-cli -a redis_dev_password_123 GET cache:ssh_failed_ips
```

## Seguridad

Redis no publica el puerto 6379 al host. Solo está disponible dentro de la red interna de Docker Compose.

Esto evita exponer Redis directamente al exterior y obliga a que el acceso pase por el backend.
