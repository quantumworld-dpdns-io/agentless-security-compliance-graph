# ADR-001: Initial Technology Stack

**Date:** 2026-05-28

**Status:** Accepted

## Context
Need to select a technology stack for an agentless security compliance graph.

## Decision
- **Primary Language:** Python 3.11+ (ecosystem for ML, quantum, AI, data)
- **Native Extensions:** Rust via PyO3 for performance-critical graph algorithms
- **eBPF Control Plane:** Go via cilium/ebpf library
- **AI Agents:** TypeScript for LangGraph.js compatibility
- **Database:** DuckDB (embedded analytical) + Apache Iceberg (lakehouse)
- **Quantum:** Qiskit (primary) + CUDA-Q (GPU acceleration)
- **Packaging:** PyPI + Docker (multi-arch) + Homebrew

## Consequences
- Polyglot codebase requires tooling for each language
- Python provides fastest path to feature completeness
- Rust ensures performance for graph operations
