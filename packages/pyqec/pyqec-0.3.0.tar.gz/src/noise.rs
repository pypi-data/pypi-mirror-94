use crate::randomness::{get_rng_with_seed, RandomNumberGenerator};
use ldpc::noise_model::{BinarySymmetricChannel, NoiseModel, Probability};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::PyObjectProtocol;

/// An implementation of a binary symmetric channel.
///
/// A binary symmetric channel flips the value
/// of each bits according to a given error probability.
#[pyclass(name = BinarySymmetricChannel)]
pub struct PyBinarySymmetricChannel {
    channel: BinarySymmetricChannel,
    probability: f64,
    rng: RandomNumberGenerator,
}

#[pymethods]
impl PyBinarySymmetricChannel {
    #[new]
    pub fn new(probability: f64, rng_seed: Option<u64>) -> PyResult<PyBinarySymmetricChannel> {
        let prob_wrapper = Probability::try_new(probability).ok_or(PyValueError::new_err(
            format!("{} is not a valid probability", probability,),
        ))?;
        let channel = BinarySymmetricChannel::with_probability(prob_wrapper);
        let rng = get_rng_with_seed(rng_seed);
        Ok(PyBinarySymmetricChannel {
            channel,
            probability,
            rng,
        })
    }

    #[text_signature = "(self, length)"]
    fn sample_error_of_length(&mut self, length: usize) -> Vec<usize> {
        self.channel
            .sample_error_of_length(length, &mut self.rng)
            .to_positions_vec()
    }

    #[text_signature = "(self)"]
    fn error_probability(&self) -> f64 {
        self.probability
    }
}

#[pyproto]
impl PyObjectProtocol for PyBinarySymmetricChannel {
    fn __repr__(&self) -> String {
        format!("BSC({})", self.error_probability())
    }
}
