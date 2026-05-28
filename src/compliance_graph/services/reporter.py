from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import json
from datetime import datetime

class ReportService:
    def __init__(self, template_dir: Optional[Path] = None):
        self.env = Environment(loader=FileSystemLoader(template_dir or Path("templates")))

    def generate_summary(self, graph_summary: dict) -> str:
        total = graph_summary.get("total_nodes", 0)
        cves = graph_summary.get("nodes_by_type", {}).get("cve", 0)
        devices = graph_summary.get("nodes_by_type", {}).get("device", 0)
        return f"""Compliance Summary
===================
Total Nodes: {total}
Devices: {devices}
CVEs: {cves}
Total Edges: {graph_summary.get('total_edges', 0)}
Generated: {datetime.utcnow().isoformat()}
"""

    def generate_html_report(self, data: dict) -> str:
        template = self.env.from_string("""<!DOCTYPE html>
<html><head><title>Compliance Report</title></head><body>
<h1>Compliance Report</h1>
<p>Generated: {{ now }}</p>
<h2>Summary</h2>
<ul>
{% for key, value in summary.items() %}
<li>{{ key }}: {{ value }}</li>
{% endfor %}
</ul>
</body></html>""")
        return template.render(summary=data, now=datetime.utcnow().isoformat())

    def export_json(self, data: dict) -> str:
        return json.dumps(data, indent=2, default=str)
