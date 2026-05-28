class MojoPerformanceKernel:
    def __init__(self):
        self._mojo_available = self._check_mojo()

    def _check_mojo(self) -> bool:
        try:
            import mojo
            return True
        except ImportError:
            return False

    def graph_traverse_accelerated(self, adjacency: list, start: str) -> list:
        return self._bfs_fallback(adjacency, start)

    def _bfs_fallback(self, adjacency: list, start: str) -> list:
        from collections import deque
        graph = {}
        for src, dst in adjacency:
            graph.setdefault(src, []).append(dst)
            graph.setdefault(dst, []).append(src)
        visited, queue = [], deque([start])
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.append(node)
                queue.extend(graph.get(node, []))
        return visited

    def benchmark(self, size: int = 1000) -> dict:
        import time
        adj = [(f"n{i}", f"n{i+1}") for i in range(size)]
        start = time.perf_counter()
        self.graph_traverse_accelerated(adj, "n0")
        elapsed = time.perf_counter() - start
        return {"nodes": size, "time_seconds": elapsed, "backend": "python_fallback"}
