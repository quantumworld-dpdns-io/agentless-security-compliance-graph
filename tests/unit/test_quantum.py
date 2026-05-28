import pytest
import numpy as np
from compliance_graph.quantum.qiskit_integration import QuantumGraphSolver, QiskitBackend
from compliance_graph.quantum.classical_quantum_interface import HybridOrchestrator

def test_qiskit_backend_initialization():
    backend = QiskitBackend()
    assert backend.use_hardware is False

def test_quantum_solver_max_cut():
    solver = QuantumGraphSolver()
    matrix = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
    result = solver.solve_max_cut(matrix)
    assert "solution" in result
    assert "fval" in result

def test_vqe_risk_scoring():
    solver = QuantumGraphSolver()
    matrix = np.random.rand(4, 4)
    matrix = (matrix + matrix.T) / 2
    result = solver.solve_vqe_risk_scoring(matrix)
    assert "eigenvalue" in result

def test_grover_cve_search():
    solver = QuantumGraphSolver()
    result = solver.grover_cve_search(16, "target_hash")
    assert "counts" in result or "status" in result

def test_hybrid_orchestrator():
    orchestrator = HybridOrchestrator()
    data = np.random.rand(6, 6)
    result = orchestrator.solve_graph_problem("max_cut", data)
    assert result is not None

def test_benchmark_comparison():
    orchestrator = HybridOrchestrator()
    results = orchestrator.benchmark_comparison(problem_sizes=[4, 6])
    assert 4 in results
    assert 6 in results
