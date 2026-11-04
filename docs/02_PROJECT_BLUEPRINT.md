# 🏗️ THunter: Project Blueprint
*Autonomous Alert Triage, Threat Enrichment & Incident Response Engine*

---

## 💡 The Problem We Are Solving
Every day, Security Operations Centers (SOCs) are bombarded by tens of thousands of security alerts. 
Human analysts get **alert fatigue**, leading to missed attacks and burnout.

Many students try to solve this by dumping raw logs into an AI like ChatGPT. But that fails in real companies because:
1. It leaks private company data (PII and internal IPs).
2. The AI hallucinates because it doesn't have live internet data.
3. Attackers can trick the AI using prompt injection.
4. It only describes the problem—it doesn't fix it.

---

## 🚀 Our Solution: THunter

`THunter` is a smart, automated assistant for security teams that handles alerts in **5 automated stages**:

```
[Raw Log Ingestion]
        │
        ▼
[Stage 1: Privacy Sanitizer]  ──> Erases private IPs and passwords
        │
        ▼
[Stage 2: Threat Intel Check] ──> Queries AbuseIPDB & VirusTotal for live IP reputation
        │
        ▼
[Stage 3: AI Security Filter] ──> Catches sneaky prompt injection attempts
        │
        ▼
[Stage 4: Gemini Analysis]    ──> Translates technical attack into plain English & MITRE codes
        │
        ▼
[Stage 5: SOAR Remediation]   ──> Generates firewall block rule & Discord alert
```

---

## 🛠️ The 5 Stages Explained

### Stage 1: Privacy Sanitizer (Zero-Trust Guardrail)
* **What it does:** Scans the incoming log for private internal network IPs (e.g., `192.168.x.x`, `10.x.x.x`) and authorization tokens/passwords. It replaces them with masked tokens like `[REDACTED_INTERNAL_IP]` before sending anything outside the local computer.

### Stage 2: Threat Intelligence Aggregator (Truecaller for Hackers)
* **What it does:** Extracts any public attacker IP address found in the log and automatically queries the **AbuseIPDB API**. It retrieves:
  * Abuse Confidence Score (0% to 100%)
  * Total number of abuse reports worldwide
  * Country of origin and ISP/Host name

### Stage 3: Prompt Injection Guardrail (Defending the AI)
* **What it does:** Checks if the attacker placed malicious English instructions in the log (e.g., in a User-Agent or username) intended to fool the AI.

### Stage 4: AI Analysis & Classification (Gemini Engine)
* **What it does:** Passes the sanitized log + live Threat Intel data to the Gemini API with a strict structured prompt.
* **The Output:**
  * Threat Summary in plain English.
  * Official MITRE ATT&CK technique code (e.g., `T1110 - Brute Force`).
  * Severity Rating: `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.

### Stage 5: SOAR Remediation & Alerts
* **What it does:**
  * Auto-generates the exact firewall command to block the malicious IP (e.g., `iptables -A INPUT -s <IP> -j DROP`).
  * Sends a formatted alert message directly to a team Discord or Slack webhook.
