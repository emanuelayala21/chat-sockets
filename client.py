import asyncio
import websockets
import sys

URI = "ws://localhost:5555"

async def chat():
    name = input("Ingresa tu nombre de usuario: ").strip() or "Anónimo"

    try:
        async with websockets.connect(URI) as ws:
            await ws.send(name)
            print(f"[Conectado como '{name}'. Escribe /salir para salir]")

            async def receive():
                async for message in ws:
                    print(message)

            async def send():
                loop = asyncio.get_event_loop()
                while True:
                    msg = await loop.run_in_executor(None, input)
                    if msg.lower() in ("/salir", "/exit", "/quit"):
                        await ws.close()
                        break
                    await ws.send(msg)

            await asyncio.gather(receive(), send())

    except ConnectionRefusedError:
        print(f"[Error] No se pudo conectar a {URI}. ¿El servidor está corriendo?")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(chat())
