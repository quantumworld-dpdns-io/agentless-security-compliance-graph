use pyo3::prelude::*;
use std::collections::{HashMap, VecDeque};

#[pyfunction]
pub fn traverse(adjacency: Vec<(String, String)>, start: String) -> PyResult<Vec<String>> {
    let mut graph: HashMap<String, Vec<String>> = HashMap::new();
    for (from, to) in &adjacency {
        graph.entry(from.clone()).or_default().push(to.clone());
        graph.entry(to.clone()).or_default().push(from.clone());
    }
    let mut visited = Vec::new();
    let mut queue = VecDeque::new();
    queue.push_back(start);
    while let Some(node) = queue.pop_front() {
        if !visited.contains(&node) {
            visited.push_back(node.clone());
            if let Some(neighbors) = graph.get(&node) {
                for n in neighbors {
                    queue.push_back(n.clone());
                }
            }
        }
    }
    Ok(visited)
}

#[pyfunction]
pub fn shortest_path(adjacency: Vec<(String, String)>, start: String, end: String) -> PyResult<Vec<String>> {
    let mut graph: HashMap<String, Vec<String>> = HashMap::new();
    for (from, to) in &adjacency {
        graph.entry(from.clone()).or_default().push(to.clone());
        graph.entry(to.clone()).or_default().push(from.clone());
    }
    let mut queue = VecDeque::new();
    let mut visited = HashMap::new();
    queue.push_back(start.clone());
    visited.insert(start, String::new());
    while let Some(node) = queue.pop_front() {
        if node == end {
            let mut path = Vec::new();
            let mut current = node;
            while !current.is_empty() {
                path.push(current.clone());
                current = visited.get(&current).cloned().unwrap_or_default();
            }
            path.reverse();
            return Ok(path);
        }
        if let Some(neighbors) = graph.get(&node) {
            for n in neighbors {
                if !visited.contains_key(n) {
                    visited.insert(n.clone(), node.clone());
                    queue.push_back(n.clone());
                }
            }
        }
    }
    Ok(vec![])
}
