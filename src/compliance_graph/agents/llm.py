from typing import Optional, Literal

class LLMProvider:
    """Abstract LLM provider interface."""

    def __init__(self, provider: Literal["openai", "anthropic", "ollama", "vllm"] = "ollama"):
        self.provider = provider
        self.client = self._init_client()

    def _init_client(self):
        if self.provider == "openai":
            from openai import OpenAI
            return OpenAI()
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic()
        elif self.provider == "ollama":
            import httpx
            return httpx.Client(base_url="http://localhost:11434")
        elif self.provider == "vllm":
            from openai import OpenAI
            return OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")
        return None

    def chat(self, messages: list[dict], model: Optional[str] = None) -> str:
        if self.provider in ("openai", "vllm"):
            response = self.client.chat.completions.create(model=model or "gpt-4", messages=messages)
            return response.choices[0].message.content
        elif self.provider == "anthropic":
            response = self.client.messages.create(model=model or "claude-3-opus-20240229", max_tokens=1024, messages=messages)
            return response.content[0].text
        elif self.provider == "ollama":
            response = self.client.post("/api/chat", json={"model": model or "llama3", "messages": messages, "stream": False})
            return response.json()["message"]["content"]
        return "LLM provider not configured"

    def analyze_compliance(self, graph_summary: dict) -> str:
        prompt = f"""Analyze this compliance graph summary:

Total Nodes: {graph_summary.get('total_nodes', 0)}
Nodes by Type: {graph_summary.get('nodes_by_type', {})}
Total Edges: {graph_summary.get('total_edges', 0)}

Provide a concise security compliance analysis with top 3 recommendations."""
        return self.chat([{"role": "user", "content": prompt}], model="gpt-4")
