import asyncio
import websockets

clients = set()

async def broadcast(message, sender=None):
    """Envía un mensaje a todos los clientes excepto al remitente."""
    targets = clients - {sender} if sender else clients
    if targets:
        await asyncio.gather(*[c.send(message) for c in targets], return_exceptions=True)

async def handle_client(websocket):
    """Maneja la conexión de un cliente WebSocket."""
    # primer mensaje es el nombre
    try:
        name = await websocket.recv()
        name = name.strip() or "Anónimo"
    except websockets.ConnectionClosed:
        return

    clients.add(websocket)
    print(f"[CONEXIÓN] {name} conectado. Activos: {len(clients)}")
    await broadcast(f"[Servidor] {name} se unió al chat.", sender=websocket)
    await websocket.send("[Servidor] Conectado. Ya puedes chatear.")

    try:
        async for message in websocket:
            print(f"[{name}]: {message}")
            await broadcast(f"[{name}]: {message}", sender=websocket)
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.discard(websocket)
        print(f"[DESCONEXIÓN] {name}. Activos: {len(clients)}")
        await broadcast(f"[Servidor] {name} abandonó el chat.")

async def main():
    print("[SERVIDOR] Escuchando en 0.0.0.0:5555")
    async with websockets.serve(handle_client, "0.0.0.0", 5555):
        await asyncio.Future()  # corre indefinidamente

if __name__ == "__main__":
    asyncio.run(main())
