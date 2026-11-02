#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"
require_root
require_ubuntu
STATE_DIR=/var/lib/mlops-infra/hardening
if [[ ! -f "$STATE_DIR/ready" ]]; then
    log_info "No hardening backup; nothing to restore."
    exit 0
fi
if [[ -n "${SSH_CONNECTION:-}" ]]; then
    log_error "Run rollback from the VMware console."
    exit 1
fi
ufw disable
for path in /etc/ssh/sshd_config /etc/ssh/mlops_hardened.conf \
    /etc/ssh/sshd_config.d/99-mlops-hardened.conf /etc/ufw /etc/default/ufw; do
    restore_path "$path"
done
/usr/sbin/sshd -t
if grep -q '^Status: active' "$STATE_DIR/ufw-status"; then
    ufw --force enable
else
    ufw disable
fi
systemctl stop ssh.service
if systemctl cat ssh.socket >/dev/null 2>&1; then
    systemctl stop ssh.socket
    if grep -qx enabled "$STATE_DIR/socket-enabled"; then
        systemctl enable ssh.socket
    else
        systemctl disable ssh.socket
    fi
fi
if grep -qx enabled "$STATE_DIR/ssh-enabled"; then
    systemctl enable ssh.service
else
    systemctl disable ssh.service
fi
systemctl daemon-reload
if grep -qx active "$STATE_DIR/socket-active"; then
    systemctl start ssh.socket
fi
if grep -qx active "$STATE_DIR/ssh-active"; then
    systemctl start ssh.service
fi
log_success "Restored saved SSH/UFW state. Kept mlops account and its files."
log_info "Backup retained; reruns restore the same baseline. Packages are retained."
