#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/00_common.sh"
require_root
require_ubuntu
STATE_DIR=/var/lib/mlops-infra/docker
packages=(docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin)
paths=(/etc/docker/daemon.json /etc/apt/keyrings/docker.asc /etc/apt/sources.list.d/docker.sources)
installed() { [[ "$(dpkg-query -W -f='${Status}' "$1" 2>/dev/null || true)" == 'install ok installed' ]]; }
id mlops >/dev/null
if [[ ! -f "$STATE_DIR/ready" ]]; then
    for pkg in docker.io docker-compose docker-compose-v2 docker-doc docker-buildx podman-docker containerd runc docker-ce-rootless-extras "${packages[@]}"; do
        if installed "$pkg"; then
            log_error "Existing package $pkg: this installer is for a fresh Docker lab VM. Stop and review migration."
            exit 1
        fi
    done
    if command -v docker >/dev/null || command -v dockerd >/dev/null; then
        log_error 'Existing manual Docker installation; stop and review.'
        exit 1
    fi
    if grep -Rqs 'download.docker.com' /etc/apt/sources.list /etc/apt/sources.list.d; then
        log_error 'Existing Docker APT source; stop and review to avoid duplicate repositories.'
        exit 1
    fi
    for path in /etc/docker/daemon.json /var/lib/docker /var/lib/containerd; do
        if [[ -e "$path" ]]; then
            log_error "Existing Docker configuration/data: $path. Use a fresh VM baseline."
            exit 1
        fi
    done
    install -d -m 0700 "$STATE_DIR"
    for path in "${paths[@]}"; do backup_path "$path"; done
    id -nG mlops | tr ' ' '\n' > "$STATE_DIR/mlops-groups"
    touch "$STATE_DIR/ready"
fi
export DEBIAN_FRONTEND=noninteractive
log_info 'Installing prerequisites; these packages are retained on rollback.'
apt-get update
apt-get install -y ca-certificates curl python3
install -d -m 0755 /etc/apt/keyrings /etc/docker
curl --fail --silent --show-error --location --retry 3 \
    https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod 0644 /etc/apt/keyrings/docker.asc
source /etc/os-release
cat > /etc/apt/sources.list.d/docker.sources <<SOURCE
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: ${UBUNTU_CODENAME:-$VERSION_CODENAME}
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
SOURCE
apt-get update
missing=()
for pkg in "${packages[@]}"; do
    if ! installed "$pkg"; then missing+=("$pkg"); fi
done
if ((${#missing[@]})); then apt-get install -y "${missing[@]}"; fi
python3 - <<'PY'
import json, os, pathlib
p = pathlib.Path('/etc/docker/daemon.json')
d = json.loads(p.read_text()) if p.exists() else {}
d['log-driver'] = 'json-file'
d['log-opts'] = {'max-size': '10m', 'max-file': '3'}
tmp = p.with_suffix('.json.tmp')
tmp.write_text(json.dumps(d, indent=2) + '\n')
os.chmod(tmp, 0o644)
os.replace(tmp, p)
PY
dockerd --validate --config-file=/etc/docker/daemon.json
systemctl enable --now containerd.service docker.service
systemctl restart docker.service
usermod -aG docker mlops
systemctl is-active --quiet docker.service
systemctl is-enabled --quiet docker.service
docker version
docker compose version
docker run --rm hello-world
touch "$STATE_DIR/complete"
log_success 'Docker/Compose ready. Logging: json-file, 10m x 3. Log out/in as mlops to refresh groups.'
log_warn 'Docker group grants root-equivalent control. Rollback: sudo bash ubuntu/scripts/02_rollback_docker.sh'
