import asyncio
import websockets

async def client():
    uri = "ws://localhost:8765"  # Replace with the server URI

    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                print("Received:", message)
            except websockets.ConnectionClosed:
                print("Connection to server closed.")
                break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(client())
