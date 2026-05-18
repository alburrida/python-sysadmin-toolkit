# Variables de entorno y archivos de entorno

## Objetivo

La configuración sensible y dependiente del entorno se ha separado del código fuente usando variables de entorno.

Esto permite usar diferentes configuraciones en desarrollo, pruebas o producción sin modificar el código de la aplicación.

## Archivo .env

El archivo `.env` contiene la configuración real usada en local:

```text
APP_ENV=development
STORAGE_DIR=/app/storage
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_dev_password_123
```

Este archivo no debe subirse a GitHub porque puede contener secretos.

Por ese motivo está incluido en `.gitignore`.

## Archivo .env.example

El archivo `.env.example` sirve como plantilla segura:

```text
APP_ENV=development
STORAGE_DIR=/app/storage
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=change_me
```

Este archivo sí se sube al repositorio para que otra persona sepa qué variables necesita definir.

## Uso en Docker Compose

El servicio backend lee el archivo `.env` mediante:

```yaml
env_file:
  - .env
```

Redis usa la contraseña definida en la variable `REDIS_PASSWORD`:

```yaml
command: redis-server --requirepass ${REDIS_PASSWORD}
```

## Uso en Python

La aplicación lee las variables desde el módulo `app_config.py`.

Variables usadas:

```text
APP_ENV
STORAGE_DIR
REDIS_HOST
REDIS_PORT
REDIS_PASSWORD
```

La API expone el endpoint:

```http
GET /runtime-config
```

Este endpoint muestra la configuración activa, pero enmascara la contraseña de Redis para no exponer secretos.

## Por qué no se deben incluir secretos en Dockerfile o Compose

No deben escribirse secretos directamente dentro de un `Dockerfile` porque pueden quedar almacenados en las capas de la imagen.

Tampoco es recomendable escribir contraseñas directamente en `docker-compose.yml`, porque el archivo suele subirse al repositorio.

La forma correcta es usar variables de entorno, archivos `.env` ignorados por Git o gestores de secretos específicos en entornos de producción.

## Advertencia sobre redis-cli

Durante las pruebas se usó:

```bash
docker compose exec redis redis-cli -a redis_dev_password_123 ping
```

Redis mostró una advertencia indicando que pasar la contraseña por línea de comandos puede no ser seguro.

Para una práctica local es aceptable, pero en producción deben usarse métodos más seguros para gestionar credenciales.
