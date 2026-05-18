# Gestión avanzada y limpieza del entorno Docker

## Objetivo

En este apartado se practica la administración avanzada de la infraestructura Docker Compose:

- Ciclo de vida completo de los servicios.
- Reconstrucción de servicios concretos.
- Escalado del backend.
- Consulta de logs.
- Monitorización de recursos.
- Limpieza de recursos no utilizados.


## Ciclo de vida con Docker Compose

Se han usado comandos básicos de administración:

```bash
docker compose ps
docker compose logs --tail=30
docker compose restart backend
docker compose ps
```

`docker compose ps` permite ver el estado de los servicios.  
`docker compose logs` permite revisar la salida de los contenedores.  
`docker compose restart backend` reinicia únicamente el servicio backend sin reiniciar Redis ni NGINX.


## Reconstrucción de un solo servicio

Se ha reconstruido únicamente el backend:

```bash
docker compose build backend
docker compose up -d backend
```

Esto permite aplicar cambios en la imagen del backend sin reconstruir Redis ni NGINX.


## Escalado del backend

Para poder escalar el backend fue necesario eliminar `container_name` del servicio `backend`, ya que Docker Compose no puede crear varias réplicas con el mismo nombre fijo.

Se escaló el backend a dos instancias:

```bash
docker compose up -d --build --scale backend=2
docker compose ps
```

El proxy NGINX sigue siendo el único punto de entrada público, mientras que las réplicas del backend quedan dentro de la red interna de Docker.

La evidencia se guardó en:

```text
docs/docker-scale-backend-ps.txt
```


## Monitorización de recursos

Se ha consultado el uso de recursos en tiempo real con:

```bash
docker stats
```

Para guardar una captura puntual:

```bash
docker stats --no-stream
```

La salida se guardó en:

```text
docs/docker-stats.txt
```

Este comando permite revisar CPU, memoria, red y uso de bloque de cada contenedor.


## Uso de disco antes de limpieza

Se consultó el espacio usado por Docker con:

```bash
docker system df
```

La salida previa a la limpieza se guardó en:

```text
docs/docker-system-df-before.txt
```


## Limpieza de recursos no utilizados

Se realizó una limpieza segura de recursos no utilizados:

```bash
docker system prune -f
```

No se usó `--volumes`, para evitar eliminar volúmenes persistentes con datos de la aplicación o Redis.

La salida posterior a la limpieza se guardó en:

```text
docs/docker-system-df-after.txt
```

Comparando `docker-system-df-before.txt` y `docker-system-df-after.txt` se puede observar el espacio recuperado.

