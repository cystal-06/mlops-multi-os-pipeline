# Multi-OS MLOps Pipeline Comparative Analysis

Comparative study of an identical, production-grade MLOps stack deployed across two contrasting Linux paradigms:
- **Arch Linux Node**: Rolling-Release, DIY, Native `nftables`, Rootless Docker with unprivileged namespaces.
- **Ubuntu Server Node**: LTS Enterprise, Debian conventions, `ufw`, System-level Docker daemon.

## Project Structure

```text
.
├── arch/                     # Arch Linux Deployment (Member 1)
│   ├── configs/              # nftables.conf, sshd_hardened.conf, sysctl_mlops.conf
│   └── scripts/              # 00_common.sh, 01_system_hardening.sh, 01_rollback_hardening.sh
├── ubuntu/                   # Ubuntu Server Deployment (Member 2)
│   ├── configs/              # sshd_hardened.conf
│   └── scripts/              # 00_common.sh, 01_system_hardening.sh, 01_rollback_hardening.sh
├── stack/                    # Parity MLOps Docker Stack (Shared)
│   └── .env.example
├── benchmark/                # Performance, RPS & RAM Benchmarks
└── docs/                     # Documentation & Team Conventions
    ├── QUY_UOC_LAM_VIEC.md
    ├── QUY_UOC_LAM_VIEC.pdf
    └── QUY_UOC_LAM_VIEC.docx
```

## Quick Start

### Arch Linux (Member 1)
```bash
cd arch/scripts
chmod +x *.sh
sudo ./01_system_hardening.sh
```

### Ubuntu Server (Member 2)
```bash
cd ubuntu/scripts
chmod +x *.sh
sudo ./01_system_hardening.sh
```
