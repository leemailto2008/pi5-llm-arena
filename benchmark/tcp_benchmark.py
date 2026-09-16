# f:\12_prj_raspi5\benchmark\tcp_benchmark.py
import sys
import socket
import time

def run_server(port=9999, size_mb=50):
    print(f"[*] Starting TCP Bench Server on port {port}, sending {size_mb} MB from RAM...", flush=True)
    data = b'A' * (64 * 1024)
    total_bytes = size_mb * 1024 * 1024
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    print(f"[*] Waiting for benchmark client on port {port}...", flush=True)
    
    conn, addr = server.accept()
    print(f"[+] Client connected from {addr}, streaming data...", flush=True)
    start = time.time()
    sent = 0
    try:
        while sent < total_bytes:
            chunk = min(len(data), total_bytes - sent)
            conn.sendall(data[:chunk])
            sent += chunk
    except Exception as e:
        print(f"[!] Server error: {e}", flush=True)
    finally:
        conn.close()
        server.close()
        
    elapsed = time.time() - start
    speed = (sent / (1024 * 1024)) / elapsed if elapsed > 0 else 0
    print(f"[✓] Server sent {sent / (1024*1024):.2f} MB in {elapsed:.2f}s ({speed:.2f} MB/s)", flush=True)

def run_client(server_ip="192.168.50.228", port=9999, bind_ip="192.168.50.3"):
    print(f"[*] Connecting to {server_ip}:{port} (Source: {bind_ip})...", flush=True)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((bind_ip, 0))
    start_conn = time.time()
    client.connect((server_ip, port))
    conn_time = time.time() - start_conn
    print(f"[+] Connected in {conn_time*1000:.1f}ms. Receiving stream...", flush=True)
    
    start_recv = time.time()
    received = 0
    last_print = time.time()
    while True:
        buf = client.recv(64 * 1024)
        if not buf:
            break
        received += len(buf)
        now = time.time()
        if now - last_print >= 1.0:
            cur_mb = received / (1024 * 1024)
            cur_spd = cur_mb / (now - start_recv)
            print(f"    [Recv] {cur_mb:5.1f} MB | Instant Speed: {cur_spd:5.2f} MB/s", flush=True)
            last_print = now
            
    client.close()
    elapsed = time.time() - start_recv
    mb = received / (1024 * 1024)
    speed = mb / elapsed if elapsed > 0 else 0
    print(f"[✓] Client received {mb:.2f} MB in {elapsed:.2f}s ({speed:.2f} MB/s)", flush=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        run_server()
    elif len(sys.argv) > 1 and sys.argv[1] == "client":
        bind = sys.argv[2] if len(sys.argv) > 2 else "192.168.50.3"
        target = sys.argv[3] if len(sys.argv) > 3 else "192.168.50.228"
        run_client(server_ip=target, bind_ip=bind)
