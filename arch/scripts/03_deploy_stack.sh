#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"

require_root

DEPLOY_USER="mlops"
USER_UID=$(id -u "${DEPLOY_USER}")
USER_HOME="/home/${DEPLOY_USER}"
STACK_SRC="${SCRIPT_DIR}/../../stack"
STACK_DST="${USER_HOME}/stack"
SYSTEMD_SRC="${SCRIPT_DIR}/../systemd/mlops-stack.service"
SYSTEMD_DST="${USER_HOME}/.config/systemd/user/mlops-stack.service"

log_step "PHASE 1: Synchronizing MLOps stack files to ${STACK_DST}"
mkdir -p "${STACK_DST}"
cp -r "${STACK_SRC}/"* "${STACK_DST}/"

if [[ ! -f "${STACK_DST}/.env" && -f "${STACK_DST}/.env.example" ]]; then
    log_info "Creating .env from .env.example..."
    cp "${STACK_DST}/.env.example" "${STACK_DST}/.env"
fi

chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "${STACK_DST}"
log_success "Stack files synced."

log_step "PHASE 2: Installing User Systemd Service"
mkdir -p "${USER_HOME}/.config/systemd/user"
cp "${SYSTEMD_SRC}" "${SYSTEMD_DST}"
chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "${USER_HOME}/.config"

log_info "Reloading user systemd daemon and enabling mlops-stack.service..."
sudo -u "${DEPLOY_USER}" XDG_RUNTIME_DIR="/run/user/${USER_UID}" DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/${USER_UID}/bus" systemctl --user daemon-reload
sudo -u "${DEPLOY_USER}" XDG_RUNTIME_DIR="/run/user/${USER_UID}" DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/${USER_UID}/bus" systemctl --user enable mlops-stack.service
log_success "mlops-stack.service enabled on boot."

log_step "PHASE 3: Building and starting MLOps container stack"
log_info "Executing 'docker compose up -d' as user ${DEPLOY_USER}..."

sudo -u "${DEPLOY_USER}" \
    XDG_RUNTIME_DIR="/run/user/${USER_UID}" \
    DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/${USER_UID}/bus" \
    DOCKER_HOST="unix:///run/user/${USER_UID}/docker.sock" \
    docker compose -f "${STACK_DST}/docker-compose.yml" up -d --build

log_step "DEPLOYMENT COMPLETED"
echo -e "${COLOR_GREEN}------------------------------------------------------------${COLOR_RESET}"
echo -e "MLOps Services accessible on host:"
echo -e "  - FastAPI Model Serving : http://localhost:8000 (docs: /docs)"
echo -e "  - MLflow Tracking UI    : http://localhost:5000"
echo -e "  - Grafana Telemetry     : http://localhost:3000 (admin / admin)"
echo -e "  - MinIO Web Console     : http://localhost:9001 (minioadmin / secure_minio_password_change_me)"
echo -e "${COLOR_GREEN}------------------------------------------------------------${COLOR_RESET}"
