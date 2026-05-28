import pytest

from compliance_graph.models import ComplianceGraph, CVENode


@pytest.fixture
def graph(tmp_path):
    return ComplianceGraph(str(tmp_path / "cve_test.db"))

def test_cve_model(graph):
    cve = CVENode(cve_id="CVE-2024-TEST", cvss_score=7.5, severity="HIGH")
    assert cve.cve_id == "CVE-2024-TEST"
    assert cve.cvss_score == 7.5

def test_cve_attributes(graph):
    cve = CVENode(
        cve_id="CVE-2024-TEST2",
        cvss_score=9.1,
        severity="CRITICAL",
        description="Test CVE",
        is_exploited=False,
    )
    assert hasattr(cve, "cve_id")
    assert hasattr(cve, "cvss_score")
    assert cve.severity == "CRITICAL"
    assert cve.description == "Test CVE"

def test_cve_ingestion_to_graph(graph):
    from compliance_graph.services.cve_ingestion import CVEIngestionService
    service = CVEIngestionService(graph)
    cves = [CVENode(cve_id="CVE-2024-TEST3", cvss_score=5.0, severity="MEDIUM")]
    count = service.ingest_to_graph(cves)
    assert count == 1
    summary = graph.get_compliance_summary()
    assert summary["total_nodes"] >= 1
