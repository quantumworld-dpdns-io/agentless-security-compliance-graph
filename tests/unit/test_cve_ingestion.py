import pytest
from compliance_graph.services.cve_ingestion import CVEIngestionService
from compliance_graph.models import ComplianceGraph

@pytest.fixture
def service(tmp_path):
    g = ComplianceGraph(str(tmp_path / "cve_test.db"))
    return CVEIngestionService(g)

def test_cve_model(service):
    cves = service.fetch_recent_cves(days=1)
    assert isinstance(cves, list)

def test_cve_attributes(service):
    cves = service.fetch_recent_cves(days=1)
    if cves:
        cve = cves[0]
        assert hasattr(cve, "cve_id")
        assert hasattr(cve, "cvss_score")
