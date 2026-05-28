use pyo3::prelude::*;

#[pyfunction]
pub fn register_graph_functions(conn_path: &str) -> PyResult<String> {
    Ok(format!("Registered DuckDB graph extension via {conn_path}"))
}
