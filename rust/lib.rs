use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (dry, d_time = 1, feedback = 1.))]
fn delay(dry: Vec<f32>, d_time: usize, feedback: f32) -> PyResult<Vec<f32>> {
    //TODO: implement delay tail
    let mut wet = vec![0f32; dry.len()];
    for i in 0..dry.len() {
        if d_time+i < dry.len() {
            wet[i+d_time] += (wet[i]+dry[i])*feedback;
        }   
    }

    Ok(wet)
}

#[pyfunction]
#[pyo3(signature = (dry, d_time, feedback))]
fn delay_m(dry: Vec<f32>, d_time: Vec<usize>, feedback: Vec<f32>) -> PyResult<Vec<f32>> {
    //TODO: implement delay tail
    let mut wet = vec![0f32; dry.len()];
    for i in 0..dry.len() {
        if d_time[i]+i < dry.len() {
            wet[d_time[i]+i] += (wet[i]+dry[i])*feedback[i];
        }   
    }

    Ok(wet)
}

//y(n) = ff1 * w(n) + ff2 * w(n - 1) + ff3 * w(n - 2) with w[n] = x[n] + fb1 * x[n - 1] + fb2 * x[n - 2]
fn w(dry: &[f64], i: usize, fb1: f64, fb2: f64) -> f64 {
    let (mut n1, mut n2) = (0.0, 0.0);
    let n0 = dry[i];
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

fn a_coef(break_freq: f32, hz: f32) -> f32 {
    use core::f32::consts::PI;
    let tan = (PI * break_freq / hz).tan();
    (tan - 1.) / (tan + 1.)
}

fn allpass_filter(input: Vec<f32>, break_freq: Vec<f32>, hz: f32) -> Vec<f32> {
    let mut dn_1 = 0.;
    let mut out = Vec::with_capacity(input.len());
    for i in 0..input.len() {
        let a1 = a_coef(break_freq[i], hz);
        let res = a1 * input[i] + dn_1;
        dn_1 = input[i] - a1 * res;
        out.push(res);
    }
    out
}
#[pyfunction]
#[pyo3(signature = (input, cutoff, hz, highpass=false, amplitude=1.0))]
fn filter(input: Vec<f32>, cutoff: Vec<f32>, hz: f32, highpass: bool, amplitude: f32) -> PyResult<Vec<f32>> {
    let allpass_out = allpass_filter(input, cutoff, hz);
    let mult = if highpass { -1. } else { 1. };
    let out = Vec::with_capacity(input.len());
    for i in 0..input.len() {
        let res = input[i] + allpass_out * mult;
        let res = res * 0.5 * amplitude;
        out.push(res);
    }
    Ok(out)
}
#[pymodule]
fn _lib(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(delay, m)?)?;
    m.add_function(wrap_pyfunction!(delay_m, m)?)?;
    m.add_function(wrap_pyfunction!(biquad, m)?)?;
    Ok(())
}
