# Redes en Docker

## Tipos de red nativos en Docker

Docker incluye varios tipos de red. Los más importantes son `bridge`, `host` y `none`.

## Red bridge

La red `bridge` es el modo por defecto cuando se crea un contenedor sin indicar una red concreta.

En este modo, Docker crea una red virtual interna. Los contenedores conectados a esa red reciben una IP privada y pueden comunicarse entre ellos si están en la misma red.

Cuando se publica un puerto con `-p`, Docker redirige tráfico desde el host hacia el contenedor.

Ejemplo:

```bash
docker run -d --name sysadmin-api -p 8000:8000 python-sysadmin-toolkit:1.1
```

Aquí el puerto `8000` del host se redirige al puerto `8000` del contenedor.

La red `bridge` es adecuada para la mayoría de aplicaciones multicontenedor, especialmente cuando se usa Docker Compose.

## Red host

En la red `host`, el contenedor no tiene una red virtual separada. Usa directamente la red del host.

Esto elimina parte del aislamiento de red, pero puede mejorar el rendimiento en casos concretos.

Ejemplo conceptual:

```bash
docker run --network host imagen
```

En este modo, si la aplicación escucha en el puerto 8000, lo hará directamente en el puerto 8000 del host.

No suele ser la opción más segura para servicios normales porque reduce el aislamiento entre host y contenedor.

## Red none

En la red `none`, el contenedor no tiene conectividad de red externa.

Ejemplo conceptual:

```bash
docker run --network none imagen
```

Este modo puede usarse cuando un contenedor no necesita acceso a red o cuando se quiere aislar completamente por motivos de seguridad.

## Service discovery en Docker Compose

Docker Compose permite que los servicios se encuentren entre sí usando el nombre del servicio como hostname.

Por ejemplo, si en `docker-compose.yml` existe un servicio llamado `redis`, el backend puede conectarse a Redis usando:

```text
redis
```

como nombre de host.

No hace falta saber la IP interna del contenedor. Docker Compose gestiona la resolución DNS interna dentro de la red del proyecto.

Ejemplo:

```python
redis_host = "redis"
```

Esto es muy importante porque las IPs internas de los contenedores pueden cambiar al recrearse, pero el nombre del servicio se mantiene.

## Puerto publicado frente a puerto interno

Un puerto publicado es accesible desde el host o desde fuera del host si el firewall lo permite.

Ejemplo:

```yaml
ports:
  - "8000:8000"
```

Esto publica el puerto `8000` del contenedor en el puerto `8000` del host.

Un puerto expuesto solo internamente no se publica hacia fuera. Otros contenedores de la misma red pueden acceder, pero el host no lo expone directamente.

Ejemplo:

```yaml
expose:
  - "8000"
```

## Diferencia de seguridad

Publicar un puerto aumenta la superficie de exposición. Cualquier servicio publicado puede recibir conexiones desde fuera del contenedor.

En una arquitectura más segura, el backend no debería publicar su puerto directamente. Lo recomendable es que solo NGINX publique los puertos `80` o `443`, y que el backend quede accesible únicamente dentro de la red interna de Docker.

Estructura recomendada:

```text
Usuario/Navegador
      |
      v
Puerto 80/443 del host
      |
      v
Contenedor NGINX
      |
      v
Red interna Docker
      |
      v
Contenedor backend FastAPI
      |
      v
Contenedor Redis
```

De esta forma, Redis y el backend no quedan expuestos directamente al exterior.

## Evidencias generadas

Listado de redes:

```text
docs/docker-network-ls.txt
```

Inspección de la red bridge:

```text
docs/docker-bridge-inspect.json
```

## Red bridge personalizada

Además de la red `bridge` por defecto, se ha creado una red personalizada para comprobar su funcionamiento:

```bash
docker network create sysadmin-test-net
docker network inspect sysadmin-test-net
docker network rm sysadmin-test-net
```

Las redes personalizadas son recomendables porque permiten aislar servicios por proyecto y facilitan el descubrimiento de servicios por nombre cuando se trabaja con Docker Compose.

La inspección de esta red se guardó en:

```text
docs/docker-custom-network-inspect.json
```
