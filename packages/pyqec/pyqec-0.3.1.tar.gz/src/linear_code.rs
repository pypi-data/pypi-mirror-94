use ldpc::{LinearCode, SparseBinMat, SparseBinSlice};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::PyObjectProtocol;
use rand::SeedableRng;
use rand_xoshiro::Xoshiro512StarStar;

/// An implementation of linear codes optimized for LDPC codes.
///
/// A code can be defined from either a parity check matrix `H`
/// or a generator matrix `G`.
/// These matrices have the property that `H G^T = 0`.
///
/// Example:
///     This example shows 2 way to define the Hamming code.
///
///     From a parity check matrix
///
///         code_from_checks = LinearCode.from_checks(
///             7,
///             [[0, 1, 2, 4], [0, 1, 3, 5], [0, 2, 3, 6]]
///         )
///
///     From a generator matrix
///
///         code_from_generators = LinearCode.from_generators(
///             7,
///             [[0, 4, 5, 6], [1, 4, 5], [2, 4, 6], [3, 5, 6]]
///         )
///
/// Comparison:
///     Use the `==` if you want to know if 2 codes
///     have exactly the same parity check matrix and
///     generator matrix.
///     However, since there is freedom in the choice of
///     parity check matrix and generator matrix for the same code,
///     use `has_same_codespace_as` method
///     if you want to know if 2 codes define the same codespace even
///     if they may have different parity check matrix or generator matrix.
///
///         >>> code_from_checks == code_from_generators
///         False
///         >>> code_from_checks.has_same_codespace_as(code_from_generators)
///         True
///
#[pyclass(name = LinearCode)]
pub struct PyLinearCode {
    pub(crate) inner: LinearCode,
}

impl From<LinearCode> for PyLinearCode {
    fn from(inner: LinearCode) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl PyLinearCode {
    /// Constructs a LinearCode from a parity check matrix.
    /// A parity check matrix `H` has the property that
    /// `Hx = 0` for all codeword x.
    ///
    /// Args:
    ///     block_size (int): The number of bits in the code.
    ///
    ///     checks (list of list of int): A list of checks where each check is
    ///         represented by the list of positions where this check has value 1.
    ///
    /// Returns:
    ///     LinearCode: The linear code with the given checks.
    ///
    /// Raises:
    ///     ValueError: If a check has a position greater
    ///         or equal to the block size.
    ///
    /// Example:
    ///     A 3 bits repetition code.
    ///
    ///         code = LinearCode.from_checks(3, [[0, 1], [1, 2]])
    #[staticmethod]
    #[text_signature = "(block_size, checks)"]
    pub fn from_checks(block_size: usize, checks: Vec<Vec<usize>>) -> PyResult<PyLinearCode> {
        let matrix = SparseBinMat::try_new(block_size, checks)
            .map_err(|error| PyValueError::new_err(error.to_string()))?;
        Ok(PyLinearCode {
            inner: LinearCode::from_parity_check_matrix(matrix),
        })
    }

    /// Constructs a LinearCode from a generator matrix.
    /// A generator matrix `G` has the property that
    /// for any codeword `x` we have `x = G^T y`
    /// where `y` is the unencoded bitstring.
    ///
    /// Args:
    ///     block_size (int): The number of bits in the code.
    ///
    ///     generators (list of list of int): A list of codeword generators
    ///         where each generator is represented by the
    ///         list of positions where this generator has value 1.
    ///
    /// Returns:
    ///     LinearCode: The linear code with the given codeword generators.
    ///
    /// Raises:
    ///     ValueError: If a generator has a position greater
    ///         or equal to the block size.
    ///
    /// Example:
    ///     A 3 bits repetition code.
    ///
    ///         code = LinearCode.from_generators(3, [[0, 1, 2]])
    #[staticmethod]
    #[text_signature = "(block_size, generators)"]
    pub fn from_generators(
        block_size: usize,
        generators: Vec<Vec<usize>>,
    ) -> PyResult<PyLinearCode> {
        let matrix = SparseBinMat::try_new(block_size, generators)
            .map_err(|error| PyValueError::new_err(error.to_string()))?;
        Ok(PyLinearCode {
            inner: LinearCode::from_generator_matrix(matrix),
        })
    }

    /// Samples a random regular codes.
    ///
    /// Parameters
    /// ----------
    /// block_size: int, default = 4
    ///     The number of bits in the code.
    /// number_of_checks: int, default = 3
    ///     The number of checks in the code.
    /// bit_degree: int, default = 3
    ///     The number of checks connected to each bit.
    /// check_degree: int, default = 4
    ///     The number of bits connected to each check.
    /// random_seed: int, optional
    ///     A seed to feed the random number generator.
    ///     By default, the rng is initialize from entropy.
    ///
    /// Returns
    /// -------
    /// LinearCode
    ///     A random linear code with the given parameters.
    ///
    /// Raises
    /// ------
    /// ValueError
    ///     If `block_size * bit_degree != number_of_checks * check_degree`.
    #[staticmethod]
    #[args(block_size = 4, number_of_checks = 3, bit_degree = 3, check_degree = 4)]
    #[text_signature = "(block_size, number_of_checks, bit_degree, check_degree, random_seed)"]
    pub fn random_regular_code(
        block_size: usize,
        number_of_checks: usize,
        bit_degree: usize,
        check_degree: usize,
        random_seed: Option<u64>,
    ) -> PyResult<Self> {
        let mut rng = if let Some(seed) = random_seed {
            Xoshiro512StarStar::seed_from_u64(seed)
        } else {
            Xoshiro512StarStar::from_entropy()
        };
        LinearCode::random_regular_code()
            .block_size(block_size)
            .number_of_checks(number_of_checks)
            .bit_degree(bit_degree)
            .check_degree(check_degree)
            .sample_with(&mut rng)
            .map(|code| code.into())
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    /// The number of bits in the code.
    #[text_signature = "(self)"]
    pub fn block_size(&self) -> usize {
        self.inner.block_size()
    }

    /// The number of encoded qubits.
    #[text_signature = "(self)"]
    pub fn dimension(&self) -> usize {
        self.inner.dimension()
    }

    /// The weight of the small non trivial codeword.
    ///
    /// Returns
    /// -------
    ///     The minimal distance of the code if
    ///     the dimension is at least 1 or -1
    ///     if the dimension is 0.
    ///
    /// Notes
    /// -----
    ///     This function execution time scale exponentially
    ///     with the dimension of the code.
    ///     Use at your own risk!
    #[text_signature = "(self)"]
    pub fn minimal_distance(&self) -> i64 {
        self.inner
            .minimal_distance()
            .map(|d| d as i64)
            .unwrap_or(-1)
    }

    /// The number of checks in the code.
    #[text_signature = "(self)"]
    pub fn number_of_checks(&self) -> usize {
        self.inner.number_of_checks()
    }

    /// The number of codeword generators in the code.
    #[text_signature = "(self)"]
    pub fn number_of_generators(&self) -> usize {
        self.inner.number_of_generators()
    }

    /// The parity check matrix of the code.
    #[text_signature = "(self)"]
    pub fn parity_check_matrix(&self) -> Vec<Vec<usize>> {
        self.inner
            .parity_check_matrix()
            .rows()
            .map(|row| row.as_slice().to_owned())
            .collect()
    }

    /// The generator matrix of the code.
    #[text_signature = "(self)"]
    pub fn generator_matrix(&self) -> Vec<Vec<usize>> {
        self.inner
            .generator_matrix()
            .rows()
            .map(|row| row.as_slice().to_owned())
            .collect()
    }

    /// The syndrome of a given message.
    ///
    /// Parameters
    /// ----------
    /// message: list of int
    ///     The positions with value 1 in the message.
    ///
    /// Returns
    /// -------
    /// list of int
    ///     The positions where `H y` is 1 where `H` is
    ///     the parity check matrix of the code and `y`
    ///     the input message.
    ///
    /// Raises
    /// ------
    /// ValueError
    ///     If a position in the message is greater or equal to the block size
    ///     of the code.
    #[text_signature = "(self, message)"]
    pub fn syndrome_of(&self, message: Vec<usize>) -> PyResult<Vec<usize>> {
        let vector = SparseBinSlice::try_new(self.inner.block_size(), &message)
            .map_err(|error| PyValueError::new_err(error.to_string()))?;
        Ok(self.inner.syndrome_of(&vector).to_positions_vec())
    }

    /// Checks if the given message is a codeword of the code.
    ///
    /// Parameters
    /// ----------
    /// message: list of int
    ///     The positions with value 1 in the message.
    ///
    /// Returns
    /// -------
    /// bool
    ///     True if the message has a zero syndrome and False otherwise.
    ///
    /// Raises
    /// ------
    /// ValueError
    ///     If a position in the message is greater or equal to the block size
    ///     of the code.
    #[text_signature = "(self, message)"]
    pub fn has_codeword(&self, message: Vec<usize>) -> PyResult<bool> {
        SparseBinSlice::try_new(self.inner.block_size(), &message)
            .map(|vector| self.inner.has_codeword(&vector))
            .map_err(|error| PyValueError::new_err(error.to_string()))
    }

    /// Checks if the other code defined the same codespace
    /// as this code.
    ///
    /// Parameters
    /// ----------
    /// other: LinearCode
    ///     The code to compare.
    ///
    /// Returns
    /// -------
    /// bool
    ///     True if other codewords are exactly the same
    ///     as this code codewords.
    #[text_signature = "(self, other)"]
    pub fn has_same_codespace_as(&self, other: &Self) -> bool {
        self.inner.has_same_codespace_as(&other.inner)
    }
}

#[pyproto]
impl PyObjectProtocol for PyLinearCode {
    fn __repr__(&self) -> String {
        format!(
            "Parity check matrix:\n{}\nGenerator matrix:\n{}",
            self.inner.parity_check_matrix(),
            self.inner.generator_matrix(),
        )
    }
}
