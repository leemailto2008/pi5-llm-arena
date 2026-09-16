# f:\12_prj_raspi5\benchmark\switch_wifi_5g.py
import sys
import time
import subprocess
import paramiko

PI_HOST = "192.168.50.228"
PI_USER = "pi"
KEY_PATH = r"C:\Users\Andrew\.ssh\id_rsa_pi5"
WIFI_5G_SSID = "My_5G_Guest1"
WIFI_5G_PWD = "my53943839"

def switch_pi5():
    print(f"[*] Connecting to Pi 5 ({PI_HOST})...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(PI_HOST, 22, username=PI_USER, key_filename=KEY_PATH, timeout=10)

    # Command to connect to 5G with fallback to 2G if connection fails
    cmd = (
        f"echo andrew | sudo -S nmcli dev wifi connect '{WIFI_5G_SSID}' password '{WIFI_5G_PWD}' > /home/pi/wifi_5g.log 2>&1; "
        "if [ $? -eq 0 ]; then "
        "  echo '5G_CONNECTED'; "
        "  echo on | echo andrew | sudo -S tee /sys/class/net/wlan0/device/power/control > /dev/null 2>&1; "
        "else "
        "  echo '5G_FAILED_FALLBACK'; "
        "  echo andrew | sudo -S nmcli connection up 'netplan-wlan0-My_2G_Guest1' > /dev/null 2>&1; "
        "fi"
    )

    print(f"[*] Triggering Pi 5 switch to '{WIFI_5G_SSID}'...")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    try:
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        print(f"[✓] Pi 5 Result:\n{out.strip()}\n{err.strip()}")
    except Exception as e:
        print(f"[*] Note: Connection closed during Wi-Fi re-association (expected): {e}")
    finally:
        try: ssh.close()
        except: pass

def switch_windows():
    print(f"[*] Switching Windows host Wi-Fi to '{WIFI_5G_SSID}'...")
    res = subprocess.run(["netsh", "wlan", "connect", f"name={WIFI_5G_SSID}"], capture_output=True, text=True)
    print(res.stdout.strip())
    print("[*] Waiting 6 seconds for DHCP assignment...")
    time.sleep(6)

def verify():
    print("[*] Verifying connectivity to Pi 5...")
    res = subprocess.run(["ping", "-n", "4", PI_HOST], capture_output=True, text=True)
    print(res.stdout)

if __name__ == "__main__":
    switch_pi5()
    switch_windows()
    verify()
