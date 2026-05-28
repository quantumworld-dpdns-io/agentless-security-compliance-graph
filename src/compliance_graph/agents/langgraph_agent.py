from typing import TypedDict, Literal, Optional
from ..models import ComplianceGraph
from ..services.policy_engine import PolicyEngine

class AgentState(TypedDict):
    query: str
    graph_data: Optional[dict]
    analysis_result: Optional[dict]
    policy_violations: list[dict]
    recommendations: list[str]
    status: str

def create_compliance_graph():
    try:
        from langgraph.graph import StateGraph, END
        workflow = StateGraph(AgentState)

        async def fetch_graph_data(state: AgentState) -> AgentState:
            graph = ComplianceGraph()
            state["graph_data"] = graph.get_compliance_summary()
            graph.close()
            return state

        async def analyze_compliance(state: AgentState) -> AgentState:
            engine = PolicyEngine()
            violations = []
            if state.get("graph_data"):
                for node_type, count in state["graph_data"].get("nodes_by_type", {}).items():
                    result = engine.evaluate({"type": node_type, "count": count})
                    violations.extend(result)
            state["policy_violations"] = violations
            state["status"] = "analyzed"
            return state

        async def generate_recommendations(state: AgentState) -> AgentState:
            state["recommendations"] = []
            for v in state.get("policy_violations", []):
                state["recommendations"].append(
                    f"Remediate {v['rule']} ({v['severity']}): {v['message']}"
                )
            state["status"] = "complete"
            return state

        def should_continue(state: AgentState) -> Literal["analyze", "recommend", "end"]:
            if state["status"] == "pending":
                return "analyze"
            elif state["status"] == "analyzed":
                return "recommend"
            return "end"

        workflow.add_node("fetch_data", fetch_graph_data)
        workflow.add_node("analyze", analyze_compliance)
        workflow.add_node("recommend", generate_recommendations)
        workflow.set_entry_point("fetch_data")
        workflow.add_conditional_edges("fetch_data", should_continue)
        workflow.add_conditional_edges("analyze", should_continue)
        workflow.add_edge("recommend", END)
        workflow.set_finish_point("recommend")

        return workflow.compile()
    except ImportError:
        return None


class ComplianceAnalyzer:
    """LangGraph-based compliance analysis agent."""

    def __init__(self):
        self.graph = create_compliance_graph()

    async def analyze(self, query: str) -> dict:
        if self.graph is None:
            return {"status": "fallback", "message": "LangGraph not available, using direct analysis"}
        initial_state: AgentState = {
            "query": query,
            "graph_data": None,
            "analysis_result": None,
            "policy_violations": [],
            "recommendations": [],
            "status": "pending"
        }
        result = await self.graph.ainvoke(initial_state)
        return result

    def analyze_sync(self, query: str) -> dict:
        import asyncio
        return asyncio.run(self.analyze(query))
