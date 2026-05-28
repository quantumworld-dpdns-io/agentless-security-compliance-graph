import pytest

from compliance_graph.agents.langgraph_agent import ComplianceAnalyzer
from compliance_graph.agents.llm import LLMProvider
from compliance_graph.agents.mcp.server import MCPServer


@pytest.mark.asyncio
async def test_compliance_analyzer():
    analyzer = ComplianceAnalyzer()
    result = await analyzer.analyze("Check compliance for all devices")
    assert result is not None

def test_mcp_server():
    server = MCPServer()
    server.register_tool("ping", lambda: "pong", "Ping tool")
    tools = server.tools
    assert "ping" in tools

def test_mcp_handle_tools_list():
    server = MCPServer()
    server.register_tool("test", lambda: None, "Test tool")
    import asyncio
    response = asyncio.run(server.handle_request({"method": "tools/list"}))
    assert "tools" in response
    assert len(response["tools"]) == 1

def test_llm_provider_init():
    provider = LLMProvider(provider="ollama")
    assert provider.provider == "ollama"
