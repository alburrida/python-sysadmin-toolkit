# Comandos esenciales de Docker CLI

Este documento recoge las pruebas realizadas con imágenes, contenedores, logs, inspección, ejecución de comandos internos y persistencia de cambios dentro de contenedores.


## Gestión de imágenes

Se ha descargado la imagen `nginx:alpine` desde el registro de Docker.

```bash
docker pull nginx:alpine
docker images nginx
docker image inspect nginx:alpine
```
La imagen se ha inspeccionado y la salida JSON completa se ha guardado en:

docs/docker-nginx-image-inspect.json


## Contenedor NGINX en segundo plano

Se ha iniciado un contenedor NGINX en segundo plano, publicando el puerto `8080` del host contra el puerto `80` del contenedor.

```bash
docker run -d --name sysadmin-nginx -p 8080:80 nginx:alpine
docker ps
curl -I http://localhost:8080
```

El parámetro `-d` ejecuta el contenedor en segundo plano. El parámetro `-p 8080:80` publica el puerto 80 interno del contenedor en el puerto 8080 del host.


## Logs del contenedor

Los logs del contenedor se han revisado con:

```bash
docker logs sysadmin-nginx
timeout 5 docker logs -f sysadmin-nginx
```

La opción `-f` permite seguir los logs en tiempo real. En la práctica se ha usado `timeout 5` para cortar el seguimiento automáticamente después de unos segundos.


## Inspección del contenedor

Se ha inspeccionado el contenedor con:

```bash
docker inspect sysadmin-nginx
```

La salida JSON completa se ha guardado en:

```text
docs/docker-nginx-container-inspect.json
```

También se han extraído datos concretos:

```bash
docker inspect -f '{{.State.Status}}' sysadmin-nginx
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' sysadmin-nginx
docker inspect -f '{{json .NetworkSettings.Ports}}' sysadmin-nginx
```

Con esto se puede comprobar el estado, la IP interna del contenedor y los puertos publicados.


## docker exec dentro del contenedor

Se ha ejecutado un comando dentro del contenedor con:

```bash
docker exec sysadmin-nginx sh -c "which curl || true"
docker exec sysadmin-nginx sh -c "apk add --no-cache curl && curl --version"
```

Esto demuestra que `docker exec` permite ejecutar comandos dentro de un contenedor en ejecución.

La utilidad `curl` se instala dentro del sistema de archivos del contenedor actual, pero no se incorpora a la imagen original. Si el contenedor se elimina y se recrea desde la misma imagen, ese cambio desaparece.


## Gestión del ciclo de vida de contenedores

Se han practicado los comandos principales de gestión:

```bash
docker stop sysadmin-nginx
docker ps
docker ps -a
docker start sysadmin-nginx
docker restart sysadmin-nginx
docker ps
```

`docker ps` muestra los contenedores en ejecución.  
`docker ps -a` muestra también los contenedores detenidos.  
`docker stop` detiene el contenedor.  
`docker start` vuelve a arrancarlo.  
`docker restart` reinicia el contenedor.


## Prueba de no persistencia tras recrear el contenedor

Se ha eliminado y recreado el contenedor:

```bash
docker rm -f sysadmin-nginx
docker run -d --name sysadmin-nginx -p 8080:80 nginx:alpine
docker exec sysadmin-nginx sh -c "which curl || echo 'curl no persiste tras recrear el contenedor'"
```

El resultado demuestra que los cambios realizados manualmente dentro de un contenedor no persisten si el contenedor se elimina y se crea uno nuevo desde la imagen original. Para persistir datos se deben usar volúmenes, y para persistir cambios de software se debe construir una nueva imagen mediante un Dockerfile.


## Eliminación de contenedor e imagen

Se ha eliminado el contenedor y posteriormente la imagen:

```bash
docker rm -f sysadmin-nginx
docker rmi nginx:alpine
```

Docker no permite eliminar una imagen que esté siendo usada por un contenedor existente, por eso primero se elimina el contenedor.

