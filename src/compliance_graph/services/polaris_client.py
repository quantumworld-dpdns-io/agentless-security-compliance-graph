
import httpx


class PolarisCatalogClient:
    """Apache Polaris Iceberg REST catalog client."""

    def __init__(self, endpoint: str = "http://localhost:8181", catalog_name: str = "compliance"):
        self.endpoint = endpoint
        self.catalog_name = catalog_name
        self.client = httpx.Client(base_url=endpoint, timeout=10.0)

    def list_namespaces(self) -> list[dict]:
        response = self.client.get(f"/api/catalog/v1/{self.catalog_name}/namespaces")
        response.raise_for_status()
        return response.json().get("namespaces", [])

    def create_namespace(self, namespace: str) -> dict:
        response = self.client.post(f"/api/catalog/v1/{self.catalog_name}/namespaces",
                                   json={"namespace": [namespace]})
        return {"status": response.status_code, "namespace": namespace}

    def health(self) -> dict:
        try:
            self.client.get("/api/management/v1/health")
            return {"status": "healthy", "polaris": True}
        except Exception:
            return {"status": "unreachable", "polaris": False}
