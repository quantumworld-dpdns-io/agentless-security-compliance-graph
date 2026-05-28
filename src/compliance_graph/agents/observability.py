
class LangSmithTracer:
    """LangSmith tracing for AI agent calls."""

    def __init__(self, project_name: str = "compliance-graph"):
        self.project_name = project_name
        self._available = self._check_langsmith()

    def _check_langsmith(self) -> bool:
        try:
            from langsmith import Client
            return True
        except ImportError:
            return False

    def trace(self, run_type: str, name: str, inputs: dict, outputs: dict):
        if self._available:
            from langsmith import Client
            client = Client()
            client.create_run(name=name, run_type=run_type, inputs=inputs, outputs=outputs)
            return {"traced": True}
        return {"traced": False, "message": "LangSmith not available"}


class WeaveTracker:
    """Weights & Biases Weave tracking for ML experiments."""

    def __init__(self, project: str = "compliance-graph"):
        self.project = project
        self._available = self._check_weave()

    def _check_weave(self) -> bool:
        try:
            import weave
            return True
        except ImportError:
            return False

    def init(self):
        if self._available:
            import weave
            weave.init(self.project)

    def log(self, data: dict):
        if self._available:
            import weave
            weave.log(data)
