import os
import sys
import time
import subprocess
import socket
import paramiko

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

WIFI_BIND_IP = "192.168.50.3"
PI_HOST = "192.168.50.228"
PI_USER = "pi"
KEY_PATH = r"C:\Users\Andrew\.ssh\id_rsa_pi5"
SSH_BIN = r"C:\Windows\System32\OpenSSH\ssh.exe"
REMOTE_MODELS = "/home/pi/.ollama/models"
LOCAL_MODELS = r"f:\12_prj_raspi5\raspi5_ollama_backup\models"
LOCAL_BLOBS = os.path.join(LOCAL_MODELS, "blobs")

# Format: (sha256_name, size_bytes, display_label)
BLOBS_CATALOG = [
    # Small metadata & template blobs (< 20KB)
    ("sha256-56380ca2ab89f1f68c283f4d50863c0bcab52ae3f1b9a88e4ab5617b176f71a3", 42, "config/digest"),
    ("sha256-ceaa5f78afb8d2870c886c89d6225f96e9b7d30737a230470b93cab69c357cd1", 33, "config/digest"),
    ("sha256-66b9ea09bd5b7099cbb4fc820f31b575c0366fa439b08245566692c6784e281e", 68, "config/digest"),
    ("sha256-8b89eea08a537a813b05fbc5edf73b7719a478a06ad69d8d02345294233ffef6", 88, "config/digest"),
    ("sha256-56bb8bd477a519ffa694fc449c2413c6f0e1d3b1c88fa7e3c9d88d3ae49d4dcb", 96, "config/digest"),
    ("sha256-f4d24e9138dd4603380add165d2b0d970bef471fac194b436ebd50e6147c6588", 148, "template"),
    ("sha256-803b5adc34487f9cabb9ca03316462d1c3089d516159eb2a00689e5a241834ce", 218, "template"),
    ("sha256-0a68a03f3c36f7b9201259dfb3a776a485e40ece5f9487465a9aadb59c3aa4ef", 461, "template"),
    ("sha256-c6bc3775a3fa9935ce4a3ccd7abc59e936c3de9308d2cc090516012f43ed9c07", 473, "template"),
    ("sha256-f0988ff50a2458c598ff6b1b87b94d0f5c44d73061c2795391878b00b2285e11", 473, "template"),
    ("sha256-161ddde4c9cd07c9f1ccb4e0167c434bce72caeb3fc1844262fa66bc877b0426", 487, "template"),
    ("sha256-40fb844194b25e429204e5163fb379ab462978a262b86aadd73d8944445c09fd", 487, "template"),
    ("sha256-455f34728c9b5dd3376378bfb809ee166c145b0b4c1f1a6feca069055066ef9a", 487, "template"),
    ("sha256-a85fe2a2e58e2426116d3686dfdc1a6ea58640c1e684069976aa730be6c1fa01", 487, "template"),
    ("sha256-d3d81dcf3ed1ec0108bd55ca284901be05a1fa76627c6705b344bd2fda19539d", 487, "template"),
    ("sha256-d9bb33f2786931fea42f50936a2424818aa2f14500638af2f01861eb2c8fb446", 487, "template"),
    ("sha256-c5ad996bda6eed4df6e3b605a9869647624851ac248209d22fd5e2c0cc1121d3", 556, "template"),
    ("sha256-34bb5ab01051a11372a91f95f3fbbc51173eed8e7f13ec395b9ae9b8bd0e242b", 561, "template"),
    ("sha256-6e4c38e1172f42fdbff13edf9a7a017679fb82b0fde415a3e8b3c31c6ed4a4e4", 1065, "template"),
    ("sha256-966de95ca8a62200913e3f8bfbf84c8494536f1b94b49166851e76644e966396", 1429, "template"),
    ("sha256-948af2743fc78a328dcb3b0f5a31b3d75f415840fdb699e8b1235978392ecf85", 1481, "template"),
    ("sha256-eb4402837c7829a690fa845de4d7f3fd842c2adee476d5341da8a46ea9255175", 1482, "template"),
    ("sha256-1e65450c30670713aa47fe23e8b9662bdf4065e81cc8e3cbfaa98924fcc0d320", 1615, "template"),
    ("sha256-a70ff7e570d97baaf4e62ac6e6ad9975e04caa6d900d3742d37698494479e0cd", 6016, "template"),
    ("sha256-b5c0e5cf74cf51af1ecbc4af597cfcd13fd9925611838884a681070838a14a50", 7387, "template"),
    ("sha256-fcc5a6bec9daf9b561a68827b67ab6088e1dba9d1fa2a50d7bbcc8384e0a265d", 7711, "template"),
    ("sha256-832dd9e00a68dd83b3c3fb9f5588dad7dcf337a0db50f7d9483f310cd292e92e", 11343, "template"),
    ("sha256-7339fa418c9ad3e8e12e74ad0fd26a9cc4be8703f9c110728a992b193be85cb2", 11355, "template"),
    ("sha256-43070e2d4e532684de521b885f385d0841030efa2b1a20bafb76133a5e1379c1", 11356, "template"),
    ("sha256-cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30", 11358, "template"),
    ("sha256-0ba8f0e314b4264dfd19df045cde9d4c394a52474bf92ed6a3de22a4ca31a177", 12320, "template"),
    # 10 Large GGUF Weight Blobs
    ("sha256-aabd4debf0c8f08881923f2c25fc0fdeed24435271c2b3e92c4af36704040dbc", 1117320512, "GGUF: deepseek-r1:1.5b"),
    ("sha256-5ee4f07cdb9beadbbb293e85803c569b01bd37ed059d2715faa7bb405f31caa6", 1929903008, "GGUF: qwen2.5:3b"),
    ("sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff", 2019377376, "GGUF: llama3.2:3b"),
    ("sha256-3b6b58718a439291ffc1953067c4cc16587a23a88b00492c491c3d0787fb206c", 4471999712, "GGUF: olmo2:7b"),
    ("sha256-ea89e3927d5ef671159a1359a22cdd418856c4baa2098e665f1c6eed59973968", 4472020256, "GGUF: olmo-3:7b"),
    ("sha256-96c415656d377afbff962f6cdb2394ab092ccbcbaab4b82525bc4ca800fe8a49", 4683073184, "GGUF: deepseek-r1:7b"),
    ("sha256-60e05f2100071479f596b964f89f510f057ce397ea22f2833a0cfe029bfc2463", 4683074048, "GGUF: qwen2.5-coder:7b"),
    ("sha256-667b0c1932bc6ffc593ed1d03f895bf2dc8dc6df21db3042284a6f4416b06a29", 4920738944, "GGUF: llama3.1:8b"),
    ("sha256-4e30e2665218745ef463f722c0bf86be0cab6ee676320f1cfadf91e989107448", 7162394016, "GGUF: gemma4:e2b"),
    ("sha256-4c27e0f5b5adf02ac956c7322bd2ee7636fe3f45a8512c9aba5385242cb6e09a", 9608338848, "GGUF: gemma4:e4b"),
]

def format_size(bytes_val):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.2f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.2f} TB"

import queue
import threading
import socket
import ctypes
from ctypes import wintypes

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8)
    ]

class WLAN_INTERFACE_INFO(ctypes.Structure):
    _fields_ = [
        ("InterfaceGuid", GUID),
        ("strInterfaceDescription", wintypes.WCHAR * 256),
        ("isState", wintypes.DWORD)
    ]

class WLAN_INTERFACE_INFO_LIST(ctypes.Structure):
    _fields_ = [
        ("dwNumberOfItems", wintypes.DWORD),
        ("dwIndex", wintypes.DWORD),
        ("InterfaceInfo", WLAN_INTERFACE_INFO * 1)
    ]

class WLAN_CONNECTION_PARAMETERS(ctypes.Structure):
    _fields_ = [
        ("wlanConnectionMode", wintypes.DWORD),
        ("strProfile", wintypes.LPCWSTR),
        ("pDot11Ssid", ctypes.c_void_p),
        ("pDesiredBssidList", ctypes.c_void_p),
        ("dot11BssType", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD)
    ]

def reconnect_windows_wifi(force=False):
    try:
        wlanapi = ctypes.windll.wlanapi
        handle = wintypes.HANDLE()
        negotiated = wintypes.DWORD()
        if wlanapi.WlanOpenHandle(2, None, ctypes.byref(negotiated), ctypes.byref(handle)) != 0:
            return False
        pIfList = ctypes.c_void_p()
        if wlanapi.WlanEnumInterfaces(handle, None, ctypes.byref(pIfList)) != 0:
            wlanapi.WlanCloseHandle(handle, None)
            return False
        ifList = WLAN_INTERFACE_INFO_LIST.from_address(pIfList.value)
        if ifList.dwNumberOfItems > 0:
            current_state = ifList.InterfaceInfo[0].isState
            if force or current_state != 1:  # 1 = wlan_interface_state_connected
                guid = ifList.InterfaceInfo[0].InterfaceGuid
                conn_params = WLAN_CONNECTION_PARAMETERS()
                conn_params.wlanConnectionMode = 0
                conn_params.strProfile = "My_2G_Guest1"
                conn_params.dot11BssType = 1
                wlanapi.WlanConnect(handle, ctypes.byref(guid), ctypes.byref(conn_params), None)
                time.sleep(3)
        wlanapi.WlanCloseHandle(handle, None)
        return True
    except Exception:
        return False

def check_wifi_health(silent=False):
    # First verify local adapter is connected
    reconnect_windows_wifi()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.bind((WIFI_BIND_IP, 0))
        s.connect((PI_HOST, 22))
        s.close()
        if not silent:
            print(f"[✓] Wi-Fi link ACTIVE ({WIFI_BIND_IP} -> {PI_HOST}:22)", flush=True)
        return True
    except Exception:
        if not silent:
            print(f"[!] Wi-Fi link waiting for Pi port 22...", flush=True)
        time.sleep(3)
        return False

def transfer_resumable(name, r_size, l_file, label=""):
    remote_path = f"{REMOTE_MODELS}/blobs/{name}"
    attempt = 0
    while True:
        attempt += 1
        curr_offset = os.path.getsize(l_file) if os.path.exists(l_file) else 0

        if curr_offset >= r_size:
            print(f"  [✓] Verified complete [{label}] ({format_size(curr_offset)} == {format_size(r_size)})\n", flush=True)
            return True

        pct = (curr_offset / r_size * 100) if r_size > 0 else 0
        if curr_offset > 0:
            print(f"  [*] Attempt {attempt} [RESUMING from {format_size(curr_offset)} ({pct:.1f}%)] [{label}]...", flush=True)
        else:
            print(f"  [*] Attempt {attempt} [Starting new transfer] [{label}]...", flush=True)

        ssh = None
        sftp = None
        r_file = None
        try:
            reconnect_windows_wifi()

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(PI_HOST, 22, username=PI_USER, key_filename=KEY_PATH, timeout=12, banner_timeout=15)
            ssh.get_transport().set_keepalive(5)
            sftp = ssh.open_sftp()
            sftp.get_channel().settimeout(30.0)
            r_file = sftp.open(remote_path, 'rb')
            if curr_offset > 0:
                r_file.seek(curr_offset)

            start_t = time.time()
            bytes_this_session = 0
            last_reported = 0

            with open(l_file, "ab") as f_out:
                while True:
                    rem_to_read = r_size - (curr_offset + bytes_this_session)
                    if rem_to_read <= 0:
                        break
                    chunk = r_file.read(min(262144, rem_to_read))
                    if not chunk:
                        break
                    f_out.write(chunk)
                    bytes_this_session += len(chunk)
                    now = time.time()
                    if now - last_reported >= 2.0:
                        f_out.flush()
                        total_bytes = curr_offset + bytes_this_session
                        pct = (total_bytes / r_size * 100) if r_size > 0 else 100
                        dt = now - start_t
                        speed = (bytes_this_session / (1024 * 1024)) / (dt if dt > 0 else 1)
                        rem = max(0, r_size - total_bytes)
                        eta_sec = int(rem / (speed * 1024 * 1024)) if speed > 0.01 else -1
                        eta_str = f"{eta_sec // 60}m {eta_sec % 60}s" if eta_sec >= 0 else "calculating..."
                        print(f"    [5G Wi-Fi SFTP] {pct:5.1f}% | {format_size(total_bytes)}/{format_size(r_size)} | Speed: {speed:5.2f} MB/s | ETA: {eta_str}", flush=True)
                        last_reported = now

        except Exception as e:
            err_str = str(e)
            print(f"  [!] SFTP Transfer interrupted: {err_str}", flush=True)
            if "10049" in err_str:
                print("  [!] Wi-Fi IP lost (10049), forcing local Wi-Fi reconnect and DHCP refresh...", flush=True)
                reconnect_windows_wifi(force=True)
                time.sleep(5)
            elif any(k in err_str for k in ["10054", "timed out", "banner", "10038"]):
                print("  [!] Backing off for 15s to allow Pi sshd to clear connection queue...", flush=True)
                time.sleep(15)
            else:
                time.sleep(3)
        finally:
            if r_file:
                try: r_file.close()
                except Exception: pass
            if sftp:
                try: sftp.close()
                except Exception: pass
            if ssh:
                try: ssh.close()
                except Exception: pass

        total_now = os.path.getsize(l_file) if os.path.exists(l_file) else 0
        if total_now >= r_size:
            if total_now > r_size:
                try:
                    with open(l_file, "r+b") as f_fix:
                        f_fix.truncate(r_size)
                except Exception:
                    pass
            print(f"  [✓] Complete [{label}]!\n", flush=True)
            return True

        time.sleep(2)

def main():
    print("=" * 70, flush=True)
    print("  Raspberry Pi 5 Ollama Backup Transporter (PERSISTENT RESUMABLE MODE)")
    print(f"  Source Interface : {WIFI_BIND_IP} (Windows Wi-Fi)")
    print(f"  Target Interface : {PI_HOST} (Raspberry Pi 5 Wi-Fi)")
    print(f"  Wired Subnet     : 172.16.x.x STRICTLY BYPASSED & FORBIDDEN")
    print(f"  Local Destination: {LOCAL_MODELS}")
    print("=" * 70, flush=True)

    os.makedirs(LOCAL_BLOBS, exist_ok=True)
    lock_file_path = os.path.join(LOCAL_MODELS, ".download.lock")
    lock_file = open(lock_file_path, "w")
    try:
        import msvcrt
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
    except Exception:
        print("[!] Another backup instance is already active and locked. Exiting.", flush=True)
        return

    total_files = len(BLOBS_CATALOG)

    for idx, (name, r_size, label) in enumerate(BLOBS_CATALOG, 1):
        l_file = os.path.join(LOCAL_BLOBS, name)
        l_size = os.path.getsize(l_file) if os.path.exists(l_file) else 0

        if l_size >= r_size and r_size > 0:
            if l_size > r_size:
                print(f"[{idx:02d}/{total_files}] [*] File {name} size {l_size} > target {r_size}, safely truncating...", flush=True)
                try:
                    with open(l_file, "r+b") as f_fix:
                        f_fix.truncate(r_size)
                except Exception:
                    pass
            print(f"[{idx:02d}/{total_files}] [✓ Skip Exists] {label:<24} ({format_size(r_size)})", flush=True)
            continue

        print(f"[{idx:02d}/{total_files}] [Wi-Fi Stream] {label:<24} ({format_size(r_size)})", flush=True)
        transfer_resumable(name, r_size, l_file, label)

    print("[🎉] All model transfers processed over pure Wi-Fi!", flush=True)
    try:
        import msvcrt
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        lock_file.close()
    except Exception:
        pass

if __name__ == "__main__":
    main()

