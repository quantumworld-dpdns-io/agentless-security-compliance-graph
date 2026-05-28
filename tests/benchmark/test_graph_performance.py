import pytest
import numpy as np
from compliance_graph.models import ComplianceGraph

class TestGraphPerformance:
    
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        self.graph = ComplianceGraph(str(tmp_path / "bench.db"))

    def test_add_nodes_benchmark(self, benchmark):
        benchmark(self._add_nodes)

    def _add_nodes(self):
        for i in range(100):
            self.graph.add_node("device", f"bench-node-{i}", {"index": i})

    def test_graph_traversal_benchmark(self, benchmark):
        self._build_large_graph(500)
        all_nodes = self.graph.conn.execute("SELECT id FROM nodes LIMIT 1").fetchone()
        if all_nodes:
            benchmark(self.graph.bfs_traverse, all_nodes[0], 5)

    def _build_large_graph(self, size):
        ids = []
        for i in range(size):
            nid = self.graph.add_node("device", f"large-{i}")
            ids.append(nid)
        for i in range(size - 1):
            self.graph.add_edge(ids[i], ids[i + 1], "CONNECTS")
