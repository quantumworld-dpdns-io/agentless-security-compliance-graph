from datetime import datetime

import httpx

from ..models import ComplianceGraph, CVENode


class CVEIngestionService:
    NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def __init__(self, graph: ComplianceGraph):
        self.graph = graph
        self.client = httpx.Client(timeout=30.0)

    def fetch_recent_cves(self, days: int = 7) -> list[CVENode]:
        params = {
            "pubStartDate": datetime.utcnow().isoformat(),
            "resultsPerPage": 50,
        }
        response = self.client.get(self.NVD_API_BASE, params=params)
        response.raise_for_status()
        data = response.json()
        cves = []
        for item in data.get("vulnerabilities", []):
            cve_data = item.get("cve", {})
            metrics = cve_data.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {})
            cve = CVENode(
                cve_id=cve_data.get("id"),
                cvss_score=metrics.get("baseScore"),
                severity=metrics.get("baseSeverity"),
                description=cve_data.get("descriptions", [{}])[0].get("value"),
                published_date=cve_data.get("published"),
            )
            cves.append(cve)
        return cves

    def ingest_to_graph(self, cves: list[CVENode]) -> int:
        count = 0
        for cve in cves:
            self.graph.add_node(
                node_type="cve",
                name=cve.cve_id,
                attributes=cve.model_dump()
            )
            count += 1
        return count
