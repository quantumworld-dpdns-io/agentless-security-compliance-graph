import numpy as np

from compliance_graph.quantum.classical_quantum_interface import HybridOrchestrator


class TestQuantumPerformance:

    def test_quantum_vs_classical_small(self, benchmark):
        orchestrator = HybridOrchestrator()
        data = np.random.rand(8, 8)
        data = (data + data.T) / 2
        benchmark(orchestrator.solve_graph_problem, "max_cut", data)

    def test_benchmark_runner(self, benchmark):
        orchestrator = HybridOrchestrator()
        results = orchestrator.benchmark_comparison([4, 6, 8])
        assert 4 in results
        assert 6 in results
        assert 8 in results
