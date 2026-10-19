#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"
require_root
require_ubuntu
STATE_DIR=/var/lib/mlops-infra/hardening
SSH_DROPIN=/etc/ssh/mlops_hardened.conf

if [[ -n "${SSH_CONNECTION:-}" ]]; then
    log_error "Run from the VMware console, not over SSH (the SSH port will change)."
    exit 1
fi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y openssh-server ufw
install -d -m 0700 "$STATE_DIR"
if [[ ! -f "$STATE_DIR/ready" ]]; then
    for path in /etc/ssh/sshd_config "$SSH_DROPIN" \
        /etc/ssh/sshd_config.d/99-mlops-hardened.conf /etc/ufw /etc/default/ufw; do
        backup_path "$path"
    done
    systemctl is-enabled ssh.service > "$STATE_DIR/ssh-enabled" 2>/dev/null || true
    systemctl is-active ssh.service > "$STATE_DIR/ssh-active" 2>/dev/null || true
    systemctl is-enabled ssh.socket > "$STATE_DIR/socket-enabled" 2>/dev/null || true
    systemctl is-active ssh.socket > "$STATE_DIR/socket-active" 2>/dev/null || true
    LC_ALL=C ufw status > "$STATE_DIR/ufw-status"
    touch "$STATE_DIR/ready"
fi

rollback_on_error() {
    local code=$? line=$1 command=$2
    trap - ERR
    log_error "Line $line: $command (exit $code). Restoring SSH/UFW backup."
    bash "$SCRIPT_DIR/01_rollback_hardening.sh" || log_error "Rollback failed: use VM snapshot."
    exit "$code"
}
trap 'rollback_on_error "$LINENO" "$BASH_COMMAND"' ERR

if ! id mlops >/dev/null 2>&1; then
    useradd -m -s /bin/bash mlops
fi
log_info "Deploy user: mlops. Set its password afterwards with sudo passwd mlops."

install -d -m 0755 /etc/ssh/sshd_config.d /run/sshd
install -m 0600 "$SCRIPT_DIR/../configs/sshd_hardened.conf" "$SSH_DROPIN"
rm -f /etc/ssh/sshd_config.d/99-mlops-hardened.conf
if ! head -n 1 /etc/ssh/sshd_config | grep -Fxq "Include $SSH_DROPIN"; then
    sed -i "1iInclude $SSH_DROPIN" /etc/ssh/sshd_config
fi
ssh-keygen -A
/usr/sbin/sshd -t
[[ "$(/usr/sbin/sshd -T | awk '$1 == "port" {print $2}')" == 2222 ]]
[[ "$(/usr/sbin/sshd -T | awk '$1 == "permitrootlogin" {print $2}')" == no ]]

log_info "Replacing UFW rules on this dedicated lab VM; original rules are backed up."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
for port in 2222 8000 5000 3000 9001; do
    ufw allow "${port}/tcp" comment 'MLOps lab'
done
ufw --force enable

if systemctl cat ssh.socket >/dev/null 2>&1; then
    systemctl disable --now ssh.socket
fi
systemctl enable ssh.service
systemctl restart ssh.service
systemctl is-active --quiet ssh.service
ss -H -ltn 'sport = :2222' | grep -q .
if ss -H -ltn 'sport = :22' | grep -q .; then
    log_error "Port 22 is still listening; refusing to report success."
    false
fi
log_success "SSH: 2222, root login disabled; UFW: five required TCP ports only."
ufw status verbose
