// rustimport:pyo3

use pyo3::prelude::*;

#[pyfunction]
fn say_hello() {
    println!("Hello from delay, implemented in Rust!")
}

#[pyfunction]
#[pyo3(signature = (dry, d_time = 1, feedback = 1.))]
fn del_line(dry: Vec<f64>, d_time: usize, feedback: f64) -> PyResult<Vec<f64>> {
    //implement delay tail
    let mut wet = vec![0f64; dry.len()];
    for i in 0..dry.len() {
        if d_time+i < dry.len() {
            wet[i+d_time] += (wet[i]+dry[i])*feedback;
        }   
    }

    Ok(wet)
}
// Uncomment the below to implement custom pyo3 binding code. Otherwise, 
// rustimport will generate it for you for all functions annotated with
// #[pyfunction] and all structs annotated with #[pyclass].
//
//#[pymodule]
//fn delay(_py: Python, m: &PyModule) -> PyResult<()> {
//    m.add_function(wrap_pyfunction!(say_hello, m)?)?;
//    m.add_function(wrap_pyfunction!(delay, m)?)?;
//    Ok(())
//}
