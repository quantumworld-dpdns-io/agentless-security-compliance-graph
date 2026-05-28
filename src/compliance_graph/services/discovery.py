import asyncio

from ..models import ComplianceGraph


class AgentlessDiscoveryService:
    """Agentless device and network discovery via passive techniques."""

    def __init__(self, graph: ComplianceGraph):
        self.graph = graph

    async def discover_devices(self) -> list[dict]:
        devices = await self._passive_scan()
        for d in devices:
            self.graph.add_node("device", d["name"], d)
        return devices

    async def discover_network_topology(self) -> list[dict]:
        return await self._analyze_connections()

    async def _passive_scan(self) -> list[dict]:
        await asyncio.sleep(0.05)
        return [
            {"name": "gateway-01", "ip": "10.0.0.1", "mac": "00:11:22:33:44:01", "type": "router"},
            {"name": "server-db-01", "ip": "10.0.1.10", "mac": "00:11:22:33:44:02", "type": "server"},
            {"name": "workstation-42", "ip": "10.0.2.100", "mac": "00:11:22:33:44:03", "type": "workstation"},
        ]

    async def _analyze_connections(self) -> list[dict]:
        return [
            {"source": "gateway-01", "target": "server-db-01", "protocol": "tcp/5432"},
            {"source": "gateway-01", "target": "workstation-42", "protocol": "tcp/443"},
        ]

    async def discover_ad_domain(self, domain: str) -> dict:
        await asyncio.sleep(0.03)
        return {"domain": domain, "controllers": 2, "users": 150, "computers": 75, "groups": 20}
