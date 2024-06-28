import asyncio
import websockets
from src.service.db import get_response_from_db,initialize_redis_connection



redis_connection = initialize_redis_connection()


async def handler(websocket, path):
    print(f"New connection from {websocket.remote_address}")
    try:
        # Send an initial message to the client
        await websocket.send("Processing Your Code")

        # Keep the connection open and handle incoming messages indefinitely
        async for message in websocket:
            print(f"Received message: {message}")
            response = get_response_from_db(redis_connection, message)
            await websocket.send(response)
            await websocket.close()

    except websockets.ConnectionClosed as e:
        print(f"Connection closed with code: {e.code}, reason: {e.reason}")

# Start the WebSocket server
start_server = websockets.serve(handler, "localhost", 12345)

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server started on ws://localhost:12345")
asyncio.get_event_loop().run_forever()
