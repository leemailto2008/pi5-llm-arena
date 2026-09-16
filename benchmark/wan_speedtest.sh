#!/bin/bash
# f:\12_prj_raspi5\benchmark\wan_speedtest.sh
set -e

echo "=========================================================================="
echo "      RASPBERRY PI 5 INTERNET (WAN) CONNECTIVITY & SPEED BENCHMARK"
echo "=========================================================================="
echo "Device: $(hostname) | Date: $(date)"
echo "Active Wi-Fi SSID: $(nmcli -t -f active,ssid dev wifi | grep '^yes:' | cut -d: -f2)"
echo "Internal IP: $(ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')"
echo ""

echo "--------------------------------------------------------------------------"
echo "  1. LATENCY & PACKET LOSS TO MAJOR DNS / CDNs (ICMP 10 Packets)"
echo "--------------------------------------------------------------------------"
test_ping() {
    local target=$1
    local name=$2
    printf "%-25s " "$name ($target):"
    res=$(ping -c 6 -i 0.2 "$target" 2>/dev/null | tail -n 2)
    loss=$(echo "$res" | grep -oP '\d+(?=% packet loss)')
    rtt=$(echo "$res" | grep -oP 'rtt min/avg/max/mdev = \K[0-9./]+' || echo "N/A/N/A/N/A/N/A")
    avg=$(echo "$rtt" | cut -d/ -f2)
    min=$(echo "$rtt" | cut -d/ -f1)
    max=$(echo "$rtt" | cut -d/ -f3)
    echo "Loss: ${loss}% | Min: ${min}ms | Avg: ${avg}ms | Max: ${max}ms"
}

test_ping "168.95.1.1" "Chunghwa Telecom DNS"
test_ping "8.8.8.8" "Google Public DNS"
test_ping "1.1.1.1" "Cloudflare DNS"
test_ping "192.168.50.1" "Local Wi-Fi Gateway"
echo ""

echo "--------------------------------------------------------------------------"
echo "  2. HTTP/HTTPS CONNECTION TIME BREAKDOWN (Cloudflare CDN)"
echo "--------------------------------------------------------------------------"
curl -s -w \
"DNS Lookup Time     : %{time_namelookup} s\n\
TCP Connect Time    : %{time_connect} s\n\
TLS Handshake Time  : %{time_appconnect} s\n\
Time to First Byte  : %{time_starttransfer} s\n\
Total Request Time  : %{time_total} s\n" \
-o /dev/null "https://speed.cloudflare.com/"
echo ""

echo "--------------------------------------------------------------------------"
echo "  3. WAN DOWNLOAD SPEED TEST (Multi-CDN Benchmark)"
echo "--------------------------------------------------------------------------"
test_download() {
    local url=$1
    local label=$2
    local size_mb=$3
    echo -n "[*] Testing $label (${size_mb} MB)... "
    res=$(curl -s -w "%{speed_download};%{time_total};%{size_download}" -o /dev/null --max-time 30 "$url" || echo "0;0;0")
    speed_bps=$(echo "$res" | cut -d';' -f1 | cut -d'.' -f1)
    elapsed=$(echo "$res" | cut -d';' -f2)
    downloaded=$(echo "$res" | cut -d';' -f3)
    
    if [ -n "$speed_bps" ] && [ "$speed_bps" -gt 0 ]; then
        speed_kbs=$(awk "BEGIN {printf \"%.2f\", $speed_bps / 1024}")
        speed_mbps=$(awk "BEGIN {printf \"%.2f\", ($speed_bps * 8) / 1000000}")
        dl_mb=$(awk "BEGIN {printf \"%.2f\", $downloaded / 1048576}")
        echo "Done!"
        echo "    -> Downloaded: ${dl_mb} MB in ${elapsed}s"
        echo "    -> Speed: ${speed_kbs} KB/s  (${speed_mbps} Mbps)"
    else
        echo "Failed or Timed out!"
    fi
}

# 1. Cloudflare 5MB
test_download "https://speed.cloudflare.com/__down?bytes=5000000" "Cloudflare Edge CDN" 5

# 2. GitHub Raw Release File (2MB)
test_download "https://raw.githubusercontent.com/curl/curl/master/docs/THANKS" "GitHub CDN" 1

echo ""
echo "--------------------------------------------------------------------------"
echo "  4. WAN UPLOAD SPEED TEST (HTTPS POST to Speedtest Endpoint)"
echo "--------------------------------------------------------------------------"
echo -n "[*] Generating 2 MB payload and testing upload speed... "
# Generate 2MB payload
dd if=/dev/urandom of=/tmp/upload_test.bin bs=1M count=2 status=none
up_res=$(curl -s -w "%{speed_upload};%{time_total}" -o /dev/null --max-time 30 -X POST -H "Content-Type: application/octet-stream" --data-binary "@/tmp/upload_test.bin" "https://speed.cloudflare.com/__up" || echo "0;0")
rm -f /tmp/upload_test.bin

up_bps=$(echo "$up_res" | cut -d';' -f1 | cut -d'.' -f1)
up_elapsed=$(echo "$up_res" | cut -d';' -f2)
if [ -n "$up_bps" ] && [ "$up_bps" -gt 0 ]; then
    up_kbs=$(awk "BEGIN {printf \"%.2f\", $up_bps / 1024}")
    up_mbps=$(awk "BEGIN {printf \"%.2f\", ($up_bps * 8) / 1000000}")
    echo "Done!"
    echo "    -> Upload Speed: ${up_kbs} KB/s  (${up_mbps} Mbps) [Elapsed: ${up_elapsed}s]"
else
    echo "Upload Test Failed or Timed out."
fi

echo ""
echo "=========================================================================="
echo "                         BENCHMARK SUMMARY"
echo "=========================================================================="
