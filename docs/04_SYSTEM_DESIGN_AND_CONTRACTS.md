# 📐 System Design & Module Interface Contracts
*Textbook Software Engineering Specification for THunter*
*Authors: Prince Patel (`Mr200`) & Vishwa Prajapati (`Ms200`)*

---

## 1. Architectural Philosophy: Contract-First Development

To allow two engineers (Prince and Vishwa) to build different parts of the system simultaneously without breaking each other's code, we follow **Interface-Driven / Contract-First Development**.

Every module has:
1. **A Single Responsibility:** Does exactly one job.
2. **Strict Input Contract:** What data types and parameters it accepts.
3. **Strict Output Contract:** What exact data types and fields it promises to return.
4. **Decoupled Architecture:** Module B does not care *how* Module A is implemented inside, as long as Module A satisfies its output contract.

---

## 2. End-to-End Data Flow Pipeline

```
[Raw Log String]
       │
       ▼
┌────────────────────────────────┐
│   Module 1: SanitizerModule    │  (Author: Prince)
└──────────────┬─────────────────┘
               │  Output: SanitizedResult
               ▼
┌────────────────────────────────┐
│    Module 2: ParserModule      │  (Author: Prince)
└──────────────┬─────────────────┘
               │  Output: NormalizedEvent
        ┌──────┴──────┐
        ▼             ▼
┌──────────────┐ ┌──────────────┐
│  Module 3:   │ │  Module 4:   │
│ Threat Intel │ │  Guardrail   │
│ (AbuseIPDB)  │ │ (Injection)  │
│ (Prince)     │ │ (Vishwa)     │
└──────┬───────┘ └──────┬───────┘
       │                │
       │ Output:        │ Output:
       │ ThreatIntel    │ GuardrailVerdict
       │                │
       └───────┬────────┘
               ▼
┌────────────────────────────────┐
│   Module 5: AITriageModule     │  (Author: Vishwa)
└──────────────┬─────────────────┘
               │  Output: IncidentTriageReport
               ▼
┌────────────────────────────────┐
│    Module 6: SOARModule        │  (Author: Vishwa)
└────────────────────────────────┘
               │  Output: ContainmentPlan
               ▼
[Firewall Rule & Discord Alert]
```

---

## 3. Formal Module Contracts

### 📦 Module 1: `SanitizerModule` (Data Privacy & Compliance)
* **Assigned To:** Prince Patel
* **Responsibility:** Strip internal RFC-1918 IPs (`192.168.x`, `10.x`), loopback addresses (`127.0.0.1`), authentication tokens (JWT, Bearer), and passwords from log strings before anything is parsed or sent to an external network.

#### Input Contract:
```python
raw_log: str  # Unmodified raw log line from a server file or stream
```

#### Output Contract (`SanitizedResult`):
| Field | Type | Description |
| :--- | :--- | :--- |
| `sanitized_text` | `str` | The log line with secrets replaced by `[REDACTED_...]` placeholders |
| `redaction_count` | `int` | Total number of sensitive items masked |
| `redacted_types` | `list[str]` | Categories masked (e.g. `["INTERNAL_IP", "PASSWORD"]`) |

---

### 📦 Module 2: `ParserModule` (Log Normalization)
* **Assigned To:** Prince Patel
* **Responsibility:** Ingest a sanitized log string and parse it into a structured, unified security event object, regardless of whether the log came from an Apache web server or Linux SSH.

#### Input Contract:
```python
sanitized_text: str  # The cleaned text from Module 1
```

#### Output Contract (`NormalizedEvent`):
| Field | Type | Description |
| :--- | :--- | :--- |
| `event_type` | `str` | `"WEB_REQUEST"`, `"SSH_AUTH"`, or `"UNKNOWN"` |
| `source_ip` | `str | None` | The client / attacker IP address (e.g. `"185.220.101.5"`) |
| `timestamp` | `str | None` | Extracted log timestamp string |
| `target_resource` | `str | None` | The URI path accessed (for web) or username targeted (for SSH) |
| `http_method` | `str | None` | `"GET"`, `"POST"`, etc. (None for non-web) |
| `status_code` | `int | None` | HTTP response code (200, 404, etc.) or None |
| `untrusted_payload` | `str` | The user-controlled portion to scan (e.g. User-Agent, URI params) |

---

### 📦 Module 3: `ThreatIntelModule` (Deterministic Indicator Reputation)
* **Assigned To:** Prince Patel
* **Responsibility:** Query the AbuseIPDB API to check if a public IPv4 address has an existing criminal/abuse history.

#### Input Contract:
```python
ip_address: str  # The client IP extracted by Module 2
```

#### Output Contract (`ThreatIntelReport`):
| Field | Type | Description |
| :--- | :--- | :--- |
| `ip` | `str` | The IP address queried |
| `abuse_confidence_score` | `int` | Confidence score from 0 (clean) to 100 (confirmed malicious) |
| `total_reports` | `int` | Number of times reported globally in the last 90 days |
| `country_code` | `str` | Two-letter country code (e.g. `"DE"`, `"US"`, `"IN"`) |
| `isp` | `str` | Internet Service Provider or hosting provider name |
| `is_tor_exit_node` | `bool` | True if the IP is a known Tor anonymization relay |
| `is_malicious` | `bool` | True if `abuse_confidence_score >= 25` |

---

### 📦 Module 4: `GuardrailModule` (Prompt Injection Defense)
* **Assigned To:** Vishwa Prajapati
* **Responsibility:** Inspect the untrusted payload (User-Agent, URI parameters) to detect whether an attacker is attempting to jailbreak or manipulate the downstream LLM.

#### Input Contract:
```python
untrusted_payload: str  # Extracted from Module 2 (NormalizedEvent.untrusted_payload)
```

#### Output Contract (`GuardrailVerdict`):
| Field | Type | Description |
| :--- | :--- | :--- |
| `is_prompt_injection` | `bool` | True if adversarial instructions are detected |
| `risk_score` | `int` | Risk score from 0 to 100 |
| `flagged_patterns` | `list[str]` | The specific injection rules triggered |
| `disarmed_payload` | `str` | The payload wrapped in isolation safety tags |

---

### 📦 Module 5: `AITriageModule` (Reasoning & MITRE ATT&CK Mapping)
* **Assigned To:** Vishwa Prajapati
* **Responsibility:** Synthesize the `NormalizedEvent`, `ThreatIntelReport`, and `GuardrailVerdict` into an AI prompt using Google Gemini to classify the attack into the official MITRE ATT&CK framework and generate an analyst summary.

#### Input Contract:
```python
event: NormalizedEvent        # Output from Module 2
intel: ThreatIntelReport      # Output from Module 3
guardrail: GuardrailVerdict   # Output from Module 4
```

#### Output Contract (`IncidentTriageReport`):
| Field | Type | Description |
| :--- | :--- | :--- |
| `threat_title` | `str` | 3 to 7 word incident headline (e.g. `"SQL Injection Probe via sqlmap"`) |
| `mitre_attack_id` | `str` | Official MITRE technique code (e.g. `"T1190 - Exploit Public-Facing Application"`) |
| `severity` | `str` | Enum: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"` |
| `confidence_score` | `int` | Triage confidence from 0 to 100 |
| `summary` | `str` | 2-3 sentence plain English explanation for the security analyst |
| `recommended_action` | `str` | Tactical instruction (e.g. `"Patch SQL binding and ban IP"`) |

---

### 📦 Module 6: `SOARModule` (Automated Containment & Alerts)
* **Assigned To:** Vishwa Prajapati
* **Responsibility:** Take the final incident assessment and auto-generate the perimeter firewall blocking command and dispatch a Discord/Slack webhook alert.

#### Input Contract:
```python
triage: IncidentTriageReport  # Output from Module 5
intel: ThreatIntelReport      # Output from Module 3
```

#### Output Contract (`ContainmentPlan`):
| Field | Type | Description |
| :--- | :--- | :--- |
| `firewall_command` | `str` | Ready-to-run command (`sudo iptables -A INPUT -s <IP> -j DROP`) |
| `notification_dispatched`| `bool` | True if Discord/Slack webhook alert was sent successfully |

---

## 4. Work Division & Development Strategy

### Phase A: Contract Approval
* Prince & Vishwa review these 6 module contracts together.
* Once both agree on the field names, inputs, and outputs, **the contracts are frozen**.

### Phase B: Independent Module Development
Because the contracts are fixed, Prince and Vishwa can build their assigned modules in complete independence:
* **Prince develops:** Module 1 (Sanitizer), Module 2 (Parser), Module 3 (Threat Intel).
* **Vishwa develops:** Module 4 (Guardrail), Module 5 (AI Triage), Module 6 (SOAR Containment).

### Phase C: Integration
* Connecting Module 1 → 2 → 3/4 → 5 → 6 takes minimal effort because both teammates followed the exact same input/output contracts!
