# Docker Compose con backend y Redis

## Objetivo

Se ha sustituido la ejecución manual con `docker run` por una infraestructura definida en `docker-compose.yml`.

La infraestructura incluye:

```text
backend FastAPI
Redis
red bridge personalizada
volúmenes persistentes
variables de entorno
```

## Servicios definidos

### backend

El servicio `backend` construye la imagen desde el `Dockerfile` del proyecto.

```yaml
backend:
  build:
    context: .
    dockerfile: Dockerfile
```

El backend carga variables desde `.env`:

```yaml
env_file:
  - .env
```

También monta un volumen persistente:

```yaml
volumes:
  - backend_storage:/app/storage
```

Durante esta fase se publica el puerto `8000` para probar directamente la API:

```yaml
ports:
  - "8000:8000"
```

Más adelante, cuando se añada NGINX, este puerto se eliminará para que el backend solo sea accesible desde la red interna.

### redis

Redis se ejecuta con la imagen oficial:

```yaml
image: redis:7-alpine
```

Se configura contraseña mediante variable de entorno:

```yaml
command: redis-server --requirepass ${REDIS_PASSWORD}
```

Redis no publica puertos al host. Solo expone el puerto internamente:

```yaml
expose:
  - "6379"
```

Esto mejora la seguridad porque Redis queda accesible únicamente para otros servicios dentro de la red Docker.

## Red personalizada

Se ha creado una red bridge personalizada:

```yaml
networks:
  sysadmin_net:
    driver: bridge
```

Los servicios `backend` y `redis` están conectados a esta red.

## Service discovery

Docker Compose permite que los servicios se encuentren por nombre.

El backend puede localizar Redis usando:

```text
redis
```

como hostname.

Se comprobó con:

```bash
docker compose exec backend python -c "import socket; print(socket.gethostbyname('redis'))"
```

## Volúmenes

Se han definido dos volúmenes:

```yaml
volumes:
  backend_storage:
  redis_data:
```

`backend_storage` conserva los datos escritos por la API en `/app/storage`.

`redis_data` conserva los datos internos de Redis.

## Comandos utilizados

Levantar infraestructura:

```bash
docker compose up -d --build
```

Ver contenedores:

```bash
docker compose ps
```

Probar backend:

```bash
curl http://localhost:8000/health
```

Probar Redis:

```bash
docker compose exec redis redis-cli -a redis_dev_password_123 ping
```

Resultado esperado:

```text
PONG
```

## Seguridad

Redis no está publicado hacia el host mediante `ports`. Solo está disponible dentro de la red Docker. Esto reduce la superficie de exposición y evita que Redis quede accesible desde fuera de la infraestructura.
