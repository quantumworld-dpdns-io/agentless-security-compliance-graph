import click
from rich.console import Console
from rich.table import Table

from ..models import ComplianceGraph
from ..services import CVEIngestionService, ReportService, ScannerService

console = Console()
graph = ComplianceGraph()

@click.group()
def cli():
    """Agentless Security Compliance Graph CLI"""

@cli.command()
def summary():
    """Show compliance graph summary"""
    data = graph.get_compliance_summary()
    table = Table(title="Compliance Graph Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    for key, value in data.items():
        table.add_row(str(key), str(value))
    console.print(table)

@cli.command()
@click.option("--type", "node_type", required=True, help="Node type")
@click.option("--name", required=True, help="Node name")
def add_node(node_type: str, name: str):
    """Add a node to the compliance graph"""
    nid = graph.add_node(node_type, name)
    console.print(f"[green]Node added:[/green] {nid}")

@cli.command()
@click.argument("node_id")
@click.option("--depth", default=5, help="Max traversal depth")
def traverse(node_id: str, depth: int):
    """Traverse graph from a node"""
    nodes = graph.bfs_traverse(node_id, depth)
    table = Table(title=f"Traversal from {node_id}")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Type")
    for n in nodes:
        table.add_row(str(n[0]), str(n[1]), str(n[2]))
    console.print(table)

@cli.command()
@click.option("--from-id", required=True)
@click.option("--to-id", required=True)
def path(from_id: str, to_id: str):
    """Find shortest path between two nodes"""
    path = graph.shortest_path(from_id, to_id)
    if path:
        console.print(f"[green]Path:[/green] {' → '.join(path)}")
    else:
        console.print("[red]No path found[/red]")

if __name__ == "__main__":
    cli()
