#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"

require_root

DEPLOY_USER="mlops"

log_step "PHASE 1: Disabling UFW Firewall"
if which ufw &>/dev/null; then
    ufw --force reset || true
    ufw disable || true
    log_success "UFW firewall reset and disabled."
fi

log_step "PHASE 2: Restoring SSH Configuration"
SSHD_HARDENED_FILE="/etc/ssh/sshd_config.d/99-mlops-hardened.conf"

if [[ -f "${SSHD_HARDENED_FILE}" ]]; then
    rm -f "${SSHD_HARDENED_FILE}"
    if sshd -t; then
        systemctl restart ssh || systemctl restart sshd
        log_success "SSH daemon reverted to default port."
    fi
fi

log_step "PHASE 3: Cleaning up Deploy User ('${DEPLOY_USER}')"
if id "${DEPLOY_USER}" &>/dev/null; then
    echo -e "${COLOR_YELLOW}[PROMPT] Remove user '${DEPLOY_USER}' and /home/${DEPLOY_USER}? [y/N]: ${COLOR_RESET}\c"
    read -r response
    if [[ "${response}" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        pkill -u "${DEPLOY_USER}" || true
        userdel -r "${DEPLOY_USER}" 2>/dev/null || userdel "${DEPLOY_USER}"
        log_success "User '${DEPLOY_USER}' removed."
    fi
fi

log_step "ROLLBACK COMPLETE"
