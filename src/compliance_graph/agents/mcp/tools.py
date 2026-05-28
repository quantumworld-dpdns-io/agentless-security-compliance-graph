from ...models import ComplianceGraph
from ...services import CVEIngestionService, ReportService

class ToolRegistry:
    """Registry of MCP tools for the compliance graph."""

    def __init__(self, server):
        self.server = server
        self.graph = ComplianceGraph()
        self.cve_service = CVEIngestionService(self.graph)
        self.reporter = ReportService()
        self._register_all()

    def _register_all(self):
        self.server.register_tool("query_graph", self._query_graph, "Query the compliance graph")
        self.server.register_tool("scan_device", self._scan_device, "Scan a device for compliance")
        self.server.register_tool("assess_compliance", self._assess_compliance, "Assess overall compliance posture")
        self.server.register_tool("generate_report", self._generate_report, "Generate a compliance report")
        self.server.register_tool("recent_cves", self._recent_cves, "Fetch recent CVE data")

    async def _query_graph(self, **kwargs):
        return self.graph.get_compliance_summary()

    async def _scan_device(self, ip: str = "127.0.0.1", **kwargs):
        return {"ip": ip, "status": "simulated", "open_ports": [22, 80, 443], "os": "Linux"}

    async def _assess_compliance(self, framework: str = "cis", **kwargs):
        return {"framework": framework, "score": 78.5, "passed": 42, "failed": 12, "total": 54}

    async def _generate_report(self, report_type: str = "summary", **kwargs):
        return {"report_type": report_type, "content": self.reporter.generate_summary(self.graph.get_compliance_summary())}

    async def _recent_cves(self, days: int = 7, **kwargs):
        cves = self.cve_service.fetch_recent_cves(days)
        return {"count": len(cves), "cves": [c.cve_id for c in cves]}
