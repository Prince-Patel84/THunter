"""
THunter - Core System Contracts & Data Transfer Objects (DTOs)
Formal Interface Specification for Prince Patel & Vishwa Prajapati

This file defines ONLY the data schemas and contracts between modules.
No business logic or implementation code belongs in this file.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# =====================================================================
# Module 1 Contract: SanitizerModule (Prince)
# =====================================================================

class SanitizedResult(BaseModel):
    """Output contract for Module 1 (Sanitizer)."""
    original_text: str = Field(description="The unmodified input log line.")
    sanitized_text: str = Field(description="The log line with private IPs and secrets masked.")
    redaction_count: int = Field(default=0, description="Total count of sensitive items redacted.")
    redacted_types: List[str] = Field(default_factory=list, description="Categories masked (e.g. ['INTERNAL_IP', 'PASSWORD']).")

    @property
    def was_sanitized(self) -> bool:
        return self.redaction_count > 0


# =====================================================================
# Module 2 Contract: ParserModule (Prince)
# =====================================================================

class EventType(str, Enum):
    WEB_REQUEST = "WEB_REQUEST"
    SSH_AUTH = "SSH_AUTH"
    UNKNOWN = "UNKNOWN"


class NormalizedEvent(BaseModel):
    """Output contract for Module 2 (Parser)."""
    raw_sanitized_log: str = Field(description="The sanitized log line from Module 1.")
    event_type: EventType = Field(default=EventType.UNKNOWN, description="Identified telemetry category.")
    source_ip: Optional[str] = Field(default=None, description="Client or attacker IP address.")
    timestamp: Optional[str] = Field(default=None, description="Extracted log timestamp.")
    target_resource: Optional[str] = Field(default=None, description="Accessed URI path (web) or targeted user (SSH).")
    http_method: Optional[str] = Field(default=None, description="HTTP method (GET, POST, etc.) if applicable.")
    status_code: Optional[int] = Field(default=None, description="HTTP status code (200, 404, etc.) or None.")
    untrusted_payload: str = Field(default="", description="Portion of log containing user-supplied input to check for attacks.")


# =====================================================================
# Module 3 Contract: ThreatIntelModule (Prince)
# =====================================================================

class ThreatIntelReport(BaseModel):
    """Output contract for Module 3 (Threat Intelligence / AbuseIPDB)."""
    ip: str = Field(description="The queried IPv4 address.")
    abuse_confidence_score: int = Field(default=0, ge=0, le=100, description="Abuse confidence score (0-100%).")
    total_reports: int = 0
    country_code: str = "UNKNOWN"
    isp: str = "UNKNOWN"
    is_tor_exit_node: bool = False
    is_malicious: bool = False


# =====================================================================
# Module 4 Contract: GuardrailModule (Vishwa)
# =====================================================================

class GuardrailVerdict(BaseModel):
    """Output contract for Module 4 (Prompt Injection Guardrail)."""
    is_prompt_injection: bool = Field(default=False, description="True if adversarial injection patterns are detected.")
    risk_score: int = Field(default=0, ge=0, le=100, description="Confidence/risk score (0-100).")
    flagged_patterns: List[str] = Field(default_factory=list, description="List of matched adversarial regex patterns.")
    disarmed_payload: str = Field(default="", description="Sanitized payload with dangerous instructions neutralized.")


# =====================================================================
# Module 5 Contract: AITriageModule (Vishwa)
# =====================================================================

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentTriageReport(BaseModel):
    """Output contract for Module 5 (Gemini AI Reasoning Engine)."""
    threat_title: str = Field(description="Short 3-7 word incident title.")
    mitre_attack_id: str = Field(description="Official MITRE ATT&CK technique code (e.g. T1190, T1110).")
    severity: SeverityLevel = Field(description="Incident severity level.")
    confidence_score: int = Field(ge=0, le=100, description="AI confidence score.")
    summary: str = Field(description="2-3 sentence plain English description for human analysts.")
    recommended_action: str = Field(description="Concrete remediation instruction.")


# =====================================================================
# Module 6 Contract: SOARModule (Vishwa)
# =====================================================================

class ContainmentPlan(BaseModel):
    """Output contract for Module 6 (SOAR Containment & Alerting)."""
    firewall_command: str = Field(default="", description="Exact CLI command to block the malicious IP.")
    notification_dispatched: bool = Field(default=False, description="True if Discord/Slack webhook alert was sent.")
