# 🎯 Threat Model & Detection Limitations Matrix
*Living Engineering Documentation for THunter*
*Authors: Prince Patel (`Mr200`) & Vishwa Prajapati (`Ms200`)*

---

## 🧭 Purpose of this Document
In professional cybersecurity, there is no such thing as "100% protection." 

Every security product has **assumptions**, **coverage boundaries**, and **blind spots (False Negatives)**. This document provides total architectural transparency into what THunter can reliably detect, what can bypass it, and our engineering roadmap to solve those limitations across versions.

---

## 📊 Version 0.1.0 Capabilities Matrix

### ✅ What THunter v0.1.0 CAN Detect (Supported Scope)
1. **Volumetric SSH / Auth Brute Force:** Repeated failed authentication attempts from single IP addresses within short timeframes.
2. **Cleartext Web Exploitation Signatures:**
   * SQL Injection (`UNION SELECT`, `' OR 1=1`, `sqlmap` signatures).
   * Local File Inclusion / Path Traversal (`../../etc/passwd`, `win.ini`).
3. **Known Malicious Infrastructure:** Attackers operating from known Tor exit nodes, bulletproof hosting, or IPs with high abuse scores on **AbuseIPDB** (Score ≥ 25%).
4. **Indirect Prompt Injection:** Adversarial instructions hidden inside User-Agents or request headers attempting to manipulate downstream LLMs (e.g. `ignore previous instructions`, `system_override`).
5. **Internal Data Leaks:** Accidental leakage of RFC-1918 private IPs (`10.x.x.x`, `192.168.x.x`) and authorization tokens (`Bearer eyJ...`, `password=...`).

---

### ⚠️ Known Blind Spots & Failure Modes (What v0.1.0 CANNOT Detect)

```
                       ┌─────────────────────────────────────┐
                       │      Incoming Attacker Request      │
                       └──────────────────┬──────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
         [Known Signature]                               [Evasion Technique]
                  │                                               │
                  ▼                                               ▼
     ┌────────────────────────┐                     ┌───────────────────────────┐
     │  Detected by v0.1.0    │                     │   Bypasses v0.1.0 Gate    │
     │ (High Confidence alert)│                     │ (False Negative / Passed) │
     └────────────────────────┘                     └─────────────┬─────────────┘
                                                                  │
                                            ┌─────────────────────┴─────────────────────┐
                                            ▼                                           ▼
                                 [Blind Spot 1: Clean IP]                   [Blind Spot 2: Obfuscation]
                                 (Residential Proxy / 0 Reports)            (Double URL Hex / Comments)
```

#### 1. Blind Spot: Brand-New or Clean IP Addresses (Residential Proxies)
* **The Failure Scenario:** An attacker rents a new AWS IP or routes traffic through a compromised home Wi-Fi (residential proxy) with 0 reports on AbuseIPDB.
* **Why v0.1.0 Misses It:** Because the Threat Intel score is 0%, the Gatekeeper may treat the IP as harmless if the payload doesn't trigger a regex pattern.
* **Target Version to Fix:** **v0.2.0** (Add frequency rate-limiting & anomaly scoring).

#### 2. Blind Spot: Obfuscated & Hex-Encoded Web Payloads
* **The Failure Scenario:** The attacker avoids literal keywords:
  * Instead of: `UNION SELECT`
  * They send: `UNI/**/ON%20%53ELECT` or `%2527%20OR%201=1` (Double-encoded quotes).
* **Why v0.1.0 Misses It:** Standard regex without a recursive URL/hex decoder will fail string matching.
* **Target Version to Fix:** **v0.2.0** (Implement a recursive normalization & decoding engine prior to regex evaluation).

#### 3. Blind Spot: Distributed "Low and Slow" Attacks
* **The Failure Scenario:** An attacker tests 1 password every 2 hours using 30 different IP addresses.
* **Why v0.1.0 Misses It:** v0.1.0 evaluates logs **statelessly** (one log line at a time). It has no memory of what happened 2 hours ago.
* **Target Version to Fix:** **v0.3.0** (Introduce a local Redis or SQLite sliding-window session store to correlate multi-day telemetry).

#### 4. Blind Spot: Payload Blindness (Truncated Web Logs)
* **The Failure Scenario:** An exploit is sent inside the JSON body of a `POST /checkout` request, but the web server log only records:
  `POST /checkout HTTP/1.1 200 450` (the body was never logged by Nginx/Apache).
* **Why v0.1.0 Misses It:** THunter can only analyze what exists in the log. If the server does not log the POST body, no tool can read it.
* **Prerequisite:** System deployment documentation must specify proper Web Application Firewall (WAF) or mod_security log format configuration.

---

## 🗺️ Version Evolution Roadmap

| Version | Focus | Major Enhancements & Blind Spots Solved |
| :---: | :--- | :--- |
| **v0.1.0** (Current) | **Foundational Pipeline** | Single-line log parsing, local privacy sanitization, AbuseIPDB integration, basic prompt injection filter, Gemini triage & iptables containment. |
| **v0.2.0** (Planned) | **Evasion Resistance** | Recursive URL/Hex/Base64 payload decoder to defeat WAF evasion; dynamic rate-limiting gatekeeper. |
| **v0.3.0** (Planned) | **Stateful Correlation** | Sliding-window memory store to catch "Low and Slow" distributed attacks across multiple hours. |
| **v0.4.0** (Planned) | **Multi-Source Threat Intel** | Add VirusTotal and AlienVault OTX fallback APIs when AbuseIPDB quota is exhausted. |
