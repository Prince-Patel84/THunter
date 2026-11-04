# 🎯 THunter (ThreatHunter-AI)

> **Autonomous Threat Hunting, Alert Triage & Incident Response Engine**  
> *Developed by Prince Patel (`Mr200`) & Vishwa Prajapati (`Ms200`)*

---

## 📌 Project Overview
**THunter** is a modern security automation (SOAR) and threat hunting engine designed to help Security Operations Centers (SOCs) combat alert fatigue.

Unlike naive LLM wrappers, THunter utilizes a **zero-trust defense-in-depth architecture**:
1. **Local Privacy Sanitization:** Strips internal RFC-1918 IPs, passwords, and sensitive PII *before* cloud inference.
2. **Deterministic Threat Intel:** Queries live global IP threat reputation databases (AbuseIPDB, VirusTotal).
3. **Prompt Injection Defense:** Validates untrusted log payloads against adversarial injection attacks.
4. **Structured AI Triage:** Employs Gemini to translate complex log telemetry into plain-English incident summaries and official **MITRE ATT&CK** technique mappings.
5. **Automated SOAR Playbooks:** Generates immediate firewall containment commands and sends real-time webhook alerts.

---

## 📚 Team Knowledge Hub & Onboarding Guides
If you are new to these terms or onboarding to the project, start by reading our guides in the `docs/` folder:

* 📖 **[Cyber Security Beginner's Dictionary](docs/01_CYBER_SECURITY_DICTIONARY.md):** Plain-English definitions for Logs, SOC, SIEM, Threat Intel, PII, SOAR, MITRE ATT&CK, and Prompt Injection.
* 🏗️ **[Project Blueprint & Architecture](docs/02_PROJECT_BLUEPRINT.md):** Deep-dive into the 5-stage pipeline and why each stage matters.
* 👥 **[Team Roles & Roadmap](docs/03_TEAM_ROLES_AND_ROADMAP.md):** Detailed breakdown of Prince's and Vishwa's responsibilities, milestones, and Git collaboration workflow.

---

## 🚀 Quickstart
```bash
# Clone the repository
git clone https://github.com/<your-username>/THunter.git
cd THunter

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
