
## Programación orientada a objetos aplicada a redes

La programación orientada a objetos permite representar dispositivos de red como entidades con atributos y comportamientos propios.

En esta práctica se ha creado una clase base llamada `NetworkDevice`, que contiene datos comunes como `hostname`, `ip` y `mac`. A partir de esa clase se han creado clases hijas como `Router` y `Server`, que heredan esos atributos comunes pero añaden información específica.

Este enfoque ayuda a mantener un inventario de red más ordenado, porque todos los dispositivos siguen una estructura común. Además, mediante polimorfismo, cada tipo de dispositivo puede aplicar su propia lógica de auditoría usando el método `audit_device()`.

Un router no se audita igual que un servidor. En un router interesa revisar firmware, reglas de firewall, NAT o administración remota. En un servidor interesa revisar actualizaciones, usuarios privilegiados, servicios críticos y logs. La POO permite separar esas diferencias sin duplicar código innecesario.
