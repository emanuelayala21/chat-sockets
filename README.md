# Chat Distribuido con Sockets TCP

Sistema de chat distribuido implementado en Python usando sockets TCP y manejo de concurrencia con hilos (threads). Proyecto académico para el curso BISOF 18 - Sistemas Operativos II, Universidad Latina de Costa Rica, 2026.

## Descripción

El sistema implementa una arquitectura cliente-servidor donde:

- El **servidor** acepta múltiples conexiones simultáneas, cada una atendida por un hilo independiente.
- Los **clientes** se conectan al servidor, envían mensajes y reciben en tiempo real los mensajes de los demás usuarios.
- El servidor implementa **tolerancia a fallos**: detecta desconexiones abruptas y continúa operando sin interrupciones para los demás clientes.

## Tecnologías

- Python 3.11 (módulos estándar: `socket`, `threading`)
- Docker y Docker Compose

## Estructura del proyecto

```
chat-distribuido/
├── server.py          # Servidor TCP con manejo de hilos
├── client.py          # Cliente de consola
├── Dockerfile         # Imagen Docker del servidor
├── docker-compose.yml # Despliegue del servidor con Docker
└── README.md
```

## Cómo ejecutar

### Opción 1: Con Docker (recomendado)

**Iniciar el servidor:**
```bash
docker-compose up --build
```

**Conectar un cliente** (en otra terminal):
```bash
python client.py
```

### Opción 2: Sin Docker

**Terminal 1 - Servidor:**
```bash
python server.py
```

**Terminal 2, 3, 4... - Clientes:**
```bash
python client.py
```

## Uso

1. Al ejecutar `client.py` se solicita un nombre de usuario.
2. Una vez conectado, escribe mensajes y presiona Enter para enviarlos.
3. Los mensajes son recibidos por todos los demás clientes conectados.
4. Para salir escribe `/salir`, `/exit` o `/quit`.

## Conceptos aplicados

| Concepto | Implementación |
|----------|---------------|
| Sockets TCP | `socket.socket(AF_INET, SOCK_STREAM)` |
| Concurrencia | `threading.Thread` por cliente |
| Sincronización | `threading.Lock` en lista de clientes |
| Tolerancia a fallos | Captura de `ConnectionResetError` y `BrokenPipeError` |
| Sistemas distribuidos | Arquitectura cliente-servidor con broadcast |

## Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

## Autor

Emmanuel José Ayala Núñez  
Universidad Latina de Costa Rica  
BISOF 18 - Sistemas Operativos II, 2026
