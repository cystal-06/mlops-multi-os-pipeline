#!/usr/bin/env bash
# ==============================================================================
# VKU MLOps AI Vision Cockpit Launcher
# Starts the interactive visual web dashboard and opens it in the browser
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8888
COCKPIT_PY="${SCRIPT_DIR}/web_cockpit.py"

C_CYAN="\033[1;36m"
C_GREEN="\033[1;32m"
C_YELLOW="\033[1;33m"
C_RESET="\033[0m"
C_BOLD="\033[1m"

echo -e "${C_CYAN}${C_BOLD}"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║          VKU MLOPS AI VISION COCKPIT — LAUNCH CONTROLLER             ║"
echo "║        Interactive Visual Dashboard • Real-Time AI Inference         ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo -e "${C_RESET}"

# Ensure web_cockpit is active
if ! curl -s -f http://localhost:${PORT}/ >/dev/null 2>&1; then
    echo -e "${C_YELLOW}[*] Đang khởi động AI Vision Cockpit Server qua systemd...${C_RESET}"
    systemctl --user start mlops-web-cockpit.service 2>/dev/null || nohup python3 "${COCKPIT_PY}" >/tmp/web_cockpit.log 2>&1 &
    sleep 1.0
fi

if curl -s -f http://localhost:${PORT}/ >/dev/null 2>&1; then
    echo -e "${C_GREEN}[✔] AI Vision Cockpit Server đã sẵn sàng trên cổng :${PORT}!${C_RESET}"
else
    echo -e "\033[1;31m[✘] Lỗi khởi động! Kiểm tra log tại /tmp/web_cockpit.log hoặc journalctl --user -u mlops-web-cockpit\033[0m"
    exit 1
fi

TARGET_URL="http://localhost:${PORT}"
echo -e "${C_CYAN}[*] Đang mở trình duyệt tại: ${C_BOLD}${TARGET_URL}${C_RESET}"

if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${TARGET_URL}" >/dev/null 2>&1 &
elif command -v firefox >/dev/null 2>&1; then
    firefox "${TARGET_URL}" >/dev/null 2>&1 &
fi

echo ""
echo -e "${C_GREEN}${C_BOLD}========================================================================${C_RESET}"
echo -e "  👉 Giao diện Web Trực Quan đã sẵn sàng tại: ${C_YELLOW}${C_BOLD}${TARGET_URL}${C_RESET}"
echo -e "  👉 Bạn có thể kéo thả ảnh, bấm chọn 3 mẫu test và bắn tải trực tiếp!"
echo -e "${C_GREEN}${C_BOLD}========================================================================${C_RESET}"
echo ""
