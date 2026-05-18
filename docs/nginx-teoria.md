# Proxy inverso y NGINX

## Qué es un proxy inverso

Un proxy inverso es un servidor que se coloca delante de una o varias aplicaciones internas. Recibe las peticiones de los clientes y las reenvía hacia el servicio backend correspondiente.

En esta práctica, NGINX actuará como proxy inverso delante de la API FastAPI.

Estructura lógica:

```text
Cliente/Navegador
      |
      v
NGINX puerto 80/443
      |
      v
Backend FastAPI puerto 8000
      |
      v
Redis puerto 6379
```

El cliente no accede directamente al backend ni a Redis. Solo accede a NGINX.

## Proxy inverso frente a proxy directo

Un proxy directo actúa en nombre del cliente. Se usa, por ejemplo, cuando una empresa quiere filtrar o controlar el tráfico de salida de sus empleados hacia Internet.

Un proxy inverso actúa en nombre del servidor. Se coloca delante de los servicios internos y decide a qué backend enviar cada petición.

Resumen:

```text
Proxy directo:
Cliente -> Proxy -> Internet

Proxy inverso:
Cliente -> Proxy inverso -> Servidor interno
```

## Por qué usar NGINX delante de una aplicación

NGINX se suele colocar delante de aplicaciones web por varias razones:

- Centraliza la entrada de tráfico.
- Permite ocultar los servicios internos.
- Puede gestionar certificados SSL/TLS.
- Permite redirigir HTTP a HTTPS.
- Puede aplicar rate limiting.
- Puede servir archivos estáticos directamente.
- Puede actuar como balanceador de carga.
- Puede añadir cabeceras de proxy.
- Puede mejorar el rendimiento mediante caché y buffering.

En una arquitectura más segura, FastAPI no debería publicar directamente su puerto al host. Solo NGINX debe publicar los puertos externos.

## Upstream en NGINX

Un `upstream` define uno o varios servidores backend a los que NGINX puede reenviar peticiones.

Ejemplo:

```nginx
upstream backend_api {
    server backend:8000;
}
```

En Docker Compose, `backend` es el nombre del servicio. NGINX puede resolverlo gracias al DNS interno de Docker.

## Server block

Un `server block` define cómo NGINX escucha peticiones y qué debe hacer con ellas.

Ejemplo:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://backend_api;
    }
}
```

En este caso, NGINX escucha en el puerto 80 y reenvía las peticiones al upstream `backend_api`.

## proxy_pass

La directiva `proxy_pass` indica a NGINX a qué servidor debe reenviar la petición.

Ejemplo:

```nginx
location / {
    proxy_pass http://backend_api;
}
```

Si el cliente solicita:

```text
http://localhost/health
```

NGINX lo reenvía internamente a:

```text
http://backend:8000/health
```

## Cabeceras de proxy

Cuando NGINX reenvía tráfico al backend, conviene pasar cabeceras para que la aplicación conozca información original de la petición.

Ejemplo:

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

Estas cabeceras permiten conservar el host original, la IP real del cliente y el protocolo usado.

## Rate limiting

El rate limiting permite limitar cuántas peticiones puede hacer un cliente en un periodo de tiempo.

Esto ayuda a reducir abusos, fuerza bruta o saturación del backend.

Ejemplo conceptual:

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
```

## Caché

NGINX puede cachear respuestas para evitar que ciertas peticiones lleguen siempre al backend.

En APIs dinámicas hay que usar caché con cuidado, pero para archivos estáticos o respuestas públicas puede mejorar mucho el rendimiento.

## SSL/TLS

NGINX puede encargarse de HTTPS y dejar que la aplicación interna funcione por HTTP dentro de la red Docker.

Esto se conoce como terminación SSL/TLS.

Estructura:

```text
Cliente -> HTTPS -> NGINX -> HTTP interno -> FastAPI
```

## Por qué NGINX es eficiente bajo carga

NGINX usa una arquitectura orientada a eventos y operaciones no bloqueantes. Esto permite manejar muchas conexiones concurrentes con pocos procesos de trabajo.

Apache tradicionalmente se ha asociado a modelos basados en procesos o hilos por conexión, aunque también puede usar módulos modernos como Event MPM. Aun así, NGINX suele ser especialmente eficiente en escenarios de alta concurrencia, proxy inverso y servicio de contenido estático.

## Aplicación en esta práctica

En esta infraestructura, NGINX se usará para:

- Publicar el puerto 80.
- Recibir las peticiones externas.
- Reenviar tráfico al backend FastAPI.
- Ocultar el puerto 8000 del backend.
- Mantener Redis inaccesible desde el exterior.
- Servir archivos estáticos.
- Aplicar cabeceras de proxy.
- Añadir rate limiting.
- Preparar HTTPS local con certificados autofirmados.
