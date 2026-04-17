import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5555


def receive_messages(client_socket: socket.socket):
    #Hilo que escucha mensajes entrantes del servidor.
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print("[Desconectado del servidor]")
                break
            print(message.decode(), end="")
        except (ConnectionResetError, OSError):
            print("[Error de conexión. Saliendo...]")
            break
    client_socket.close()
    sys.exit(0)


def send_messages(client_socket: socket.socket):
    #Hilo que lee input del usuario y lo envía al servidor.
    while True:
        try:
            message = input()
            if message.lower() in ("/salir", "/exit", "/quit"):
                print("[Cerrando conexión...]")
                client_socket.close()
                sys.exit(0)
            client_socket.send(message.encode())
        except (EOFError, OSError):
            break


def start_client():
    name = input("Ingresa tu nombre de usuario: ").strip()
    if not name:
        name = "Anónimo"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[Error] No se pudo conectar a {HOST}:{PORT}. ¿El servidor está corriendo?")
        sys.exit(1)

    # envía el nombre como primer mensaje para identificarse
    client_socket.send(name.encode())

    print(f"[Conectado al chat como '{name}'. Escribe /salir para salir]")

    # hilo receptor: solo escucha, no bloquea el input
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,), daemon=True)
    recv_thread.start()

    # hilo de envío: lee desde consola
    send_messages(client_socket)


if __name__ == "__main__":
    start_client()
