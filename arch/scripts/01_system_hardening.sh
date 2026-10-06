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
    log_info "Creating user '${DEPLOY_USER}' with bash shell and home directory..."
    useradd -m -s /bin/bash -G wheel "${DEPLOY_USER}"
    log_success "User '${DEPLOY_USER}' created successfully."
    log_warn "Remember to set a password for '${DEPLOY_USER}' using: sudo passwd ${DEPLOY_USER}"
fi

if [[ -f /etc/sudoers.d/10-wheel ]]; then
    log_info "Sudoers drop-in for wheel already present."
else
    log_info "Configuring sudoers drop-in for wheel group..."
    echo "%wheel ALL=(ALL:ALL) ALL" > /etc/sudoers.d/10-wheel
    chmod 0440 /etc/sudoers.d/10-wheel
fi

log_step "PHASE 2: Applying High-Throughput Kernel Sysctl Tuning"

SYSCTL_SRC="${CONFIGS_DIR}/sysctl_mlops.conf"
SYSCTL_DST="/etc/sysctl.d/99-mlops.conf"

if [[ -f "${SYSCTL_SRC}" ]]; then
    log_info "Copying ${SYSCTL_SRC} -> ${SYSCTL_DST}"
    cp "${SYSCTL_SRC}" "${SYSCTL_DST}"
    chmod 0644 "${SYSCTL_DST}"
    log_info "Loading sysctl parameters into live kernel..."
    sysctl --system > /dev/null
    log_success "Kernel parameters applied successfully."
else
    log_error "Sysctl source configuration not found: ${SYSCTL_SRC}"
    exit 1
fi

log_step "PHASE 3: Hardening SSH Daemon (Port 2222)"

SSHD_CONF_DIR="/etc/ssh/sshd_config.d"
mkdir -p "${SSHD_CONF_DIR}"
SSHD_SRC="${CONFIGS_DIR}/sshd_hardened.conf"
SSHD_DST="${SSHD_CONF_DIR}/99-mlops-hardened.conf"

if [[ -f "${SSHD_SRC}" ]]; then
    log_info "Installing hardened SSH drop-in configuration to ${SSHD_DST}"
    cp "${SSHD_SRC}" "${SSHD_DST}"
    chmod 0600 "${SSHD_DST}"
    
    if [[ ! -f /etc/ssh/ssh_host_rsa_key && ! -f /etc/ssh/ssh_host_ed25519_key ]]; then
        log_info "No SSH host keys found. Generating host keys with 'ssh-keygen -A'..."
        ssh-keygen -A
    fi

    if sshd -t; then
        log_info "SSH configuration syntax verified. Enabling and restarting sshd..."
        systemctl enable sshd
        systemctl restart sshd
        log_success "SSH daemon reloaded and active on Port 2222."
    else
        log_error "sshd syntax test failed! Reverting drop-in config to prevent lockout."
        rm -f "${SSHD_DST}"
        exit 1
    fi
else
    log_error "SSH source configuration not found: ${SSHD_SRC}"
    exit 1
fi

log_step "PHASE 4: Deploying Native nftables Stateful Firewall"

NFT_SRC="${CONFIGS_DIR}/nftables.conf"
NFT_DST="/etc/nftables.conf"

if [[ -f "${NFT_SRC}" ]]; then
    log_info "Validating nftables ruleset syntax..."
    nft -c -f "${NFT_SRC}"
    
    log_info "Deploying ruleset to ${NFT_DST}..."
    cp "${NFT_SRC}" "${NFT_DST}"
    chmod 0644 "${NFT_DST}"

    log_info "Loading ruleset into active kernel..."
    nft -f "${NFT_DST}"

    log_info "Enabling and starting nftables systemd service..."
    systemctl enable --now nftables
    log_success "nftables stateful firewall active and enabled on boot."
else
    log_error "nftables configuration not found: ${NFT_SRC}"
    exit 1
fi

log_step "SUMMARY"
log_success "System Hardening Complete!"
echo -e "${COLOR_GREEN}------------------------------------------------------------${COLOR_RESET}"
echo -e "1. Deploy User    : ${DEPLOY_USER} (Group: wheel)"
echo -e "2. SSH Port       : 2222 (Root login disabled)"
echo -e "3. Firewall       : nftables (Anti-Brute Force active)"
echo -e "4. Sysctl Tuning  : /etc/sysctl.d/99-mlops.conf applied"
echo -e "${COLOR_GREEN}------------------------------------------------------------${COLOR_RESET}"
