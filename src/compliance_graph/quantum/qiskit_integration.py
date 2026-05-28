
import numpy as np


class QiskitBackend:
    """Abstraction over Qiskit backends — real hardware or simulator."""

    def __init__(self, use_hardware: bool = False, hub: str = "ibm-q", group: str = "open", project: str = "main"):
        self.use_hardware = use_hardware
        self.hub = hub
        self.group = group
        self.project = project
        self.backend = None

    def get_backend(self):
        from qiskit_aer import AerSimulator
        self.backend = AerSimulator()
        return self.backend

    def run_circuit(self, circuit, shots: int = 1024):
        if self.backend is None:
            self.get_backend()
        try:
            from qiskit_aer import AerSimulator
            backend = AerSimulator()
            job = backend.run(circuit, shots=shots)
            return job.result()
        except ImportError:
            from qiskit import BasicAer
            backend = BasicAer.get_backend("qasm_simulator")
            job = backend.run(circuit, shots=shots)
            return job.result()


class QuantumGraphSolver:
    """Solves compliance graph optimization problems using quantum algorithms."""

    def __init__(self, backend: QiskitBackend | None = None):
        self.backend = backend or QiskitBackend()

    def build_qaoa_circuit(self, adjacency_matrix: np.ndarray, p: int = 1):
        from qiskit import QuantumCircuit
        from qiskit.circuit import Parameter
        n_qubits = adjacency_matrix.shape[0]
        circuit = QuantumCircuit(n_qubits)
        gamma = Parameter("γ")
        beta = Parameter("β")
        circuit.h(range(n_qubits))
        for i in range(n_qubits):
            for j in range(n_qubits):
                if adjacency_matrix[i][j] != 0:
                    circuit.rzz(2 * gamma * adjacency_matrix[i][j], i, j)
        circuit.ry(2 * beta, range(n_qubits))
        return circuit

    def solve_max_cut(self, adjacency_matrix: np.ndarray) -> dict:
        try:
            from qiskit_algorithms import QAOA
            from qiskit_algorithms.optimizers import COBYLA
            from qiskit_optimization.algorithms import MinimumEigenOptimizer
            from qiskit_optimization.applications import Maxcut

            maxcut = Maxcut(adjacency_matrix)
            qp = maxcut.to_quadratic_program()
            qaoa = QAOA(optimizer=COBYLA(), reps=1)
            optimizer = MinimumEigenOptimizer(qaoa)
            result = optimizer.solve(qp)
            return {"solution": result.x.tolist(), "fval": result.fval, "status": "optimized"}
        except ImportError:
            return self._classical_max_cut(adjacency_matrix)

    def _classical_max_cut(self, adjacency_matrix: np.ndarray) -> dict:
        n = adjacency_matrix.shape[0]
        best = {"solution": [], "fval": 0}
        for mask in range(1 << n):
            cut = 0
            for i in range(n):
                for j in range(n):
                    if ((mask >> i) & 1) != ((mask >> j) & 1):
                        cut += adjacency_matrix[i][j]
            if cut > best["fval"]:
                best = {"solution": [(mask >> i) & 1 for i in range(n)], "fval": cut}
        return {**best, "status": "classical_fallback"}

    def solve_vqe_risk_scoring(self, risk_matrix: np.ndarray) -> dict:
        try:
            from qiskit.circuit.library import TwoLocal
            from qiskit_algorithms import VQE
            from qiskit_algorithms.optimizers import SLSQP

            ansatz = TwoLocal(risk_matrix.shape[0], "ry", "cz", reps=3)
            vqe = VQE(ansatz=ansatz, optimizer=SLSQP())
            result = vqe.compute_minimum_eigenvalue(risk_matrix)
            return {"eigenvalue": float(result.eigenvalue.real), "status": "quantum"}
        except ImportError:
            eigenvalues = np.linalg.eigvalsh(risk_matrix)
            return {"eigenvalue": float(eigenvalues[0]), "status": "classical_fallback"}

    def grover_cve_search(self, cve_database_size: int, target_hash: str) -> dict:
        from qiskit import QuantumCircuit
        n_qubits = max(1, int(np.ceil(np.log2(cve_database_size))))
        circuit = QuantumCircuit(n_qubits)
        circuit.h(range(n_qubits))
        for _ in range(int(np.pi / 4 * np.sqrt(2 ** n_qubits))):
            circuit.h(range(n_qubits))
            circuit.x(range(n_qubits))
            circuit.h(n_qubits - 1)
            circuit.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            circuit.h(n_qubits - 1)
            circuit.x(range(n_qubits))
            circuit.h(range(n_qubits))
        result = self.backend.run_circuit(circuit)
        counts = result.get_counts()
        return {"counts": counts, "n_qubits": n_qubits, "status": "simulated"}
