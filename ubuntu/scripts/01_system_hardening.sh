#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"

require_root

DEPLOY_USER="mlops"
CONFIGS_DIR="${SCRIPT_DIR}/../configs"

log_step "PHASE 1: Setting up isolated deploy user '${DEPLOY_USER}'"

if id "${DEPLOY_USER}" &>/dev/null; then
    log_info "User '${DEPLOY_USER}' already exists. Skipping creation."
else
    log_info "Creating user '${DEPLOY_USER}' with bash shell and sudo group..."
    useradd -m -s /bin/bash -G sudo "${DEPLOY_USER}"
    log_success "User '${DEPLOY_USER}' created successfully."
    log_warn "Remember to set a password for '${DEPLOY_USER}' using: sudo passwd ${DEPLOY_USER}"
fi

log_step "PHASE 2: Hardening SSH Daemon (Port 2222)"

SSHD_CONF_DIR="/etc/ssh/sshd_config.d"
mkdir -p "${SSHD_CONF_DIR}"
SSHD_SRC="${CONFIGS_DIR}/sshd_hardened.conf"
SSHD_DST="${SSHD_CONF_DIR}/99-mlops-hardened.conf"

if [[ -f "${SSHD_SRC}" ]]; then
    log_info "Installing hardened SSH drop-in configuration to ${SSHD_DST}"
    cp "${SSHD_SRC}" "${SSHD_DST}"
    chmod 0600 "${SSHD_DST}"

    if [[ ! -f /etc/ssh/ssh_host_rsa_key && ! -f /etc/ssh/ssh_host_ed25519_key ]]; then
        log_info "Generating host keys with 'ssh-keygen -A'..."
        ssh-keygen -A
    fi

    if sshd -t; then
        log_info "SSH syntax valid. Restarting ssh service..."
        systemctl enable ssh || systemctl enable sshd
        systemctl restart ssh || systemctl restart sshd
        log_success "SSH daemon running on Port 2222."
    else
        log_error "sshd syntax test failed! Reverting drop-in config."
        rm -f "${SSHD_DST}"
        exit 1
    fi
fi

log_step "PHASE 3: Configuring UFW Firewall"

export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq ufw

ufw default deny incoming
ufw default allow outgoing

ufw allow 2222/tcp comment 'Hardened SSH'
ufw allow 8000/tcp comment 'FastAPI Model Serving'
ufw allow 5000/tcp comment 'MLflow UI'
ufw allow 3000/tcp comment 'Grafana Telemetry'
ufw allow 9001/tcp comment 'MinIO Web Console'

ufw --force enable
log_success "UFW firewall active and configured."

log_step "SUMMARY"
log_success "Ubuntu Hardening Complete!"
