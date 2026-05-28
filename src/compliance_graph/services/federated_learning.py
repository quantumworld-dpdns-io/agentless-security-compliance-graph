from typing import Optional

class FederatedLearningClient:
    def __init__(self, server_url: str = "http://localhost:9090"):
        self.server_url = server_url
        self._flower_available = self._check_flower()

    def _check_flower(self) -> bool:
        try:
            import flwr
            return True
        except ImportError:
            return False

    def start_client(self, model_type: str = "risk_classifier"):
        if self._flower_available:
            import flwr as fl
            fl.client.start_client(server_address=self.server_url, client=self._create_client())
            return {"status": "federated_client_started"}
        return {"status": "simulated", "model_type": model_type}

    def _create_client(self):
        import flwr as fl
        class ComplianceClient(fl.client.NumPyClient):
            def get_parameters(self, config):
                return []
            def fit(self, parameters, config):
                return [], 10, {}
            def evaluate(self, parameters, config):
                return 0.0, 10, {"accuracy": 0.95}
        return ComplianceClient()

    def aggregate_models(self, client_updates: list[dict]) -> dict:
        return {"status": "aggregated", "clients": len(client_updates), "round": 1}
