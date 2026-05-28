# Architecture

## System Design

The Agentless Security Compliance Graph uses a layered architecture:

1. **Discovery Layer** — eBPF probes, passive scanning, OTel telemetry
2. **Graph Engine** — DuckDB-backed property graph with Rust native extensions
3. **Analysis Layer** — Classical graph algorithms + quantum-enhanced optimization
4. **AI Agent Layer** — LangGraph state machines, CrewAI multi-agent crews
5. **API Layer** — FastAPI REST endpoints + MCP server for AI integration
6. **Security Layer** — OWASP Top 10 tested, PQC-ready, ZK-proof attestation

## Data Flow

```
eBPF Probes → Event Ring Buffer → Normalization → Graph Nodes/Edges
Passive Scan → Discovery Service → DuckDB → Graph Traversal → Analysis
CVE Feeds → NVD API Client → CVE Nodes → Policy Engine → Violations
Quantum → Qiskit/CUDA-Q → QAOA/VQE → Compliance Optimization
AI Agents → LangGraph → CrewAI → MCP → Automated Remediation
```

## Component Diagram

See README.md for the C4-style component diagram.
