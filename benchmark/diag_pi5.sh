#!/bin/bash
# f:\12_prj_raspi5\benchmark\diag_pi5.sh
set -e

echo "================================================================="
echo "  RASPBERRY PI 5 COMPREHENSIVE PERFORMANCE & NETWORK DIAGNOSTIC"
echo "================================================================="
echo "Host: $(hostname) | Kernel: $(uname -r) | Date: $(date)"
echo ""

echo "-----------------------------------------------------------------"
echo "  [Test 1] ETHERNET (eth0) PHY & HARDWARE STATE"
echo "-----------------------------------------------------------------"
ip link show eth0
echo -n "Carrier Status: "
cat /sys/class/net/eth0/carrier 2>/dev/null || echo "0 (No physical carrier detected)"
echo -n "Operstate: "
cat /sys/class/net/eth0/operstate 2>/dev/null || echo "unknown"
echo ""
echo "Ethtool Diagnostics:"
if command -v ethtool >/dev/null 2>&1; then
    sudo ethtool eth0 2>/dev/null | grep -E "(Speed|Duplex|Port|Supported link modes|Auto-negotiation|Link detected)" || ethtool eth0 2>/dev/null || echo "Unable to query ethtool"
else
    echo "ethtool not installed"
fi
echo ""
echo "Recent Kernel Messages for Ethernet:"
dmesg | grep -iE "(eth0|bcm54|macb|carrier)" | tail -n 8 || true
echo ""

echo "-----------------------------------------------------------------"
echo "  [Test 2] WI-FI (wlan0) RF LINK, PHY & NEGOTIATION RATE"
echo "-----------------------------------------------------------------"
if command -v iw >/dev/null 2>&1; then
    iw dev wlan0 link
    echo ""
    echo "Wi-Fi Dev Info:"
    iw dev wlan0 info
fi
echo ""
echo "NetworkManager Wi-Fi Status:"
nmcli -f IN-USE,SSID,BSSID,CHAN,FREQ,RATE,SIGNAL,BARS,SECURITY dev wifi | grep '^\*' || nmcli dev wifi list | head -n 5
echo ""
echo "Current Routing & Interface IP:"
ip -4 addr show wlan0 | grep inet || true
ip route | head -n 5
echo ""

echo "-----------------------------------------------------------------"
echo "  [Test 3] LATENCY, JITTER & PACKET LOSS (ICMP)"
echo "-----------------------------------------------------------------"
echo "1. Ping Gateway (192.168.50.1) - 5 packets:"
ping -c 5 -i 0.2 192.168.50.1 || true
echo ""
echo "2. Ping Windows Host (192.168.50.3) - 5 packets:"
ping -c 5 -i 0.2 192.168.50.3 || true
echo ""

echo "-----------------------------------------------------------------"
echo "  [Test 4] STORAGE READ BENCHMARK (Disk/SD/NVMe I/O)"
echo "-----------------------------------------------------------------"
BLOB_DIR="/home/pi/.ollama/models/blobs"
if [ -d "$BLOB_DIR" ]; then
    SAMPLE_BLOB=$(ls -S "$BLOB_DIR"/sha256-* 2>/dev/null | head -n 1)
    if [ -n "$SAMPLE_BLOB" ]; then
        echo "Target Test File: $(basename "$SAMPLE_BLOB")"
        echo "File Size: $(du -h "$SAMPLE_BLOB" | cut -f1)"
        echo "Clearing drop_caches before read test..."
        echo 3 | sudo tee /proc/sys/vm/drop_caches >/dev/null 2>&1 || true
        echo "Executing 1 GB Direct Sequential Read Benchmark..."
        dd if="$SAMPLE_BLOB" of=/dev/null bs=4M count=256 status=progress 2>&1
    else
        echo "No blobs found in $BLOB_DIR"
    fi
else
    echo "Directory $BLOB_DIR does not exist"
fi
echo ""

echo "-----------------------------------------------------------------"
echo "  [Test 5] CPU CRYPTO THROUGHPUT (ARMv8 Neon / Crypto Extensions)"
echo "-----------------------------------------------------------------"
echo "OpenSSL ChaCha20-Poly1305 Benchmark (2s):"
openssl speed -seconds 2 -evp chacha20-poly1305 2>&1 | grep -A 1 "type" || true
echo ""
echo "OpenSSL AES-128-GCM Benchmark (2s):"
openssl speed -seconds 2 -evp aes-128-gcm 2>&1 | grep -A 1 "type" || true
echo ""

echo "================================================================="
echo "  DIAGNOSTIC COMPLETED SUCCESSFULLY"
echo "================================================================="
