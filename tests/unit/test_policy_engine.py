
import pytest

from compliance_graph.services.policy_engine import PolicyEngine


@pytest.fixture
def engine(tmp_path):
    policies_dir = tmp_path / "policies"
    policies_dir.mkdir()
    (policies_dir / "cis_foundation.yaml").write_text("""
name: CIS Foundation Benchmark
severity: high
condition:
  field: os_version
  operator: contains
  value: Windows
message: Windows devices require additional CIS hardening
""")
    return PolicyEngine(rules_dir=policies_dir)

def test_policy_violation(engine):
    result = engine.evaluate({"os_version": "Windows 10", "type": "device"})
    assert len(result) == 1
    assert result[0]["rule"] == "cis_foundation"

def test_policy_compliance(engine):
    result = engine.evaluate({"os_version": "Ubuntu 22.04", "type": "device"})
    assert len(result) == 0

def test_evaluate_condition_operators(engine):
    assert engine._check_condition(5, "gt", 3)
    assert engine._check_condition("a", "in", ["a", "b", "c"])
    assert engine._check_condition("hello", "contains", "ell")
    assert engine._check_condition(10, "eq", 10)
    assert not engine._check_condition(5, "eq", 10)
