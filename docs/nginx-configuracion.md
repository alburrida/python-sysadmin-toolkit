# Configuración de NGINX como proxy inverso

## Objetivo

Se ha añadido un tercer servicio al `docker-compose.yml` llamado `proxy`, usando la imagen oficial `nginx:alpine`.

NGINX queda como único punto de entrada público de la infraestructura.

## Arquitectura resultante

```text
Cliente
  |
  | HTTP 80 / HTTPS 443
  v
NGINX proxy
  |
  | red interna Docker
  v
Backend FastAPI :8000
  |
  v
Redis :6379
```

## Cambios en Docker Compose

El backend ya no publica el puerto `8000` al host. Solo lo expone internamente:

```yaml
expose:
  - "8000"
```

El proxy publica los puertos externos:

```yaml
ports:
  - "80:80"
  - "443:443"
```

Redis continúa sin publicar puertos al host.

## Configuración como volumen de solo lectura

La configuración de NGINX se monta como volumen de solo lectura:

```yaml
volumes:
  - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
```

También se montan los certificados y los archivos estáticos:

```yaml
- ./nginx/certs:/etc/nginx/certs:ro
- ./static:/usr/share/nginx/html/static:ro
```

## Upstream

Se define un upstream hacia el backend:

```nginx
upstream backend_api {
    server backend:8000;
}
```

Gracias al DNS interno de Docker Compose, NGINX puede resolver `backend` como nombre del servicio.

## Proxy pass

Las peticiones se reenvían a FastAPI con:

```nginx
proxy_pass http://backend_api;
```

## Cabeceras de proxy

Se han añadido cabeceras para conservar información original de la petición:

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

## Archivos estáticos

NGINX sirve archivos estáticos directamente desde:

```text
/usr/share/nginx/html/static/
```

Prueba realizada:

```bash
curl -k https://localhost/static/status.txt
```

## HTTPS local

Se generó un certificado autofirmado local:

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout nginx/certs/local.key \
  -out nginx/certs/local.crt \
  -subj "/C=ES/ST=Madrid/L=Madrid/O=SysadminToolkit/OU=ASIR/CN=localhost"
```

La configuración HTTPS usa:

```nginx
ssl_certificate /etc/nginx/certs/local.crt;
ssl_certificate_key /etc/nginx/certs/local.key;
```

Como es un certificado autofirmado, las pruebas con `curl` usan `-k`.

## Redirección HTTP a HTTPS

El bloque de puerto 80 redirige a HTTPS:

```nginx
return 301 https://$host$request_uri;
```

Prueba:

```bash
curl -I http://localhost/health
```

## Rate limiting

Se ha configurado una zona de limitación por IP:

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
```

Y se aplica al proxy principal:

```nginx
limit_req zone=api_limit burst=20 nodelay;
```

Esto ayuda a proteger la API frente a abuso o ataques de fuerza bruta.

## Evidencias

Estado de Compose:

```text
docs/nginx-compose-ps.txt
```

Logs del proxy:

```text
docs/nginx-proxy-logs.txt
```

Respuesta del endpoint `/health` por NGINX:

```text
docs/nginx-health-response.json
```

Respuesta del archivo estático:

```text
docs/nginx-static-response.txt
```
