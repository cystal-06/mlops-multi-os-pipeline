#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_common.sh"
require_root
require_ubuntu
STATE_DIR=/var/lib/mlops-infra/docker
if [[ ! -f "$STATE_DIR/ready" ]]; then
    log_info 'No managed Docker installation to roll back.'
    exit 0
fi
if command -v docker >/dev/null && systemctl is-active --quiet docker; then
    if [[ -n "$(docker ps -q)" ]]; then
        log_error 'Containers still running. Stop your stack before rollback.'
        exit 1
    fi
fi
for unit in docker.service docker.socket containerd.service; do
    if systemctl cat "$unit" >/dev/null 2>&1; then systemctl disable --now "$unit"; fi
done
packages=()
for pkg in docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras; do
    if [[ "$(dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null || true)" == 'install ok installed' ]]; then
        packages+=("$pkg")
    fi
done
if ((${#packages[@]})); then apt-get remove -y "${packages[@]}"; fi
for path in /etc/docker/daemon.json /etc/apt/keyrings/docker.asc /etc/apt/sources.list.d/docker.sources; do
    restore_path "$path"
done
if ! grep -qx docker "$STATE_DIR/mlops-groups" && id -nG mlops | tr ' ' '\n' | grep -qx docker; then
    gpasswd -d mlops docker
fi
systemctl daemon-reload
log_success 'Removed managed Docker packages and restored saved configuration/membership.'
log_info 'Images, volumes, container data, prerequisites and backup are retained. Existing sessions must log out.'
log_info 'Reinstall with 02_setup_docker.sh; for exact full-machine rollback use the pre-Docker VM snapshot.'
