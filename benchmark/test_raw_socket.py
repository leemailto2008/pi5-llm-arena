# f:\12_prj_raspi5\benchmark\test_raw_socket.py
import socket
import time
import subprocess

PI_HOST = "192.168.50.228"
KEY_PATH = r"C:\Users\Andrew\.ssh\id_rsa_pi5"
TEST_BYTES = 20 * 1024 * 1024  # 20 MB

def test_download_speed():
    # 1. Start server on Pi 5 that sends TEST_BYTES to connecting client
    pi_server_cmd = (
        "python3 -c \""
        "import socket; "
        "s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); "
        "s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); "
        "s.bind(('0.0.0.0', 9876)); "
        "s.listen(1); "
        "conn, _ = s.accept(); "
        "chunk = b'A' * 65536; "
        f"sent = 0; target = {TEST_BYTES}; "
        "while sent < target: conn.sendall(chunk); sent += len(chunk); "
        "conn.close(); s.close()\""
    )
    
    print(f"[*] Starting sender daemon on Pi 5 ({PI_HOST}:9876)...")
    proc = subprocess.Popen([
        'ssh', '-i', KEY_PATH, '-o', 'BatchMode=yes', f'pi@{PI_HOST}',
        pi_server_cmd
    ])
    
    time.sleep(2)
    
    print("[*] Connecting to Pi 5 from Windows to receive 20 MB...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((PI_HOST, 9876))
    
    total = 0
    t0 = time.time()
    while True:
        data = client.recv(131072)
        if not data:
            break
        total += len(data)
    t1 = time.time()
    client.close()
    proc.wait()
    
    dt = t1 - t0
    speed_mbs = (total / (1024 * 1024)) / dt if dt > 0 else 0
    print(f"[✓] Transferred {total / (1024 * 1024):.2f} MB in {dt:.2f}s")
    print(f"[✓] Physical Raw TCP Throughput (Pi 5 -> Windows): {speed_mbs:.2f} MB/s ({speed_mbs * 8:.2f} Mbps)")

if __name__ == '__main__':
    test_download_speed()
