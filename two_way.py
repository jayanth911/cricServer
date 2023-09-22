import asyncio
import websockets

class DataLoader:
    def __init__(self, message_rate):
        self.message_rate = message_rate
        self.clients = set()

    async def start_server(self):
        server = await websockets.serve(self.handle_client, "192.168.29.193", 8765)
        await server.wait_closed()



    async def handle_client(self, websocket, path):
        self.clients.add(websocket)
        try:
            
            async for message in websocket:
                print(message)
                await self.broadcast(message, websocket)
                await asyncio.sleep(self.message_rate / 1000)
        except websockets.ConnectionClosed:
            print("Connection closed by the client")
        finally:
            self.clients.remove(websocket)

    async def broadcast(self, message, sender):
        removals = []
        for client in self.clients:
            if client != sender:
                if client.open:
                    await client.send(message)
                else:
                    removals.append(client)
        
        # Clean up closed websockets
        for client in removals:
            self.clients.remove(client)

if __name__ == "__main__":
    message_rate = 1  # Adjust this value as needed in ms

    data_loader = DataLoader(message_rate)
    try:
        asyncio.get_event_loop().run_until_complete(data_loader.start_server())
    except KeyboardInterrupt:
        print("Stopping the data loader...")
