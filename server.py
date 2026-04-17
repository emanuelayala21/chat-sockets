import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

clients = []       # lista de (socket, nombre)
lock = threading.Lock()


def broadcast(message: bytes, sender_socket=None):
    """Envía un mensaje a todos los clientes excepto al remitente."""
    with lock:
        for client_socket, _ in clients:
            if client_socket is not sender_socket:
                try:
                    client_socket.send(message)
                except Exception:
                    pass  # si falla el envío se limpia en handle_client


def remove_client(client_socket, name: str):
    """Elimina un cliente desconectado del registro activo."""
    with lock:
        clients[:] = [(s, n) for s, n in clients if s is not client_socket]
    try:
        client_socket.close()
    except Exception:
        pass
    print(f"[DESCONEXIÓN] {name} se desconectó. Clientes activos: {len(clients)}")
    broadcast(f"[Servidor] {name} abandonó el chat.\n".encode())


def handle_client(client_socket: socket.socket, address):
    """Hilo dedicado a un cliente: recibe mensajes y los difunde."""
    # primer mensaje es el nombre del usuario
    try:
        name = client_socket.recv(1024).decode().strip()
    except Exception:
        client_socket.close()
        return

    with lock:
        clients.append((client_socket, name))

    print(f"[CONEXIÓN] {name} conectado desde {address}. Clientes activos: {len(clients)}")
    broadcast(f"[Servidor] {name} se unió al chat.\n".encode(), sender_socket=client_socket)
    client_socket.send("[Servidor] Conectado. Ya puedes enviar mensajes.\n".encode())

    while True:
        try:
            message = client_socket.recv(1024)
            if not message:  # conexión cerrada limpiamente
                break
            text = message.decode().strip()
            print(f"[{name}]: {text}")
            broadcast(f"[{name}]: {text}\n".encode(), sender_socket=client_socket)
        except (ConnectionResetError, BrokenPipeError, OSError):
            break  # desconexión abrupta

    remove_client(client_socket, name)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Apagando servidor...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
