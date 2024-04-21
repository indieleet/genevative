
use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (dry, d_time = 1, feedback = 1.))]
fn delay(dry: Vec<f64>, d_time: usize, feedback: f64) -> PyResult<Vec<f64>> {
    //implement delay tail
    let mut wet = vec![0f64; dry.len()];
    for i in 0..dry.len() {
        if d_time+i < dry.len() {
            wet[i+d_time] += (wet[i]+dry[i])*feedback;
        }   
    }

    Ok(wet)
}

//y(n) = ff1 * w(n) + ff2 * w(n - 1) + ff3 * w(n - 2) with w[n] = x[n] + fb1 * x[n - 1] + fb2 * x[n - 2]
fn w(dry: &Vec<f64>, i: usize, fb1: f64, fb2: f64) -> f64 {
    let (mut n0, mut n1, mut n2) = (0.0, 0.0, 0.0);
    n0 = dry[i];
    if i>0 {
        n1 = dry[i-1];
    }
    if i>1 {
        n2 = dry[i-2];
    }
    n0 + fb1*n1 + fb2*n2
}
#[pyfunction]
#[pyo3(signature = (dry, coef=(0.0, 0.0, 1.0, 1.0, 0.0)))]
fn biquad(dry: Vec<f64>, coef: (f64, f64, f64, f64, f64)) -> PyResult<Vec<f64>> {
    let (fb1, fb2, ff1, ff2, ff3) = coef;
    let mut wet = vec![0f64; dry.len()];
    let (mut i1, mut i2) = (0, 0) ;
    for i in 0..dry.len() {
        if i>0 {
            i1 = i-1;
        }
        if i>1 {
            i2 = i-2;
        }
        wet[i] = ff1 * w(&dry, i, fb1, fb2) + ff2 * w(&dry, i1, fb1, fb2) + ff3 * w(&dry, i2, fb1, fb2);
        
//y(n) = ff1 * w(n) + ff2 * w(n - 1) + ff3 * w(n - 2) with w[n] = x[n] + fb1 * x[n - 1] + fb2 * x[n - 2]
    }

    Ok(wet)
}


#[pymodule]
fn _lib(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(delay, m)?)?;
    m.add_function(wrap_pyfunction!(biquad, m)?)?;
    Ok(())
}
