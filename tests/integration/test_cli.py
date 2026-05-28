import subprocess
import sys

def test_cli_help():
    result = subprocess.run([sys.executable, "-m", "compliance_graph", "--help"],
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert "Usage" in result.stdout

def test_cli_summary():
    result = subprocess.run([sys.executable, "-m", "compliance_graph", "summary"],
                          capture_output=True, text=True)
    assert result.returncode == 0
