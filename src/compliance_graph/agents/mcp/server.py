import json
import sys
from typing import Any

class MCPServer:
    """MCP (Model Context Protocol) server for compliance graph tools."""

    def __init__(self, name: str = "compliance-graph"):
        self.name = name
        self.tools = {}
        self.resources = {}
        self._running = False

    def register_tool(self, name: str, handler: callable, description: str = ""):
        self.tools[name] = {"handler": handler, "description": description}

    def register_resource(self, uri: str, handler: callable):
        self.resources[uri] = handler

    async def handle_request(self, request: dict) -> dict:
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "tools/list":
            return {"tools": [{"name": n, "description": d["description"]} for n, d in self.tools.items()]}
        elif method == "tools/call":
            tool_name = params.get("name")
            if tool_name in self.tools:
                result = await self.tools[tool_name]["handler"](**params.get("arguments", {}))
                return {"content": [{"type": "text", "text": json.dumps(result, default=str)}]}
            return {"error": f"Tool {tool_name} not found"}
        elif method == "resources/list":
            return {"resources": list(self.resources.keys())}
        elif method == "resources/read":
            uri = params.get("uri")
            if uri in self.resources:
                return {"contents": [{"uri": uri, "text": json.dumps(self.resources[uri](), default=str)}]}
            return {"error": f"Resource {uri} not found"}
        return {"error": f"Unknown method: {method}"}

    def run_stdio(self):
        """Run MCP server over stdio transport."""
        self._running = True
        for line in sys.stdin:
            if not self._running:
                break
            try:
                request = json.loads(line.strip())
                import asyncio
                response = asyncio.run(self.handle_request(request))
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except json.JSONDecodeError:
                continue
            except KeyboardInterrupt:
                break

    def stop(self):
        self._running = False
