from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


def _now():
    return datetime.now(timezone.utc)

class BaseNode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    node_type: str
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    metadata: dict = Field(default_factory=dict)

class DeviceNode(BaseNode):
    node_type: str = "device"
    ip_address: str | None = None
    mac_address: str | None = None
    os_version: str | None = None
    open_ports: list[int] = Field(default_factory=list)
    is_active: bool = True

class ADAccountNode(BaseNode):
    node_type: str = "ad_account"
    sam_account_name: str | None = None
    distinguished_name: str | None = None
    is_admin: bool = False
    is_service_account: bool = False
    last_logon: datetime | None = None

class CVENode(BaseNode):
    node_type: str = "cve"
    cve_id: str
    cvss_score: float | None = None
    severity: str | None = None
    is_exploited: bool = False
    published_date: datetime | None = None
    description: str | None = None

class PolicyGapNode(BaseNode):
    node_type: str = "policy_gap"
    policy_id: str
    framework: str = "custom"
    severity: str = "medium"
    remediation: str | None = None
