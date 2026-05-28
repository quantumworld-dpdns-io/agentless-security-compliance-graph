# Agentless Security Compliance Graph 🔐

> **Agentless internal security compliance graph** — maps devices, AD accounts, CVEs, and policy gaps without a heavy agent.
>
> Built with eBPF + OpenTelemetry + DuckDB + LangGraph + Quantum Computing (Qiskit, CUDA-Q, ZK Proofs)

[![CI](https://github.com/quantumworld-dpdns-io/agentless-security-compliance-graph/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/agentless-security-compliance-graph/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/compliance-graph)](https://pypi.org/project/compliance-graph/)
[![Docker](https://img.shields.io/docker/v/quantumworld-dpdns-io/compliance-graph)](https://ghcr.io/quantumworld-dpdns-io/agentless-security-compliance-graph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange)](https://rust-lang.org)
[![Go](https://img.shields.io/badge/Go-1.22%2B-blue)](https://go.dev)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

---

## Overview

This repository is part of the [quantumworld-dpdns-io](https://github.com/quantumworld-dpdns-io) Wild SaaS & Tech Development initiative.

### What it does

- **Agentless discovery** — Uses eBPF probes and passive network scanning to discover devices, AD accounts, and network topology without installing agents
- **Compliance graph** — Maps relationships between devices, AD accounts, CVEs, and policy gaps in a property graph stored in DuckDB
- **Risk analysis** — Traverses attack paths, finds privilege escalation routes, calculates blast radius, and identifies critical compliance gaps
- **Quantum-enhanced optimization** — Leverages Qiskit, CUDA-Q, and zero-knowledge proofs (Noir, RISC Zero) for advanced graph optimization and verifiable compliance attestation
- **AI-powered analysis** — LangGraph state machines and CrewAI multi-agent crews for automated compliance scanning, analysis, and remediation
- **OWASP Top 10 tested** — Comprehensive Robot Framework test suite covering all OWASP Top 10:2021 categories
- **Enterprise ready** — Homebrew + Docker + PyPI distribution, Helm charts, Terraform IaC, and full CI/CD with GitHub Actions

### Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Core Engine** | Python 3.11+, DuckDB, LangGraph, FastAPI |
| **Native Extensions** | Rust (PyO3), C eBPF, Go (cilium/ebpf) |
| **Quantum Computing** | Qiskit, CUDA-Q, QAOA, VQE, Grover's Search |
| **Zero-Knowledge Proofs** | Noir, RISC Zero zkVM |
| **AI & Agents** | LangGraph, CrewAI, MCP, Claude Code, Codex |
| **Security** | OWASP Top 10, Robot Framework, PQC (liboqs), Cilium Tetragon |
| **Data Lakehouse** | Apache Iceberg, Parquet, Apache Polaris, DataFusion |
| **Vector Databases** | Chroma, Milvus, Weaviate, Qdrant, LanceDB |
| **Observability** | OpenTelemetry, LangSmith, Weights & Biases Weave, Arize Phoenix |
| **CI/CD & Release** | GitHub Actions, PyPI, Docker (multi-arch), Homebrew, Terraform |
| **Infrastructure** | Redis (Dragonfly), WebAssembly (Wasmtime, Fermyon Spin) |

---

## Quick Start

### Installation

```bash
# Via pip
pip install compliance-graph

# Via Homebrew (macOS)
brew install quantumworld-dpdns-io/tap/compliance-graph

# Via Docker
docker pull ghcr.io/quantumworld-dpdns-io/agentless-security-compliance-graph:latest
```

### Running the API

```bash
# Start the REST API
uvicorn compliance_graph.api.main:app --host 0.0.0.0 --port 8000

# Or use the CLI
compliance-graph --help
compliance-graph summary
```

### Docker Compose (full stack)

```bash
docker compose up -d
# Starts API, Redis, OTel collector, and DuckDB
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ LangGraph│  │ CrewAI   │  │ MCP      │  │ Claude     │  │
│  │ State    │  │ Multi-   │  │ Server   │  │ Code       │  │
│  │ Machines │  │ Agents   │  │ Tools    │  │ Plugin     │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │
├───────┴─────────────┴─────────────┴───────────────┴────────┤
│                    Quantum Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ Qiskit   │  │ CUDA-Q   │  │ QAOA/    │  │ ZK Proofs  │  │
│  │ Circuits │  │ GPU Sim  │  │ VQE Solver│  │ Noir/RISC0 │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │
├───────┴─────────────┴─────────────┴───────────────┴────────┤
│                  Compliance Graph Engine                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Graph Model (DuckDB + Rust Extensions)                │ │
│  │  • BFS/DFS Traversal  • Shortest Path  • Blast Radius │ │
│  │  • Privilege Escalation  • Reachability  • Degree     │ │
│  └────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│               Agentless Discovery Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │ eBPF     │  │ OpenTele-│  │ Passive  │  │ AD/LDAP    │  │
│  │ Probes   │  │ metry    │  │ Scanning │  │ Connector  │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Features

### Agentless Discovery

- **eBPF probes** — Process execution monitoring, TCP connection tracking, file integrity
- **Passive scanning** — SSDP/mDNS, ARP, DHCP, LLDP/CDP discovery
- **AD/LDAP integration** — Domain discovery, trust mapping, privilege analysis
- **OpenTelemetry** — Distributed tracing and metrics collection

### Compliance Graph

- **Property graph model** — Nodes (devices, AD accounts, CVEs, policy gaps) + typed edges
- **DuckDB-backed** — In-process OLAP with recursive CTEs for graph traversal
- **Rust extensions** — High-performance native graph algorithms via PyO3
- **Apache Iceberg** — Lakehouse compliance data with time-travel queries

### Quantum Computing

- **QAOA** — Max-Cut optimization for attack surface minimization
- **VQE** — Variational risk scoring for compliance posture
- **Grover's search** — Accelerated CVE lookup and correlation
- **CUDA-Q** — GPU-accelerated quantum circuit simulation
- **ZK Proofs** — Zero-knowledge compliance attestation via Noir and RISC Zero
- **Hybrid orchestrator** — Automatically selects quantum vs classical solver

### AI Agents

- **LangGraph** — Stateful compliance analysis workflows with conditional branching
- **CrewAI** — Multi-agent crews (Scanner, Analyzer, Reporter, Remediation)
- **MCP Server** — Model Context Protocol for AI tool integration (Claude Code, Codex)
- **LLM Provider** — Pluggable backend (OpenAI, Anthropic, Ollama, vLLM)

### Security Testing (Robot Framework + OWASP Top 10)

| OWASP Category | Test Coverage |
|---------------|--------------|
| A01: Broken Object Level Authorization | API endpoint authorization tests |
| A02: Broken Authentication | Token validation, credential testing |
| A03: Injection | SQLi, NoSQLi, LDAPi, OS command injection |
| A04: Insecure Design | Input validation, schema enforcement |
| A05: Security Misconfiguration | CORS, headers, method restrictions |
| A06: Sensitive Data Exposure | Secret scanning in responses |
| A08: SSRF | Internal metadata endpoint blocking |
| A09: Security Logging | Audit trail completeness |
| A10: Server-Side Request Forgery | URL validation bypass tests |

---

## CLI Reference

```bash
# Show compliance graph summary
compliance-graph summary

# Add a node
compliance-graph add-node --type device --name "server-01"

# Traverse graph from a node
compliance-graph traverse <node-id> --depth 5

# Find shortest path
compliance-graph path --from-id <id1> --to-id <id2>
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/nodes` | Create a node |
| POST | `/api/v1/edges` | Create an edge |
| GET | `/api/v1/graph/summary` | Graph summary stats |
| GET | `/api/v1/traverse/{node_id}` | BFS traversal |
| GET | `/api/v1/shortest-path` | Shortest path |
| GET | `/api/v1/compliance/report` | Compliance report |

---

## Project Structure

```
.
├── src/compliance_graph/        # Python package
│   ├── models/                  # Graph data models
│   ├── services/                # Core services
│   ├── api/                     # FastAPI REST endpoints
│   ├── cli/                     # Click CLI
│   ├── agents/                  # LangGraph, CrewAI, MCP
│   ├── quantum/                 # Qiskit, CUDA-Q, ZK proofs
│   ├── security/                # PQC, compliance audit
│   └── config/                  # Settings
├── native/                      # Rust native extensions (PyO3)
├── agentless/                   # Go eBPF control plane
│   └── ebpf/                    # C eBPF programs
├── agents/                      # TypeScript AI agents
├── tests/                       # Test suites
│   ├── unit/                    # pytest unit tests
│   ├── integration/             # API/CLI integration tests
│   ├── robot/                   # Robot Framework (OWASP Top 10)
│   └── benchmark/               # pytest-benchmark performance
├── docs/                        # Documentation
├── .github/workflows/           # CI/CD pipelines
├── scripts/                     # Terraform, Helm charts
├── contrib/homebrew/            # Homebrew formula
├── Dockerfile                   # Multi-stage container build
├── docker-compose.yml           # Full stack local dev
└── Makefile                     # Build automation
```

---

## Development

```bash
# Install in dev mode
make install

# Run tests
make test

# Run linting
make lint

# Build everything
make build

# Run benchmarks
make benchmark
```

### Running Robot Framework tests

```bash
# Start API first
uvicorn compliance_graph.api.main:app &

# Run Robot tests
robot --outputdir robot-results tests/robot/

# View results
open robot-results/report.html
```

---

## CI/CD Pipelines

| Workflow | Trigger | Description |
|----------|---------|-------------|
| **CI** | Push/PR to main | Lint, test, security scan, build |
| **Release** | Tag v*.*.* | PyPI publish, Docker multi-arch build, Homebrew |
| **Docker** | Weekly + push | Multi-arch container images |
| **CodeQL** | Push/schedule | GitHub CodeQL security analysis |
| **Dependabot** | Daily | Automated dependency updates |

### Release Process

```bash
# 1. Create a tag
git tag v0.1.0
git push origin v0.1.0

# 2. GitHub Actions automatically:
#    - Builds Python wheels
#    - Builds Go binaries (linux/amd64, darwin/amd64, darwin/arm64)
#    - Generates SBOM
#    - Signs packages with Sigstore
#    - Publishes to PyPI
#    - Builds and pushes Docker images (linux/amd64 + linux/arm64)
```

### Package Distribution

```
PyPI:    pip install compliance-graph
Docker:  ghcr.io/quantumworld-dpdns-io/agentless-security-compliance-graph
Homebrew: brew install quantumworld-dpdns-io/tap/compliance-graph
```

---

## Configuration

Environment variables (prefix `CG_`):

| Variable | Default | Description |
|----------|---------|-------------|
| `CG_ENVIRONMENT` | `dev` | Environment (dev/staging/production) |
| `CG_DATABASE_URL` | `compliance_graph.db` | DuckDB database path |
| `CG_REDIS_URL` | `redis://localhost:6379` | Redis connection string |
| `CG_OTEL_ENDPOINT` | `http://localhost:4317` | OpenTelemetry collector |
| `CG_LOG_LEVEL` | `INFO` | Logging level |

---

## Quantum Computing Integration

### Available Quantum Solvers

| Solver | Problem | Backend |
|--------|---------|---------|
| QAOA Max-Cut | Attack surface minimization | Qiskit/Aer, IBM Quantum |
| VQE Risk Scoring | Compliance posture scoring | Qiskit/Aer |
| Grover's Search | Accelerated CVE lookup | Qiskit Simulator |
| CUDA-Q Hybrid | General optimization | GPU/CUDA-Q, Aer fallback |

### Zero-Knowledge Proofs

```python
from compliance_graph.quantum.zk import NoirProver, NoirVerifier

prover = NoirProver()
proof = prover.generate_proof("graph_attestation", {"graph_hash": "0x..."})

verifier = NoirVerifier()
assert verifier.verify_proof(proof, public_inputs={})
```

---

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) before opening a pull request.

### Development Workflow

1. Fork and create a feature branch from `main`
2. Make changes with clear commit messages
3. Run `make lint && make test` before committing
4. Open a pull request with description of changes
5. Ensure all CI checks pass

---

## License

[MIT](LICENSE) — Copyright (c) 2026 quantumworld-dpdns-io

---

## Roadmap

- [x] Phase 1: Foundation & Project Scaffold
- [x] Phase 2: Core Compliance Engine (Classical)
- [x] Phase 3: Agentless Discovery & Telemetry
- [x] Phase 4: DuckDB & Iceberg Lakehouse
- [x] Phase 5: Quantum Computing Module
- [x] Phase 6: AI & Agentic Stack
- [x] Phase 7: Tool Expansion & Integrations
- [x] Phase 8: Security & Robot Framework Tests
- [x] Phase 9: CI/CD, Releases & Packaging
- [x] Phase 10: Production Hardening & Documentation
