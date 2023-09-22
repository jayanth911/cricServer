import asyncio
import websockets


class DataLoader:
    def __init__(self, file_path, message_rate):
        self.file_path = file_path
        self.message_rate = message_rate
        self.websocket_server = None

    async def start_server(self):
        server = await websockets.serve(self.handle_client, "localhost", 8765)
        await server.wait_closed()

    async def handle_client(self, websocket, path):
        self.websocket_server = websocket
        with open(self.file_path, "r") as file:
            for line in file:
                if not self.websocket_server:
                    break
                await self.send_line(line.strip())
                await asyncio.sleep(self.message_rate / 1000)

    async def send_line(self, line):
        if self.websocket_server and self.websocket_server.open:
            await self.websocket_server.send(line)
        else:
            print("WebSocket connection is closed. Stopping data loader.")
            self.websocket_server = None

    def stop(self):
        if self.websocket_server and self.websocket_server.open:
            self.websocket_server.close()
            self.websocket_server = None


if __name__ == "__main__":
    file_path = "file.txt"
    message_rate = 2000  # Adjust this value as needed in ms

    data_loader = DataLoader(file_path, message_rate)

    try:
        asyncio.get_event_loop().run_until_complete(data_loader.start_server())
    except KeyboardInterrupt:
        print("Stopping the data loader...")
        data_loader.stop()
# import asyncio
# import websockets

# class DataLoader:
#     def __init__(self, file_path, message_rate):
#         self.file_path = file_path
#         self.message_rate = message_rate

#     async def start_server(self):
#         while True:
#             async with websockets.connect("ws://localhost:8765") as websocket:
#                 with open(self.file_path, 'r') as file:
#                     for line in file:
#                         await self.send_line(websocket, line.strip())
#                         await asyncio.sleep(1/self.message_rate)

#     async def send_line(self, websocket, line):
#         await websocket.send(line)

# if __name__ == "__main__":
#     file_path = "file.txt"
#     message_rate = 1  # Adjust this value as needed

#     data_loader = DataLoader(file_path, message_rate)

#     try:
#         asyncio.get_event_loop().run_until_complete(data_loader.start_server())
#     except KeyboardInterrupt:
#         print("Stopping the data loader...")
