# 👥 Team Roles & Step-by-Step Roadmap
*Collaboration Guide for Prince Patel & Vishwa Prajapati*

---

## 🎯 Division of Responsibilities

Having two distinct, complementary roles makes your project look like a real engineering collaboration during technical interviews!

```
┌───────────────────────────────────────────────┐
│                    THUNTER                    │
├───────────────────────┬───────────────────────┤
│    Prince Patel       │   Vishwa Prajapati    │
│  (Data & Intel Lead)  │  (AI & Response Lead) │
├───────────────────────┼───────────────────────┤
│ • Log Ingestion &     │ • AI Prompt Engine    │
│   Parsing (FastAPI)   │   (Gemini Structured) │
│ • Local Privacy       │ • Prompt Injection    │
│   Sanitizer / Masker  │   Guardrail Filter    │
│ • Threat Intel API    │ • SOAR Remediation &  │
│   Client (AbuseIPDB)  │   Discord Alert Webhook
└───────────────────────┴───────────────────────┘
```

---

### 🛡️ Prince's Domain: Data, Privacy & Threat Intelligence
1. **Log Parser:** Writes Python functions to take raw log strings (Apache, Nginx, or SSH auth logs) and extract timestamps, IPs, request methods, and user agents.
2. **Privacy Sanitizer:** Writes regular expressions (regex) to detect internal RFC-1918 IPs (`10.x.x.x`, `192.168.x.x`) and sensitive strings (passwords, auth tokens) and replace them with safe placeholders.
3. **Threat Intel Aggregator:** Implements the API caller for **AbuseIPDB** and **VirusTotal** to fetch live attacker reputation data.

---

### 🧠 Vishwa's Domain: AI Reasoning, Guardrails & Response
1. **Adversarial Prompt Guardrail:** Builds a detector to scan extracted log fields for jailbreak attempts or prompt injection strings before the LLM processes them.
2. **Gemini Structured Triage Engine:** Crafts and tests the prompt with the Gemini API to reliably output clean JSON containing threat descriptions, MITRE ATT&CK mappings, and severity scores.
3. **SOAR & Alert Dispatcher:** Takes the final triage results and generates:
   * Ready-to-execute firewall blocking commands (`iptables` / Windows Firewall).
   * A clean Discord / Slack webhook alert formatted with color-coded severity.

---

## 🗺️ Step-by-Step Roadmap

| Phase | Milestone | Objective |
| :---: | :--- | :--- |
| **Phase 1** | **Setup & Foundation** | Initialize Git repo, set up Python virtual environment, install dependencies (`fastapi`, `requests`, `google-genai`, `pydantic`). |
| **Phase 2** | **Privacy & Log Ingestion** | Build log parser and local data sanitizer (Prince). |
| **Phase 3** | **Threat Intel Integration** | Connect to AbuseIPDB API and fetch live IP reputation scores (Prince). |
| **Phase 4** | **Prompt Injection Guard** | Build the adversarial prompt filter to protect the AI (Vishwa). |
| **Phase 5** | **Gemini Triage & Reasoning** | Connect Gemini API for structured JSON triage with MITRE mapping (Vishwa). |
| **Phase 6** | **SOAR Remediation & Webhooks**| Build automated firewall rule generator and Discord webhook alert (Vishwa). |
| **Phase 7** | **Interactive Web UI / CLI** | Build a sleek web dashboard or CLI demo to showcase the pipeline in action. |
| **Phase 8** | **Interview Prep & Packaging** | Write README with architecture diagrams, record a demo, and draft resume bullet points. |

---

## 🤝 How to Collaborate Using Git & GitHub

1. **One GitHub Repository:** Create a single repository on GitHub (e.g., `github.com/<username>/SentinelFlow-AI`).
2. **Both are Collaborators:** Add each other as collaborators so both have full commit access.
3. **Read this `docs/` folder:** Whenever either of you opens the project, everything you need to know is documented right here in `docs/`!
