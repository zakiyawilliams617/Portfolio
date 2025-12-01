# Wazuh Detection Analysis

# Problem I Solved
Analyze how Wazuh detects and responds to adversary techniques across Windows and Linux endpoints, using simulated attacks mapped to MITRE ATT&CK and the Cyber Kill Chain.

# Environment / Architecture
- Wazuh Manager / Indexer / Dashboard
- Windows + Linux endpoints
- Attack simulation tools (Atomic Red Team, CALDERA)
- Virtualization platform: ___ (Proxmox, KVM, etc.)

# Tools Used
- Wazuh
- MITRE ATT&CK
- Python (for data analysis)
- Bash / PowerShell
- Virtualization platform

# What I Did
- Simulated multiple attack techniques (e.g., T1059, T1078, T1082, T1046, T1053)
- Collected Wazuh logs and alerts
- Measured detection timeliness, severity, and rule coverage
- Compared detections across Windows vs. Linux endpoints

# Results (Highlights)
- ⏱ Detection time ranges: …
- 🎯 True positives vs. false positives: …
- 🧩 Differences between OS types: …

# Folder Structure
- `diagrams/` – Architecture diagrams, pipeline diagrams
- `logs/` – Sample anonymized Wazuh logs
- `scripts/` – Python or shell scripts used for parsing/analyzing logs
- `results/` – Aggregated CSVs, charts, tables

# What I Learned
- How to design repeatable adversary simulations
- How to interpret Wazuh alerts and rule IDs
- How to quantify SIEM/XDR detection performance with metrics

