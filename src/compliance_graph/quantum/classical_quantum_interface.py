from typing import Optional
import numpy as np
from .qiskit_integration import QuantumGraphSolver
from .cuda_q_integration import HybridSolver

class HybridOrchestrator:
    """Orchestrates between classical and quantum solvers based on problem characteristics."""

    def __init__(self, quantum_threshold: int = 20, use_quantum: bool = True):
        self.quantum_threshold = quantum_threshold
        self.use_quantum = use_quantum
        self.qiskit_solver = QuantumGraphSolver()
        self.hybrid_solver = HybridSolver()

    def solve_graph_problem(self, problem_type: str, data: np.ndarray) -> dict:
        n = data.shape[0]
        if n < self.quantum_threshold and not self.use_quantum:
            return self._classical_fallback(problem_type, data)
        
        if problem_type == "max_cut":
            return self.qiskit_solver.solve_max_cut(data)
        elif problem_type == "risk_scoring":
            return self.qiskit_solver.solve_vqe_risk_scoring(data)
        elif problem_type == "optimization":
            return self.hybrid_solver.solve_compliance_optimization(data)
        else:
            return self._classical_fallback(problem_type, data)

    def _classical_fallback(self, problem_type: str, data: np.ndarray) -> dict:
        return {"solution": "classical", "problem_type": problem_type, "status": "fallback"}

    def benchmark_comparison(self, problem_sizes: list[int] = None) -> dict:
        if problem_sizes is None:
            problem_sizes = [4, 8, 12, 16, 20, 24]
        import time
        results = {}
        for n in problem_sizes:
            data = np.random.rand(n, n)
            data = (data + data.T) / 2
            
            start = time.perf_counter()
            quantum = self.solve_graph_problem("max_cut", data)
            q_time = time.perf_counter() - start
            
            self.use_quantum = False
            start = time.perf_counter()
            classical = self._classical_fallback("max_cut", data)
            c_time = time.perf_counter() - start
            self.use_quantum = True
            
            results[n] = {
                "quantum_time": q_time,
                "classical_time": c_time,
                "speedup": c_time / q_time if q_time > 0 else float('inf')
            }
        return results
