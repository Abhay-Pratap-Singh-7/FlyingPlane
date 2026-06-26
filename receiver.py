import socket
import struct
import time
from collections import deque

def main():
    port = 9000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Increase socket receive buffer size for high-frequency telemetry
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
    sock.bind(('0.0.0.0', port))
    
    print(f"Listening for UDP gyroscope data on port {port}...")
    
    timestamps = deque(maxlen=200)
    packet_count = 0
    
    try:
        while True:
            data, addr = sock.recvfrom(12)
            if len(data) != 12:
                continue
            
            # Unpack 3 floats in big-endian (network byte order)
            x, y, z = struct.unpack('!fff', data)
            packet_count += 1
            
            now = time.time()
            timestamps.append(now)
            
            # Calculate rolling Hz over window of last 200 packets
            if len(timestamps) > 1:
                duration = timestamps[-1] - timestamps[0]
                hz = (len(timestamps) - 1) / duration if duration > 0 else 0.0
            else:
                hz = 0.0
                
            # Throttle print frequency to avoid terminal rendering overhead bottlenecking receiver loop
            if packet_count % 15 == 0:
                print(f"[{addr[0]}] Gyro X: {x:8.4f} | Y: {y:8.4f} | Z: {z:8.4f} | Rate: {hz:6.1f} Hz", end='\r', flush=True)
                
    except KeyboardInterrupt:
        print("\nReceiver stopped.")
    finally:
        sock.close()

if __name__ == '__main__':
    main()
