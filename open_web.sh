#!/usr/bin/env bash
# Tiện ích tự động mở toàn bộ các trang Web UI của MLOps Stack trên trình duyệt

echo "[*] Đang mở các giao diện Web của đồ án MLOps trên trình duyệt..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! pgrep -f "python3.*web_cockpit.py" >/dev/null 2>&1; then
    nohup python3 "${SCRIPT_DIR}/web_cockpit.py" >/tmp/web_cockpit.log 2>&1 &
    sleep 0.8
fi

URLS=(
    "http://localhost:8888"
    "http://localhost:8080/docs"
    "http://localhost:5000"
    "http://localhost:3000"
    "http://localhost:9090"
)

for url in "${URLS[@]}"; do
    echo "  -> Đang mở: ${url}"
    xdg-open "${url}" >/dev/null 2>&1 || firefox "${url}" >/dev/null 2>&1 &
    sleep 0.5
done

echo "[✔] Đã mở thành công toàn bộ các tab Web UI!"
