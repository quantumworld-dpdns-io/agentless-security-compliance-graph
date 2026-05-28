
class DataFusionBackend:
    """Apache DataFusion as alternative query engine."""

    def __init__(self):
        self._datafusion_available = self._check_datafusion()

    def _check_datafusion(self) -> bool:
        try:
            import datafusion
            return True
        except ImportError:
            return False

    def query(self, sql: str) -> list[dict]:
        if not self._datafusion_available:
            return [{"error": "DataFusion not available"}]
        import datafusion
        ctx = datafusion.SessionContext()
        return ctx.sql(sql).to_pylist()

    def register_duckdb_table(self, duckdb_conn, table_name: str):
        if not self._datafusion_available:
            return
        import datafusion
        ctx = datafusion.SessionContext()
        records = duckdb_conn.execute(f"SELECT * FROM {table_name}").fetchdf()
        from datafusion import DataFrame
        ctx.register_dataframe(table_name, DataFrame.from_pandas(records))
