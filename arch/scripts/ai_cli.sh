#!/usr/bin/env bash

set -euo pipefail

COLOR_RESET="\033[0m"
COLOR_RED="\033[1;31m"
COLOR_GREEN="\033[1;32m"
COLOR_YELLOW="\033[1;33m"
COLOR_BLUE="\033[1;34m"
COLOR_CYAN="\033[1;36m"
COLOR_BOLD="\033[1m"
COLOR_MAGENTA="\033[1;35m"

print_header() {
    clear
    echo -e "${COLOR_CYAN}${COLOR_BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║       ARCH LINUX MLOPS TERMINAL - AI OCR VISION INTERFACE            ║"
    echo "║       FastAPI Inference • Tesseract Engine • Rootless Docker         ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo -e "${COLOR_RESET}"
}

scan_single_image() {
    local img_path="$1"
    if [[ ! -f "${img_path}" ]]; then
        echo -e "${COLOR_RED}[✘] File không tồn tại:${COLOR_RESET} ${img_path}"
        return 1
    fi

    echo -e "${COLOR_BLUE}[*] File Target :${COLOR_RESET} ${COLOR_BOLD}${img_path}${COLOR_RESET} ($(du -h "${img_path}" | awk '{print $1}'))"
    echo -e "${COLOR_YELLOW}[>>>] AI Đang Quét Và Nhận Diện Chữ...${COLOR_RESET}"

    local start_time=$(date +%s%N)
    local response=$(curl -s -X POST "http://localhost:8080/v1/ocr/scan" \
        -H "Accept: application/json" \
        -F "file=@${img_path}")
    local end_time=$(date +%s%N)
    local duration=$(( (end_time - start_time) / 1000000 ))

    python3 -c '
import sys, json

try:
    data = json.loads(sys.argv[1])
except Exception:
    print("\033[1;31m[✘] Lỗi kết nối tới AI API!\033[0m")
    sys.exit(1)

if data.get("status") == "success":
    dur = sys.argv[2]
    print(f"\033[1;32m[✔] QUÉT THÀNH CÔNG TRONG {dur} ms!\033[0m")
    print("\033[1;34m" + "─"*70 + "\033[0m")
    print(f"  • Model Engine  : \033[1;35m{data.get(\"model_engine\")}\033[0m")
    print(f"  • Độ Phân Giải  : {data.get(\"image_resolution\")}")
    print(f"  • Số Từ Đọc Được: \033[1;33m{data.get(\"word_count\")}\033[0m từ")
    print(f"  • Tổng Ký Tự    : \033[1;33m{data.get(\"char_count\")}\033[0m ký tự")
    print("\033[1;34m" + "─"*70 + "\033[0m")
    print("\033[1;32m[NỘI DUNG VĂN BẢN TRONG ẢNH]:\033[0m\n")
    print(f"\033[1m{data.get(\"extracted_text\")}\033[0m\n")
    print("\033[1;36m" + "═"*70 + "\033[0m")
else:
    print(f"\033[1;31m[✘] Lỗi:\033[0m {data.get(\"detail\", \"Unknown error\")}")
' "${response}" "${duration}"
}

while true; do
    print_header
    echo -e "${COLOR_BOLD}CHỌN CHỨC NĂNG DEMO:${COLOR_RESET}"
    echo -e "  ${COLOR_GREEN}[1]${COLOR_RESET} Nhập đường dẫn 1 file ảnh bất kỳ để AI quét"
    echo -e "  ${COLOR_GREEN}[2]${COLOR_RESET} Quét ảnh mẫu test có sẵn trong hệ thống"
    echo -e "  ${COLOR_GREEN}[3]${COLOR_RESET} Kiểm tra trạng thái AI Model (/health)"
    echo -e "  ${COLOR_GREEN}[4]${COLOR_RESET} Thoát"
    echo ""
    read -rp ">> Nhập lựa chọn [1-4]: " choice

    case "${choice}" in
        1)
            echo ""
            read -rp ">> Nhập đường dẫn file ảnh (.png/.jpg): " user_img
            echo ""
            scan_single_image "${user_img}"
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        2)
            echo ""
            SAMPLE_IMG="/home/nguyencongduc/.gemini/antigravity/brain/981bbd72-00b6-4bbe-938a-a6d35d7bb69e/.user_uploaded/media_1792421487464.png"
            scan_single_image "${SAMPLE_IMG}"
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        3)
            echo ""
            echo -e "${COLOR_YELLOW}[*] Kiểm tra AI Health Check:${COLOR_RESET}"
            curl -s http://localhost:8080/health | python3 -m json.tool || echo "Service offline"
            echo ""
            read -rp "Bấm Enter để tiếp tục..."
            ;;
        4)
            echo -e "\n${COLOR_CYAN}Tạm biệt! Chúc bạn thuyết trình 10/10!${COLOR_RESET}\n"
            exit 0
            ;;
        *)
            echo -e "${COLOR_RED}Lựa chọn không hợp lệ!${COLOR_RESET}"
            sleep 1
            ;;
    esac
done
