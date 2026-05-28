from hypothesis import given
from hypothesis import strategies as st

from compliance_graph.models import ComplianceGraph


@given(st.text(min_size=1, max_size=64), st.text(min_size=1, max_size=64))
def test_node_id_is_unique(name1, name2):
    graph = ComplianceGraph(":memory:")
    n1 = graph.add_node("device", name1)
    n2 = graph.add_node("device", name2)
    assert n1 != n2
    graph.close()


@given(st.integers(min_value=1, max_value=100))
def test_graph_summary_counts(n):
    graph = ComplianceGraph(":memory:")
    for i in range(n):
        graph.add_node("device", f"d{i}")
    summary = graph.get_compliance_summary()
    assert summary["total_nodes"] == n
    graph.close()
