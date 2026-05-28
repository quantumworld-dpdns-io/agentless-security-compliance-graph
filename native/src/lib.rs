use pyo3::prelude::*;

mod graph;
mod duckdb_ext;

#[pymodule]
fn compliance_graph_native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(graph::traverse, m)?)?;
    m.add_function(wrap_pyfunction!(graph::shortest_path, m)?)?;
    m.add_function(wrap_pyfunction!(duckdb_ext::register_graph_functions, m)?)?;
    Ok(())
}
