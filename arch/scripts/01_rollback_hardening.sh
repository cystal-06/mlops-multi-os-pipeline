#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"

require_root

DEPLOY_USER="mlops"

log_step "PHASE 1: Reverting nftables Firewall"
if systemctl is-active --quiet nftables; then
    log_info "Stopping and disabling nftables service..."
    systemctl disable --now nftables
    nft flush ruleset || true
    log_success "nftables disabled and ruleset flushed."
else
    log_info "nftables service is not running. Skipping."
fi

if [[ -f /etc/nftables.conf ]]; then
    log_info "Cleaning up /etc/nftables.conf..."
    cat << 'EOF' > /etc/nftables.conf
#!/usr/sbin/nft -f
flush ruleset
table inet filter {
    chain input { type filter hook input priority filter; policy accept; }
    chain forward { type filter hook forward priority filter; policy accept; }
    chain output { type filter hook output priority filter; policy accept; }
}
EOF
    log_success "Reset /etc/nftables.conf to default accept-all state."
fi

log_step "PHASE 2: Restoring SSH Configuration"
SSHD_HARDENED_FILE="/etc/ssh/sshd_config.d/99-mlops-hardened.conf"

if [[ -f "${SSHD_HARDENED_FILE}" ]]; then
    log_info "Removing hardened SSH configuration: ${SSHD_HARDENED_FILE}"
    rm -f "${SSHD_HARDENED_FILE}"
    
    if sshd -t; then
        log_info "Reloading sshd back to original defaults..."
        systemctl restart sshd
        log_success "SSH daemon reverted to system defaults (Port 22, etc.)."
    else
        log_warn "sshd test encountered an issue. Please inspect /etc/ssh/sshd_config."
    fi
else
    log_info "No hardened SSH drop-in configuration found. Skipping."
fi

log_step "PHASE 3: Reverting Sysctl Kernel Parameters"
SYSCTL_DST="/etc/sysctl.d/99-mlops.conf"

if [[ -f "${SYSCTL_DST}" ]]; then
    log_info "Removing ${SYSCTL_DST}..."
    rm -f "${SYSCTL_DST}"
    log_info "Reloading system sysctl defaults..."
    sysctl --system > /dev/null
    log_success "Sysctl parameters reverted."
else
    log_info "Sysctl drop-in not found. Skipping."
fi

log_step "PHASE 4: Isolated User Cleanup ('${DEPLOY_USER}')"
if id "${DEPLOY_USER}" &>/dev/null; then
    echo -e "${COLOR_YELLOW}[PROMPT] Do you want to completely remove user '${DEPLOY_USER}' and /home/${DEPLOY_USER}? [y/N]: ${COLOR_RESET}\c"
    read -r response
    if [[ "${response}" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        log_info "Killing lingering processes for ${DEPLOY_USER}..."
        loginctl disable-linger "${DEPLOY_USER}" 2>/dev/null || true
        pkill -u "${DEPLOY_USER}" || true
        log_info "Deleting user '${DEPLOY_USER}' and home directory..."
        userdel -r "${DEPLOY_USER}" 2>/dev/null || userdel "${DEPLOY_USER}"
        log_success "User '${DEPLOY_USER}' has been removed."
    else
        log_info "User '${DEPLOY_USER}' preserved."
    fi
fi

if [[ -f /etc/sudoers.d/10-wheel ]]; then
    rm -f /etc/sudoers.d/10-wheel
fi

log_step "ROLLBACK COMPLETE"
log_success "System has been cleanly restored to its original state!"
