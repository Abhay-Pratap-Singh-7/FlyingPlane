import asyncio
import socket
import struct
import json
import threading
import websockets

CONNECTED_CLIENTS = set()
loop = None

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

async def register(websocket):
    CONNECTED_CLIENTS.add(websocket)
    local_ip = get_local_ip()
    try:
        await websocket.send(json.dumps({"type": "status", "ip": local_ip}))
        await websocket.wait_closed()
    finally:
        CONNECTED_CLIENTS.remove(websocket)

def udp_receive_loop():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Increase socket buffer to handle high frequency telemetry
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
    sock.bind(('0.0.0.0', 9000))
    
    print("UDP Listener running on port 9000...")
    while True:
        try:
            data, _ = sock.recvfrom(12)
            if len(data) == 12:
                x, y, z = struct.unpack('!fff', data)
                payload = json.dumps({"x": x, "y": y, "z": z})
                
                if CONNECTED_CLIENTS and loop:
                    # Thread-safe schedule broadcast on asyncio loop
                    asyncio.run_coroutine_threadsafe(broadcast(payload), loop)
        except Exception:
            pass

async def broadcast(message):
    if CONNECTED_CLIENTS:
        # Broadcast concurrently to all connected web browser sessions
        await asyncio.gather(
            *[client.send(message) for client in CONNECTED_CLIENTS],
            return_exceptions=True
        )

async def main():
    global loop
    loop = asyncio.get_running_loop()
    
    # Run UDP receiver loop in a dedicated background thread
    threading.Thread(target=udp_receive_loop, daemon=True).start()
    
    async with websockets.serve(register, "0.0.0.0", 8765):
        print("WebSocket Server running on ws://localhost:8765")
        
        # Automatically open the game in default web browser
        import webbrowser
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(script_dir, "index.html")
        webbrowser.open(f"file://{html_path}")
        
        await asyncio.Future()  # Keep running forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBridge stopped.")
