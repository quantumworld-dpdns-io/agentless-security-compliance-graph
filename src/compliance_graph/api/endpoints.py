from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..models import ComplianceGraph
from ..services import ReportService

router = APIRouter()

def get_graph():
    from ..config import settings
    return ComplianceGraph(settings.database_url)

class NodeCreate(BaseModel):
    node_type: str
    name: str
    attributes: dict = {}

class EdgeCreate(BaseModel):
    source_id: str
    target_id: str
    edge_type: str
    weight: float = 1.0

@router.post("/nodes")
def create_node(data: NodeCreate, graph: ComplianceGraph = Depends(get_graph)):
    node_id = graph.add_node(data.node_type, data.name, data.attributes)
    return {"id": node_id, "status": "created"}

@router.post("/edges")
def create_edge(data: EdgeCreate, graph: ComplianceGraph = Depends(get_graph)):
    edge_id = graph.add_edge(data.source_id, data.target_id, data.edge_type, data.weight)
    return {"id": edge_id, "status": "created"}

@router.get("/graph/summary")
def graph_summary(graph: ComplianceGraph = Depends(get_graph)):
    return graph.get_compliance_summary()

@router.get("/traverse/{node_id}")
def traverse(node_id: str, depth: int = 5, graph: ComplianceGraph = Depends(get_graph)):
    return {"nodes": graph.bfs_traverse(node_id, depth)}

@router.get("/shortest-path")
def shortest_path(from_id: str, to_id: str, graph: ComplianceGraph = Depends(get_graph)):
    path = graph.shortest_path(from_id, to_id)
    return {"path": path, "length": len(path)}

@router.get("/compliance/report")
def compliance_report(graph: ComplianceGraph = Depends(get_graph)):
    summary = graph.get_compliance_summary()
    report = ReportService()
    return {"summary": summary, "report_text": report.generate_summary(summary)}
