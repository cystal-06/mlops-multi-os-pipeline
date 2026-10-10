#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/00_common.sh"

USER_UID=$(id -u mlops 2>/dev/null || echo "1000")
DOCKER_CMD="sudo -u mlops XDG_RUNTIME_DIR=/run/user/${USER_UID} DOCKER_HOST=unix:///run/user/${USER_UID}/docker.sock docker"

log_step "CHECK 1: Validating Linux Host Hardening & Firewall (nftables)"
if systemctl is-active --quiet nftables; then
    log_success "nftables firewall: ACTIVE (Ruleset loaded)"
else
    log_warn "nftables firewall: INACTIVE"
fi

if [[ -f /etc/sysctl.d/99-mlops.conf ]]; then
    log_success "Sysctl MLOps Kernel tuning: PRESENT"
else
    log_warn "Sysctl MLOps Kernel tuning: MISSING"
fi

log_step "CHECK 2: Verifying Rootless Docker Isolation"
CONTAINER_USER=$(${DOCKER_CMD} run --rm alpine id -u 2>/dev/null || echo "error")
if [[ "${CONTAINER_USER}" == "0" ]]; then
    log_success "Rootless Docker: RUNNING (Isolated Container UID 0 maps safely to unprivileged Host UID ${USER_UID})"
else
    log_error "Rootless Docker check failed"
fi

log_step "CHECK 3: Verifying MLOps Container Stack Status"
${DOCKER_CMD} ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

log_step "CHECK 4: Probing Service Endpoints (HTTP Health Checks)"

check_endpoint() {
    local name=$1
    local url=$2
    local expected=$3
    local code=$(curl -s -o /dev/null -w "%{http_code}" "${url}" || echo "000")
    if [[ "${code}" == "${expected}" ]]; then
        echo -e "  [${COLOR_GREEN}PASS${COLOR_RESET}] ${name} (${url}) -> HTTP ${code}"
    else
        echo -e "  [${COLOR_YELLOW}WAIT${COLOR_RESET}] ${name} (${url}) -> HTTP ${code} (expected ${expected})"
    fi
}

check_endpoint "FastAPI Model Serving" "http://localhost:8000/health" "200"
check_endpoint "MLflow Tracking UI   " "http://localhost:5000/" "200"
check_endpoint "Grafana Dashboard UI " "http://localhost:3000/api/health" "200"
check_endpoint "MinIO Web Console    " "http://localhost:9001/" "200"

log_step "CHECK 5: Testing Zero-Trust Network Isolation (Security Audit)"
if nc -z -w 1 localhost 5432 2>/dev/null; then
    log_error "PostgreSQL port 5432 is EXPOSED to host! Security violation."
else
    log_success "PostgreSQL port 5432: HIDDEN (Secure internal network)"
fi

if nc -z -w 1 localhost 9000 2>/dev/null; then
    log_error "MinIO S3 API port 9000 is EXPOSED to host! Security violation."
else
    log_success "MinIO S3 API port 9000: HIDDEN (Secure internal network)"
fi

log_step "VERIFICATION SUMMARY COMPLETE"
