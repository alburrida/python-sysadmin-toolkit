# Fundamentos teóricos de Docker

## Máquina virtual frente a contenedor Docker

Una máquina virtual emula un sistema completo. Incluye su propio sistema operativo invitado, kernel, librerías, servicios y aplicaciones. Esto permite un aislamiento fuerte, pero consume más recursos porque cada máquina virtual necesita arrancar y mantener su propio sistema operativo.

Un contenedor Docker no virtualiza una máquina completa. Ejecuta procesos aislados sobre el sistema operativo del host, compartiendo el kernel del host. Esto hace que los contenedores sean más ligeros, rápidos de arrancar y fáciles de replicar.

La diferencia principal es que una máquina virtual incluye un sistema operativo completo, mientras que un contenedor empaqueta la aplicación y sus dependencias, pero utiliza el kernel del sistema anfitrión.

## Recursos compartidos con el host

Un contenedor comparte con el host el kernel del sistema operativo. También utiliza recursos físicos del host como CPU, memoria, red y disco, aunque Docker puede limitar y controlar el acceso a esos recursos.

## Elementos que aísla Docker

Docker aísla procesos, sistema de archivos, red, variables de entorno y dependencias de la aplicación. Esto permite que una aplicación se ejecute de forma independiente sin mezclar sus librerías o configuración con las del sistema principal.

## Conceptos clave

### Imagen

Una imagen es una plantilla inmutable que contiene todo lo necesario para ejecutar una aplicación: código, dependencias, librerías, configuración y comandos de arranque.

### Contenedor

Un contenedor es una instancia en ejecución de una imagen. Si la imagen es la plantilla, el contenedor es el proceso real ejecutándose.

### Dockerfile

Un Dockerfile es un archivo de texto con instrucciones para construir una imagen Docker. Define la imagen base, las dependencias, los archivos que se copian y el comando de arranque.

### Docker Hub

Docker Hub es un registro público donde se almacenan y distribuyen imágenes Docker. Desde Docker Hub se pueden descargar imágenes oficiales como `nginx`, `redis`, `ubuntu` o `python`.

### Capa

Una capa es una parte de una imagen Docker generada por una instrucción del Dockerfile. Docker reutiliza capas en caché para acelerar futuras construcciones.

### Registro

Un registro es un repositorio de imágenes Docker. Puede ser público, como Docker Hub, o privado, como un registro interno de empresa.

## Ciclo de vida de un contenedor

Un contenedor puede pasar por varios estados:

- Creado: el contenedor existe, pero todavía no está ejecutándose.
- En ejecución: el proceso principal del contenedor está activo.
- Pausado: el contenedor está congelado temporalmente.
- Detenido: el proceso principal ha terminado.
- Eliminado: el contenedor se ha borrado del sistema.

Cuando un contenedor se elimina, los datos escritos dentro de su sistema de archivos desaparecen salvo que se hayan almacenado en un volumen o en un bind mount. Por eso los volúmenes son necesarios para persistir información.

## Diagrama lógico de Docker

```text
+--------------------------------------------------+
| Host Ubuntu                                      |
|                                                  |
|  +--------------------------------------------+  |
|  | Kernel Linux compartido                    |  |
|  +--------------------------------------------+  |
|                                                  |
|  +--------------------------------------------+  |
|  | Docker Engine                              |  |
|  | - Gestiona imágenes                        |  |
|  | - Crea contenedores                        |  |
|  | - Gestiona redes y volúmenes               |  |
|  +--------------------------------------------+  |
|                                                  |
|  +----------------+  +----------------------+  |
|  | Contenedor API |  | Contenedor Redis     |  |
|  | Python/FastAPI |  | Base de datos cache  |  |
|  +----------------+  +----------------------+  |
|                                                  |
|  +----------------+                            |
|  | Contenedor NGINX                            |
|  | Proxy inverso                               |
|  +----------------+                            |
+--------------------------------------------------+
```

Docker Engine se ejecuta sobre el sistema operativo anfitrión y utiliza el kernel del host para ejecutar contenedores aislados. Cada contenedor tiene su propio sistema de archivos, red y procesos, pero no incluye un kernel propio.
