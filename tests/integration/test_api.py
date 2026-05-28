import pytest
from httpx import AsyncClient, ASGITransport
from compliance_graph.api.main import app

@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")

@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_create_node(client):
    response = await client.post("/api/v1/nodes", json={
        "node_type": "device",
        "name": "test-device",
        "attributes": {"ip": "10.0.0.1"}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "created"
    assert "id" in data

@pytest.mark.asyncio
async def test_graph_summary(client):
    response = await client.get("/api/v1/graph/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_nodes" in data
