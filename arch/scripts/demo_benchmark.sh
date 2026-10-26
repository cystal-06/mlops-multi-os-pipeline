#!/usr/bin/env bash
# ==============================================================================
# ARCH LINUX MLOPS PIPELINE - HIGH PERFORMANCE BENCHMARK SUITE
# Interactive live stress testing and real-time latency benchmark for thesis defense
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENGINE_PY="${SCRIPT_DIR}/arch/scripts/benchmark_engine.py"
SAMPLE_IMG="${SCRIPT_DIR}/assets/sample_ocr.png"

C_RESET="\033[0m"
C_BOLD="\033[1m"
C_RED="\033[1;31m"
C_GREEN="\033[1;32m"
C_YELLOW="\033[1;33m"
C_BLUE="\033[1;34m"
C_MAGENTA="\033[1;35m"
C_CYAN="\033[1;36m"
C_WHITE="\033[1;37m"

print_banner() {
    clear 2>/dev/null || true
    echo -e "${C_CYAN}${C_BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║       ARCH LINUX MLOPS PIPELINE - LIVE BENCHMARK CONTROLLER          ║"
    echo "║       High-Throughput ASGI Stress Test • AI OCR Engine • Metrics     ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${C_RESET}"
}

check_prerequisites() {
    if ! curl -s -f http://localhost:8080/health >/dev/null 2>&1; then
        echo -e "${C_RED}[✘] CẢNH BÁO: Vi dịch vụ FastAPI chưa khởi động tại http://localhost:8080!${C_RESET}"
        echo -e "${C_YELLOW}[*] Đang kiểm tra stack MLOps...${C_RESET}"
        echo -e "    Gợi ý khởi động: bash ${SCRIPT_DIR}/open_web.sh"
        echo ""
        read -rp "Bấm Enter để quay lại menu..."
        return 1
    fi
    return 0
}

open_grafana() {
    echo -e "${C_YELLOW}[*] Đang mở Grafana và Prometheus trên trình duyệt...${C_RESET}"
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "http://localhost:3000" >/dev/null 2>&1 &
        xdg-open "http://localhost:9090" >/dev/null 2>&1 &
    elif command -v firefox >/dev/null 2>&1; then
        firefox "http://localhost:3000" "http://localhost:9090" >/dev/null 2>&1 &
    fi
    echo -e "${C_GREEN}[✔] Đã mở Grafana (Port 3000) và Prometheus (Port 9090)!${C_RESET}"
    sleep 1
}

# Support command line arguments directly
if [[ $# -gt 0 ]]; then
    case "$1" in
        --auto)
            python3 "${ENGINE_PY}" --requests 500 --concurrency 25
            exit 0
            ;;
        --quick)
            python3 "${ENGINE_PY}" --requests 100 --concurrency 10
            exit 0
            ;;
        --heavy)
            python3 "${ENGINE_PY}" --requests 1000 --concurrency 50
            exit 0
            ;;
        --ocr)
            python3 "${ENGINE_PY}" --mode ocr --requests 20 --concurrency 4 --image "${SAMPLE_IMG}"
            exit 0
            ;;
        --help|-h)
            echo "Usage: $0 [--auto | --quick | --heavy | --ocr]"
            exit 0
            ;;
        *)
            python3 "${ENGINE_PY}" "$@"
            exit 0
            ;;
    esac
fi

# Interactive Menu Loop
while true; do
    print_banner
    echo -e "${C_BOLD}HỆ THỐNG MỤC TIÊU:${C_RESET}"
    echo -e "  • FastAPI Serving  : ${C_GREEN}http://localhost:8080${C_RESET} (Trạng thái: $(curl -s -f http://localhost:8080/health >/dev/null 2>&1 && echo -e "${C_GREEN}ONLINE${C_RESET}" || echo -e "${C_RED}OFFLINE${C_RESET}"))"
    echo -e "  • Prometheus Server: ${C_BLUE}http://localhost:9090${C_RESET}"
    echo -e "  • Grafana Dashboard: ${C_BLUE}http://localhost:3000${C_RESET}"
    echo ""
    echo -e "${C_BOLD}CHỌN KỊCH BẢN BẮN TẢI BENCHMARK:${C_RESET}"
    echo -e "  ${C_GREEN}[1]${C_RESET} ${C_BOLD}Kiểm chứng nhanh${C_RESET} (100 Requests, Concurrency: 10)  ${C_DIM}~1 giây${C_RESET}"
    echo -e "  ${C_GREEN}[2]${C_RESET} ${C_BOLD}BENCHMARK CHUẨN ĐỒ ÁN - SLIDE 10${C_RESET} (500 Requests, Concurrency: 25) ${C_YELLOW}★ Khuyên dùng khi thuyết trình${C_RESET}"
    echo -e "  ${C_GREEN}[3]${C_RESET} ${C_BOLD}Bắn tải cực hạn Stress Test${C_RESET} (1,000 Requests, Concurrency: 50) ${C_DIM}~3 giây${C_RESET}"
    echo -e "  ${C_GREEN}[4]${C_RESET} ${C_BOLD}Stress Test AI OCR Thực Tế${C_RESET} (20 Ảnh AI Scan, Concurrency: 4) ${C_MAGENTA}CPU Neural Network${C_RESET}"
    echo -e "  ${C_GREEN}[5]${C_RESET} ${C_BOLD}Tùy chỉnh số lượng${C_RESET} (Nhập số Requests và luồng tự do)"
    echo -e "  ${C_CYAN}[6]${C_RESET} Mở trình duyệt xem biểu đồ Grafana LIVE (Port 3000)"
    echo -e "  ${C_RED}[0]${C_RESET} Thoát"
    echo ""
    read -rp ">> Lựa chọn của bạn [0-6]: " choice

    case "${choice}" in
        1)
            check_prerequisites && python3 "${ENGINE_PY}" --requests 100 --concurrency 10
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        2)
            check_prerequisites && python3 "${ENGINE_PY}" --requests 500 --concurrency 25
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        3)
            check_prerequisites && python3 "${ENGINE_PY}" --requests 1000 --concurrency 50
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        4)
            check_prerequisites && python3 "${ENGINE_PY}" --mode ocr --requests 20 --concurrency 4 --image "${SAMPLE_IMG}"
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        5)
            echo ""
            read -rp ">> Nhập tổng số requests [ví dụ: 300]: " req_input
            read -rp ">> Nhập mức đồng thời concurrency [ví dụ: 20]: " conc_input
            req_input="${req_input:-300}"
            conc_input="${conc_input:-20}"
            check_prerequisites && python3 "${ENGINE_PY}" --requests "${req_input}" --concurrency "${conc_input}"
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        6)
            open_grafana
            ;;
        0)
            echo -e "\n${C_CYAN}Cảm ơn bạn! Chúc buổi báo cáo đồ án ngày mai thành công rực rỡ! 🎉${C_RESET}\n"
            exit 0
            ;;
        *)
            echo -e "${C_RED}Lựa chọn không hợp lệ! Vui lòng chọn từ 0 đến 6.${C_RESET}"
            sleep 1
            ;;
    esac
done
