#!/usr/bin/env bash

set -euo pipefail
set -E

readonly COLOR_RESET="\033[0m"
readonly COLOR_RED="\033[1;31m"
readonly COLOR_GREEN="\033[1;32m"
readonly COLOR_YELLOW="\033[1;33m"
readonly COLOR_BLUE="\033[1;34m"
readonly COLOR_CYAN="\033[1;36m"
readonly COLOR_BOLD="\033[1m"

log_info() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} [$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log_success() {
    echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_RESET} [$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log_warn() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} [$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} [$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

log_step() {
    echo -e "\n${COLOR_CYAN}${COLOR_BOLD}>>> $*${COLOR_RESET}"
}

error_trap() {
    local exit_code=$?
    local line_no=$1
    local command=$2
    log_error "Command failed at line ${line_no} with exit code ${exit_code}: '${command}'"
    exit "${exit_code}"
}

trap 'error_trap "$LINENO" "$BASH_COMMAND"' ERR

require_root() {
    if [[ "${EUID}" -ne 0 ]]; then
        log_error "This script must be executed with root privileges (sudo)."
        exit 1
    fi
}

require_non_root() {
    if [[ "${EUID}" -eq 0 ]]; then
        log_error "This script should be executed as a non-root user (e.g., mlops)."
        exit 1
    fi
}

require_ubuntu() {
    source /etc/os-release
    if [[ "$ID" != ubuntu || ! "$VERSION_ID" =~ ^(22\.04|24\.04)$ ]]; then
        log_error "Use a dedicated Ubuntu Server 22.04/24.04 LTS VM."
        exit 1
    fi
}

backup_path() {
    local path=$1
    mkdir -p "${STATE_DIR}/files$(dirname "$path")"
    rm -rf -- "${STATE_DIR}/files${path}"
    if [[ -e "$path" || -L "$path" ]]; then
        cp -a "$path" "${STATE_DIR}/files${path}"
    fi
}

restore_path() {
    local path=$1
    rm -rf -- "$path"
    if [[ -e "${STATE_DIR}/files${path}" || -L "${STATE_DIR}/files${path}" ]]; then
        mkdir -p "$(dirname "$path")"
        cp -a "${STATE_DIR}/files${path}" "$path"
    fi
}
