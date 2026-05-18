# Imágenes por capas y Dockerfile

## Sistema de capas de Docker

Una imagen Docker está formada por capas. Cada instrucción importante del Dockerfile genera una nueva capa sobre la anterior. Por ejemplo, una instrucción `FROM` define la base, una instrucción `RUN` puede instalar paquetes y una instrucción `COPY` puede añadir archivos de la aplicación.

Docker reutiliza estas capas mediante caché. Si una capa no ha cambiado, Docker no necesita reconstruirla y puede usar la versión anterior. Esto acelera mucho el proceso de construcción de imágenes.

## Importancia del orden de instrucciones

El orden de las instrucciones afecta directamente al rendimiento del build.

Si se copia todo el proyecto antes de instalar dependencias, cualquier cambio pequeño en el código invalida la caché y obliga a reinstalar todas las dependencias.

Por eso es mejor copiar primero solo `requirements.txt`, instalar dependencias y después copiar el resto del código. Así, si cambia un archivo `.py`, Docker mantiene cacheada la capa de instalación de paquetes.

Ejemplo recomendado:

```Dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

Con esta estructura, la capa de dependencias solo se reconstruye si cambia `requirements.txt`.

## Instrucciones principales de un Dockerfile

### FROM

Define la imagen base desde la que se construye la nueva imagen.

```Dockerfile
FROM python:3.11-alpine
```

### WORKDIR

Establece el directorio de trabajo dentro del contenedor.

```Dockerfile
WORKDIR /app
```

### COPY

Copia archivos desde el host hacia la imagen.

```Dockerfile
COPY requirements.txt .
COPY . .
```

### ADD

También copia archivos, pero añade funciones extra como descomprimir archivos comprimidos o descargar desde una URL. En general, se recomienda usar `COPY` salvo que se necesiten esas funciones adicionales.

### RUN

Ejecuta comandos durante la construcción de la imagen. Se usa para instalar dependencias o preparar el entorno.

```Dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

### ENV

Define variables de entorno dentro de la imagen o del contenedor.

```Dockerfile
ENV PYTHONUNBUFFERED=1
```

### EXPOSE

Documenta el puerto que la aplicación usa dentro del contenedor. No publica el puerto por sí solo.

```Dockerfile
EXPOSE 8000
```

### CMD

Define el comando por defecto que se ejecutará al iniciar el contenedor.

```Dockerfile
CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ENTRYPOINT

Define el ejecutable principal del contenedor. Se suele usar cuando el contenedor debe comportarse siempre como un comando concreto.

```Dockerfile
ENTRYPOINT ["python"]
```

### ARG

Define variables disponibles durante el build de la imagen. A diferencia de `ENV`, no están pensadas para permanecer como variables de entorno en ejecución.

```Dockerfile
ARG APP_VERSION=1.0
```

## Diferencia entre CMD y ENTRYPOINT

`CMD` define el comando por defecto del contenedor, pero se puede sobrescribir fácilmente al ejecutar `docker run`.

`ENTRYPOINT` define el ejecutable principal del contenedor. Los argumentos pasados al ejecutar el contenedor suelen añadirse al `ENTRYPOINT`.

En la práctica, `CMD` es más flexible para aplicaciones normales. `ENTRYPOINT` es útil cuando la imagen debe funcionar como una herramienta ejecutable fija.

Ejemplo con CMD:

```Dockerfile
CMD ["python", "sys_toolkit.py"]
```

Se puede sobrescribir con:

```bash
docker run imagen python otro_script.py
```

Ejemplo con ENTRYPOINT:

```Dockerfile
ENTRYPOINT ["python"]
CMD ["sys_toolkit.py"]
```

En ese caso, el contenedor ejecuta siempre `python` y se le puede cambiar el argumento.

## Imagen base Alpine

Alpine Linux es una distribución ligera orientada a seguridad y bajo consumo de recursos. Las imágenes basadas en Alpine suelen ocupar mucho menos espacio que imágenes basadas en Ubuntu o Debian.

Se prefiere Alpine cuando se quiere reducir el tamaño de la imagen, acelerar despliegues y disminuir la superficie de ataque.

Sin embargo, Alpine usa `musl` en lugar de `glibc`, por lo que algunas dependencias pueden requerir compilación adicional o paquetes específicos. En proyectos Python sencillos suele ser una buena opción, pero en proyectos con dependencias pesadas a veces puede ser más cómodo usar imágenes basadas en Debian slim.

## Conclusión

El uso correcto de capas y Dockerfile permite crear imágenes reproducibles, ligeras y rápidas de reconstruir. Para este proyecto se usará una imagen base `python:3.11-alpine`, se copiará primero `requirements.txt` para aprovechar la caché, y después se copiará el resto del código de la aplicación.
