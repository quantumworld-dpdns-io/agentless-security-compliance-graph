from typing import Optional
import duckdb

class ComplianceGraph:
    def __init__(self, database_url: str = "compliance_graph.db"):
        self.conn = duckdb.connect(database_url)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE SEQUENCE IF NOT EXISTS node_seq START 1;
            CREATE TABLE IF NOT EXISTS nodes (
                id VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                node_type VARCHAR NOT NULL,
                attributes JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS edges (
                id VARCHAR PRIMARY KEY,
                source_id VARCHAR NOT NULL,
                target_id VARCHAR NOT NULL,
                edge_type VARCHAR NOT NULL,
                weight FLOAT DEFAULT 1.0,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES nodes(id),
                FOREIGN KEY (target_id) REFERENCES nodes(id)
            );
            CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
            CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);
            CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(edge_type);
        """)

    def add_node(self, node_type: str, name: str, attributes: Optional[dict] = None) -> str:
        import uuid
        node_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO nodes (id, name, node_type, attributes) VALUES (?, ?, ?, ?)",
            [node_id, name, node_type, attributes or {}]
        )
        return node_id

    def add_edge(self, source_id: str, target_id: str, edge_type: str, weight: float = 1.0, metadata: Optional[dict] = None) -> str:
        import uuid
        edge_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO edges (id, source_id, target_id, edge_type, weight, metadata) VALUES (?, ?, ?, ?, ?, ?)",
            [edge_id, source_id, target_id, edge_type, weight, metadata or {}]
        )
        return edge_id

    def bfs_traverse(self, start_node_id: str, max_depth: int = 10) -> list[dict]:
        return self.conn.execute("""
            WITH RECURSIVE graph_traversal AS (
                SELECT source_id AS node_id, 0 AS depth, CAST(source_id AS VARCHAR) AS path
                FROM edges WHERE source_id = ?
                UNION ALL
                SELECT e.target_id, gt.depth + 1, gt.path || '->' || e.target_id
                FROM edges e JOIN graph_traversal gt ON e.source_id = gt.node_id
                WHERE gt.depth < ?
            )
            SELECT DISTINCT n.id, n.name, n.node_type, n.attributes
            FROM graph_traversal gt JOIN nodes n ON gt.node_id = n.id
        """, [start_node_id, max_depth]).fetchall()

    def shortest_path(self, from_id: str, to_id: str) -> list[str]:
        result = self.conn.execute("""
            WITH RECURSIVE path_finding AS (
                SELECT source_id, target_id, CAST(source_id AS VARCHAR) || '->' || target_id AS path, 1 AS depth
                FROM edges WHERE source_id = ?
                UNION ALL
                SELECT e.source_id, e.target_id, pf.path || '->' || e.target_id, pf.depth + 1
                FROM edges e JOIN path_finding pf ON e.source_id = pf.target_id
                WHERE pf.depth < 20 AND pf.target_id != ?
            )
            SELECT path, depth FROM path_finding
            WHERE target_id = ? ORDER BY depth LIMIT 1
        """, [from_id, to_id, to_id]).fetchone()
        return result[0].split("->") if result else []

    def find_privilege_escalation_paths(self) -> list[dict]:
        return self.conn.execute("""
            SELECT e1.source_id AS start_node, e2.target_id AS end_node,
                   e1.source_id || '->' || e1.target_id || '->' || e2.target_id AS path
            FROM edges e1 JOIN edges e2 ON e1.target_id = e2.source_id
            WHERE e1.edge_type = 'MEMBER_OF' AND e2.edge_type = 'HAS_ADMIN_RIGHTS'
        """).fetchall()

    def get_compliance_summary(self) -> dict:
        total = self.conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        by_type = self.conn.execute(
            "SELECT node_type, COUNT(*) FROM nodes GROUP BY node_type"
        ).fetchall()
        edges_count = self.conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        return {"total_nodes": total, "nodes_by_type": dict(by_type), "total_edges": edges_count}

    def close(self):
        self.conn.close()
