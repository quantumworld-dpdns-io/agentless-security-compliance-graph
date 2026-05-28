from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import uuid4

class BaseNode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    node_type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict)

class DeviceNode(BaseNode):
    node_type: str = "device"
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    os_version: Optional[str] = None
    open_ports: list[int] = Field(default_factory=list)
    is_active: bool = True

class ADAccountNode(BaseNode):
    node_type: str = "ad_account"
    sam_account_name: Optional[str] = None
    distinguished_name: Optional[str] = None
    is_admin: bool = False
    is_service_account: bool = False
    last_logon: Optional[datetime] = None

class CVENode(BaseNode):
    node_type: str = "cve"
    cve_id: str
    cvss_score: Optional[float] = None
    severity: Optional[str] = None
    is_exploited: bool = False
    published_date: Optional[datetime] = None
    description: Optional[str] = None

class PolicyGapNode(BaseNode):
    node_type: str = "policy_gap"
    policy_id: str
    framework: str = "custom"
    severity: str = "medium"
    remediation: Optional[str] = None
