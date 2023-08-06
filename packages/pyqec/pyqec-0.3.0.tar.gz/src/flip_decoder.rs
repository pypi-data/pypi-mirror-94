use crate::PyLinearCode;
use ldpc::decoders::FlipDecoder;
use ldpc::{LinearCode, SparseBinVec};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass(name = FlipDecoder)]
pub struct PyFlipDecoder {
    pub(crate) inner: FlipDecoder<LinearCode>,
    block_size: usize,
}

#[pymethods]
impl PyFlipDecoder {
    #[new]
    pub fn new(code: &PyLinearCode) -> PyFlipDecoder {
        PyFlipDecoder {
            inner: FlipDecoder::new(code.inner.clone()),
            block_size: code.block_size(),
        }
    }

    pub fn decode(&self, message: Vec<usize>) -> PyResult<Vec<usize>> {
        SparseBinVec::try_new(self.block_size, message)
            .map(|message| self.inner.decode(&message).to_positions_vec())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }
}
