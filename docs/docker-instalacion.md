# Instalación y primer contacto con Docker

## Verificación de Docker

```text
Docker version 29.1.3, build 29.1.3-0ubuntu3~24.04.2
Docker Compose version 2.40.3+ds1-0ubuntu1~24.04.1
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## Salida de docker version

```text
Client:
 Version:           29.1.3
 API version:       1.52
 Go version:        go1.24.4
 Git commit:        29.1.3-0ubuntu3~24.04.2
 Built:             Wed Apr 29 16:41:06 2026
 OS/Arch:           linux/amd64
 Context:           default

Server:
 Engine:
  Version:          29.1.3
  API version:      1.52 (minimum version 1.44)
  Go version:       go1.24.4
  Git commit:       29.1.3-0ubuntu3~24.04.2
  Built:            Wed Apr 29 16:41:06 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          2.2.1
  GitCommit:        
 runc:
  Version:          1.3.4-0ubuntu1~24.04.1
  GitCommit:        
 docker-init:
  Version:          0.19.0
  GitCommit:        
```

## Salida de docker info

```text
Client:
 Version:    29.1.3
 Context:    default
 Debug Mode: false
 Plugins:
  compose: Docker Compose (Docker Inc.)
    Version:  2.40.3+ds1-0ubuntu1~24.04.1
    Path:     /usr/libexec/docker/cli-plugins/docker-compose
  trust: Manage trust on Docker images (Docker Inc.)
    Version:  29.1.3
    Path:     /usr/libexec/docker/cli-plugins/docker-trust

Server:
 Containers: 2
  Running: 0
  Paused: 0
  Stopped: 2
 Images: 7
 Server Version: 29.1.3
 Storage Driver: overlayfs
  driver-type: io.containerd.snapshotter.v1
 Logging Driver: json-file
 Cgroup Driver: systemd
 Cgroup Version: 2
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local splunk syslog
 CDI spec directories:
  /etc/cdi
  /var/run/cdi
 Swarm: inactive
 Runtimes: io.containerd.runc.v2 runc
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 
 runc version: 
 init version: 
 Security Options:
  apparmor
  seccomp
   Profile: builtin
  cgroupns
 Kernel Version: 6.8.0-111-generic
 Operating System: Ubuntu 24.04.4 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 1
 Total Memory: 1.922GiB
 Name: ubuntulab
 ID: 22d38d92-f22e-4407-9231-53e285e2b14a
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Username: alburrida
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
  ::1/128
 Live Restore Enabled: false
 Firewall Backend: iptables

```

## Primer contenedor: hello-world

```text

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

```

Docker ha descargado la imagen hello-world si no estaba disponible localmente, ha creado un contenedor temporal, ha ejecutado el proceso principal y lo ha eliminado automáticamente gracias a la opción --rm.

## Contenedor Ubuntu efímero

Se ha ejecutado el siguiente comando:

```bash
docker run --rm -it ubuntu:22.04 bash
```

Este comando descarga la imagen `ubuntu:22.04` si no está disponible, crea un contenedor interactivo y abre una terminal Bash dentro de él.

Dentro del contenedor se ha comprobado el sistema con:

```bash
cat /etc/os-release
```

Después se ha salido con:

```bash
exit
```

Al usar la opción `--rm`, Docker elimina automáticamente el contenedor al finalizar. Por eso, al ejecutar `docker ps -a`, el contenedor efímero ya no aparece.
