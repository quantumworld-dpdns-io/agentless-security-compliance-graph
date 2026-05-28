"""Unit tests for the compliance graph data model."""

import pytest
from compliance_graph.models import ComplianceGraph
import uuid

@pytest.fixture
def graph(tmp_path):
    db_path = tmp_path / "test.db"
    g = ComplianceGraph(str(db_path))
    yield g
    g.close()

def test_add_node(graph):
    node_id = graph.add_node("device", "test-device-01", {"ip": "192.168.1.1"})
    assert node_id is not None
    assert isinstance(node_id, str)

def test_add_edge(graph):
    n1 = graph.add_node("device", "device-a")
    n2 = graph.add_node("device", "device-b")
    edge_id = graph.add_edge(n1, n2, "CONNECTS_TO", weight=1.0)
    assert edge_id is not None
    assert isinstance(edge_id, str)

def test_graph_summary(graph):
    graph.add_node("device", "d1")
    graph.add_node("cve", "CVE-2024-0001")
    graph.add_node("ad_account", "admin@corp")
    summary = graph.get_compliance_summary()
    assert summary["total_nodes"] == 3
    assert summary["nodes_by_type"]["device"] == 1
    assert summary["nodes_by_type"]["cve"] == 1

def test_bfs_traversal(graph):
    n1 = graph.add_node("device", "gateway")
    n2 = graph.add_node("device", "server-01")
    n3 = graph.add_node("device", "workstation-01")
    graph.add_edge(n1, n2, "ROUTES_TO")
    graph.add_edge(n2, n3, "ROUTES_TO")
    nodes = graph.bfs_traverse(n1, depth=5)
    assert len(nodes) >= 2

def test_shortest_path(graph):
    n1 = graph.add_node("device", "start")
    n2 = graph.add_node("device", "mid")
    n3 = graph.add_node("device", "end")
    graph.add_edge(n1, n2, "CONNECTS")
    graph.add_edge(n2, n3, "CONNECTS")
    path = graph.shortest_path(n1, n3)
    assert len(path) >= 2

def test_node_types(graph):
    types = ["device", "cve", "ad_account", "policy_gap"]
    for t in types:
        graph.add_node(t, f"test-{t}")
    summary = graph.get_compliance_summary()
    assert summary["total_nodes"] == 4
