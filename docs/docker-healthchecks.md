# Healthchecks y dependencias entre servicios

## Objetivo

Se han añadido healthchecks a los servicios principales de la infraestructura para comprobar automáticamente si están funcionando correctamente.

También se han configurado dependencias entre servicios para que cada contenedor espere a que el servicio necesario esté saludable antes de arrancar.

## Healthcheck de Redis

Redis usa `redis-cli` para comprobar si responde correctamente:

```yaml
healthcheck:
  test: ["CMD-SHELL", "redis-cli -a $$REDIS_PASSWORD ping | grep PONG"]
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 10s
```

El resultado esperado es:

```text
PONG
```

Para que el healthcheck pueda leer la contraseña, el servicio Redis también carga el archivo `.env`.

## Dependencia del backend respecto a Redis

El backend depende de Redis:

```yaml
depends_on:
  redis:
    condition: service_healthy
```

Esto evita que la API arranque antes de que Redis esté disponible.

## Healthcheck del backend

El backend comprueba su endpoint interno `/health`:

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=3)"]
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 15s
```

Se usa Python porque ya está disponible dentro de la imagen del backend.

## Dependencia del proxy respecto al backend

El proxy depende del backend:

```yaml
depends_on:
  backend:
    condition: service_healthy
```

Esto evita que NGINX arranque antes de que la API esté lista.

## Healthcheck del proxy

El proxy comprueba que NGINX tiene una configuración válida:

```yaml
healthcheck:
  test: ["CMD", "nginx", "-t"]
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 15s
```

## Por qué son importantes los healthchecks

Los healthchecks son importantes en producción porque permiten detectar automáticamente si un servicio está caído, bloqueado o no responde correctamente.

Evitan problemas como:

- Arrancar un backend antes de que la base de datos esté lista.
- Enviar tráfico a un servicio que todavía no responde.
- Dar por iniciado un contenedor cuyo proceso existe, pero cuya aplicación está fallando.
- Dificultar el diagnóstico cuando varios servicios dependen unos de otros.

## Evidencias

Estado de Compose con healthchecks:

```text
docs/docker-healthchecks-ps.txt
```

Inspecciones completas:

```text
docs/docker-healthcheck-redis-inspect.json
docs/docker-healthcheck-backend-inspect.json
docs/docker-healthcheck-proxy-inspect.json
```
