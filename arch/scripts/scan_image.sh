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

print_banner() {
    clear 2>/dev/null || true
    echo -e "${COLOR_CYAN}${COLOR_BOLD}"
    echo "========================================================================"
    echo "       ARCH LINUX MLOPS OCR INFERENCE SCANNER (TERMINAL CLI)            "
    echo "       Underlying Engine: Tesseract-OCR + FastAPI + Rootless Docker     "
    echo "========================================================================"
    echo -e "${COLOR_RESET}"
}

if [[ $# -lt 1 ]]; then
    print_banner
    echo -e "${COLOR_YELLOW}[USAGE]:${COLOR_RESET} $0 <duong_dan_file_anh>"
    echo -e "${COLOR_BLUE}[EXAMPLE]:${COLOR_RESET} $0 /home/nguyencongduc/sample_text.png"
    echo ""
    exit 1
fi

IMAGE_PATH="$1"

if [[ ! -f "${IMAGE_PATH}" ]]; then
    echo -e "${COLOR_RED}[ERROR]: File không tồn tại: '${IMAGE_PATH}'${COLOR_RESET}"
    exit 1
fi

print_banner
echo -e "${COLOR_BLUE}[*] Target Image    :${COLOR_RESET} ${COLOR_BOLD}${IMAGE_PATH}${COLOR_RESET}"
echo -e "${COLOR_BLUE}[*] File Size       :${COLOR_RESET} $(du -h "${IMAGE_PATH}" | awk '{print $1}')"
echo -e "${COLOR_BLUE}[*] Endpoint Target :${COLOR_RESET} http://localhost:8080/v1/ocr/scan"
echo ""
echo -e "${COLOR_YELLOW}[>>>] Uploading & Performing AI OCR Scanning...${COLOR_RESET}"

START_TIME=$(date +%s%N)

RESPONSE=$(curl -s -X POST "http://localhost:8080/v1/ocr/scan" \
    -H "Accept: application/json" \
    -F "file=@${IMAGE_PATH}")

END_TIME=$(date +%s%N)
DURATION_MS=$(( (END_TIME - START_TIME) / 1000000 ))

# Parse JSON using built-in python3 (no external jq dependency needed)
python3 -c '
import sys, json

try:
    data = json.loads(sys.argv[1])
except Exception as e:
    print(f"\033[1;31m[✘] Error parsing response:\033[0m {sys.argv[1]}")
    sys.exit(1)

if data.get("status") == "success":
    duration = sys.argv[2]
    engine = data.get("model_engine", "Unknown")
    ver = data.get("model_version", "")
    res = data.get("image_resolution", "Unknown")
    wcount = data.get("word_count", 0)
    ccount = data.get("char_count", 0)
    text = data.get("extracted_text", "")

    print(f"\033[1;32m[✔] SCAN COMPLETED SUCCESSFULLY IN {duration} ms!\033[0m")
    print("\033[1;36m------------------------------------------------------------------------\033[0m")
    print(f"  • Engine Model   : \033[1;35m{engine}\033[0m ({ver})")
    print(f"  • Image Res      : {res}")
    print(f"  • Words Detected : \033[1m{wcount}\033[0m")
    print(f"  • Characters     : \033[1m{ccount}\033[0m")
    print("\033[1;36m------------------------------------------------------------------------\033[0m")
    print("\033[1;32m\033[1m[EXTRACTED TEXT FROM IMAGE]:\033[0m\n")
    print(f"\033[1m{text}\033[0m\n")
    print("\033[1;36m========================================================================\033[0m")
else:
    print(f"\033[1;31m[✘] OCR SCAN FAILED:\033[0m {data}")
' "${RESPONSE}" "${DURATION_MS}"
