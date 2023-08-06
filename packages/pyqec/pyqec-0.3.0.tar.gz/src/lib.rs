use pyo3::prelude::*;

mod linear_code;
use linear_code::PyLinearCode;

mod noise;
use noise::PyBinarySymmetricChannel;

mod flip_decoder;
use flip_decoder::PyFlipDecoder;

mod randomness;

/// A toolbox for classical (and soon quantum) error correction.
#[pymodule]
fn pyqec(_py: Python, module: &PyModule) -> PyResult<()> {
    module.add_class::<PyLinearCode>()?;
    module.add_class::<PyBinarySymmetricChannel>()?;
    module.add_class::<PyFlipDecoder>()?;
    Ok(())
}
