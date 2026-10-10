#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"

require_root

DEPLOY_USER="mlops"

log_step "PHASE 1: Installing Rootless Docker prerequisites on Arch Linux"
pacman -Sy --noconfirm --needed docker docker-compose fuse-overlayfs rootlesskit shadow

log_step "PHASE 2: Configuring subuid and subgid for unprivileged user namespaces"
if ! grep -q "^${DEPLOY_USER}:" /etc/subuid 2>/dev/null; then
    log_info "Assigning subuid range to ${DEPLOY_USER}..."
    echo "${DEPLOY_USER}:100000:65536" >> /etc/subuid
else
    log_info "subuid already configured for ${DEPLOY_USER}."
fi

if ! grep -q "^${DEPLOY_USER}:" /etc/subgid 2>/dev/null; then
    log_info "Assigning subgid range to ${DEPLOY_USER}..."
    echo "${DEPLOY_USER}:100000:65536" >> /etc/subgid
else
    log_info "subgid already configured for ${DEPLOY_USER}."
fi

log_step "PHASE 3: Delegating cgroups v2 resource controllers to user session"
CGROUP_DROPIN_DIR="/etc/systemd/system/user@.service.d"
mkdir -p "${CGROUP_DROPIN_DIR}"
cat << 'EOF' > "${CGROUP_DROPIN_DIR}/delegate.conf"
[Service]
Delegate=cpu cpuset io memory pids
EOF
systemctl daemon-reload
log_success "cgroups v2 delegation configured."

log_step "PHASE 4: Enabling systemd lingering for persistent daemon"
loginctl enable-linger "${DEPLOY_USER}"
log_success "Lingering enabled for ${DEPLOY_USER}."

log_step "PHASE 5: Initializing rootless docker environment for '${DEPLOY_USER}'"
MLOPS_HOME="/home/${DEPLOY_USER}"

cat << 'EOF' > "${MLOPS_HOME}/.bashrc_docker"
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DOCKER_HOST="unix://${XDG_RUNTIME_DIR}/docker.sock"
export PATH="/usr/bin:${PATH}"
EOF

if ! grep -q ".bashrc_docker" "${MLOPS_HOME}/.bashrc" 2>/dev/null; then
    echo "source ~/.bashrc_docker" >> "${MLOPS_HOME}/.bashrc"
    chown "${DEPLOY_USER}:${DEPLOY_USER}" "${MLOPS_HOME}/.bashrc"
fi
chown "${DEPLOY_USER}:${DEPLOY_USER}" "${MLOPS_HOME}/.bashrc_docker"

log_step "ROOTLESS PREREQUISITES COMPLETE"
echo -e "${COLOR_GREEN}------------------------------------------------------------${COLOR_RESET}"
echo -e "Next step: Run the user-level setup command as '${DEPLOY_USER}':"
echo -e "  sudo -u ${DEPLOY_USER} -i dockerd-rootless-setuptool.sh install"
echo -e "${COLOR_GREEN}------------------------------------------------------------${COLOR_RESET}"
