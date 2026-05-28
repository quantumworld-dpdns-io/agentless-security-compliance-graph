import duckdb


class DuckDBGraphExtension:
    """Advanced DuckDB graph query extensions for compliance analysis."""

    def __init__(self, conn: duckdb.DuckDBPyConnection):
        self.conn = conn
        self._register_functions()

    def _register_functions(self):
        self.conn.create_function("graph_degree", self._graph_degree)
        self.conn.create_function("graph_neighbors", self._graph_neighbors)
        self.conn.create_function("is_reachable", self._is_reachable)

    def _graph_degree(self, node_id: str) -> int:
        result = self.conn.execute("""
            SELECT COUNT(*) FROM edges WHERE source_id = ? OR target_id = ?
        """, [node_id, node_id]).fetchone()
        return result[0] if result else 0

    def _graph_neighbors(self, node_id: str) -> list[str]:
        result = self.conn.execute("""
            SELECT DISTINCT CASE WHEN source_id = ? THEN target_id ELSE source_id END
            FROM edges WHERE source_id = ? OR target_id = ?
        """, [node_id, node_id, node_id]).fetchall()
        return [r[0] for r in result]

    def _is_reachable(self, from_id: str, to_id: str) -> bool:
        result = self.conn.execute("""
            WITH RECURSIVE reachable(node_id) AS (
                SELECT ? UNION
                SELECT CASE WHEN source_id = reachable.node_id THEN target_id ELSE source_id END
                FROM edges, reachable
                WHERE source_id = reachable.node_id OR target_id = reachable.node_id
            )
            SELECT COUNT(*) FROM reachable WHERE node_id = ?
        """, [from_id, to_id]).fetchone()
        return result[0] > 0 if result else False

    def create_materialized_compliance_view(self):
        self.conn.execute("""
            CREATE OR REPLACE VIEW compliance_summary_view AS
            SELECT
                n.node_type,
                COUNT(*) AS total,
                COUNT(CASE WHEN n.attributes->>'severity' = 'critical' THEN 1 END) AS critical,
                COUNT(CASE WHEN n.attributes->>'severity' = 'high' THEN 1 END) AS high
            FROM nodes n
            GROUP BY n.node_type
        """)

    def export_to_parquet(self, table_name: str, path: str):
        self.conn.execute(f"COPY {table_name} TO '{path}' (FORMAT PARQUET)")

    def import_from_parquet(self, path: str, table_name: str):
        self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet('{path}')")
