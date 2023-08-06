use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::class::number::PyNumberProtocol;


#[pyclass]
#[derive(Clone)]
pub struct Failure {
    #[pyo3(get)]
    message: String,
    #[pyo3(get)]
    position: usize
}


#[pyclass]
#[derive(Clone)]
pub struct Result {
    value: Option<PyObject>,
    failures: Vec<Failure>
}

#[pymethods]
impl Result {
    pub fn is_failure(&self) -> bool {
	self.failures.len() > 0
    }

    pub fn map_value(&self, py: Python, mapping: PyObject) -> PyResult<Self> {
	match &self.value {
	    Some(old_value) => {
		let mut other = self.clone();
		other.value = mapping.call1(py, (old_value,)).ok();
		Ok(other)
	    },
	    None => Ok(self.clone())
	}
    }

    #[getter]
    pub fn value(&self, py: Python) -> PyResult<PyObject> {
	match &self.value {
	    Some(value) => Ok(value.clone()),
	    None => Ok(py.None())
	}
    }

    pub fn get_failures(&self, py: Python) -> PyResult<Vec<Failure>> {
	Ok(self.failures.iter().cloned().collect())
    }
}

#[pyproto]
impl<'e> PyNumberProtocol<'e> for Result {
    fn __add__(lhs: Result, rhs: Result) -> Result {
	if lhs.is_failure() {
	    if rhs.is_failure() {
		let mut failures = Vec::new();
		failures.append(&mut lhs.failures.iter().cloned().collect());
		failures.append(&mut rhs.failures.iter().cloned().collect());
		Result {
		    value: None,
		    failures,
		}
	    } else {
		rhs
	    }
	} else {
	    lhs
	}
    }
}

#[pyfunction]
fn success<'p>(python: Python<'p>, value: PyObject) -> Result {
    Result {value: Some(value), failures: vec!()}
}

#[pyfunction]
fn failure<'p>(python: Python<'p>, message: String, position: usize) -> Result {
    Result {value: None, failures: vec!(Failure { message, position })}
}


#[pymodule]
fn result(_py: Python<'_>, module: &PyModule) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(success, module)?)?;
    module.add_function(wrap_pyfunction!(failure, module)?)?;
    module.add_class::<Failure>()?;
    module.add_class::<Result>()?;
    Ok(())
}
