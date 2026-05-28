# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ |

## Reporting a Vulnerability

Report vulnerabilities to security@quantumworld.dev

## OWASP Top 10 Coverage

This project includes Robot Framework tests covering all OWASP Top 10:2021 categories. See `tests/robot/owasp_top10_tests.robot`.

## Post-Quantum Cryptography

The PQC module provides:
- Kyber-768 key encapsulation
- Dilithium-3 digital signatures
- TLS configuration auditing
- PQC migration readiness assessment

## Zero-Knowledge Proofs

Compliance attestations can be verified without revealing sensitive details using Noir circuits and RISC Zero zkVM.
