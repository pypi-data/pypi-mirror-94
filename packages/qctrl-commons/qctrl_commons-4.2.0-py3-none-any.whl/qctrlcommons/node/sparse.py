# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""Module for sparse."""
from typing import (
    List,
    Optional,
    Union,
)

import forge
import numpy as np
from scipy.sparse import (
    coo_matrix,
    issparse,
)

from qctrlcommons.node import types
from qctrlcommons.node.module import CoreNode
from qctrlcommons.node.node_data import SparsePwcNodeData
from qctrlcommons.node.tensorflow import TensorNodeData
from qctrlcommons.node.utils import (
    validate_hamiltonian,
    validate_shape,
)
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_hermitian,
    check_argument_integer,
    check_argument_numeric,
    check_duration,
    check_operator,
    check_sample_times,
)


class SparsePwcOperator(CoreNode):
    r"""
    Creates a sparse piecewise-constant operator (sparse-matrix-valued function of time).

    Each of the piecewise-constant segments (time periods) is a scalar multiple
    of the operator.

    Parameters
    ----------
    signal : TensorPwc
        The scalar-valued piecewise-constant function of time :math:`a(t)`.
    operator : scipy.sparse.coo_matrix
        The sparse operator :math:`A` to be scaled over time.

    Returns
    -------
    SparsePwc
        The piecewise-constant sparse operator :math:`a(t)A`.

    See Also
    --------
    constant_sparse_pwc_operator : A function to create constant `SparsePwc`s.
    sparse_pwc_sum : A function to calculate the sum of multiple `SparsePwc`s.
    """

    name = "sparse_pwc_operator"
    _module_attr = "create_sparse_pwc_operator"
    args = [
        forge.arg("signal", type=types.TensorPwc),
        forge.arg("operator", type=coo_matrix),
    ]
    kwargs = {}  # SparsePwc doesn't accept `name` as an argument.
    rtype = types.SparsePwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        signal = kwargs.get("signal")
        operator = kwargs.get("operator")
        signal_shape = signal.values_shape
        check_argument(
            signal_shape == (),
            "The signal must be scalar-valued.",
            {"signal": signal},
            {"signal.values_shape": signal_shape},
        )
        batch_shape = signal.batch_shape
        check_argument(
            batch_shape == (),
            "Batching is not supported for sparse_pwc.",
            {"signal": signal},
            {"signal.batch_shape": batch_shape},
        )
        operator_shape = validate_shape(operator, "operator")
        check_argument(
            len(operator_shape) == 2 and operator_shape[0] == operator_shape[1],
            "Operator must be a 2D square matrix.",
            {"operator": operator},
            {"operator.shape": operator_shape},
        )
        return SparsePwcNodeData(_operation, values_shape=operator_shape)


class ConstantSparsePwcOperator(CoreNode):
    r"""
    Creates a constant sparse piecewise-constant operator over a specified duration.

    Parameters
    ----------
    duration : float
        The duration :math:`\tau` for the resulting piecewise-constant operator.
    operator : scipy.sparse.coo_matrix
        The sparse operator :math:`A`.

    Returns
    -------
    SparsePwc
        The constant operator :math:`t\mapsto A` (for :math:`0\leq t\leq\tau`).

    See Also
    --------
    sparse_pwc_operator : A function to create time-dependent sparse piecewise-constant operators.
    sparse_pwc_sum : A function to calculate the sum of multiple `SparsePwc`s.
    """

    name = "constant_sparse_pwc_operator"
    _module_attr = "create_constant_sparse_pwc_operator"
    args = [forge.arg("duration", type=float), forge.arg("operator", type=coo_matrix)]
    kwargs = {}  # SparsePwc doesn't accept `name` as an argument.
    rtype = types.SparsePwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        duration = kwargs.get("duration")
        operator = kwargs.get("operator")
        check_duration(duration, "duration")
        operator_shape = validate_shape(operator, "operator")
        check_argument(
            len(operator_shape) == 2 and operator_shape[0] == operator_shape[1],
            "Operator must be a 2D square matrix.",
            {"operator": operator},
            {"operator.shape": operator_shape},
        )
        return SparsePwcNodeData(_operation, values_shape=operator_shape)


class SparsePwcSum(CoreNode):
    r"""
    Creates the sum of multiple sparse-matrix-valued piecewise-constant functions.

    Parameters
    ----------
    terms : list[SparsePwc]
        The individual piecewise-constant terms :math:`\{v_j(t)\}` to sum.
        All terms must be sparse, have values of the same shape,
        and have the same total duration
        but may have different numbers of segments of different durations.

    Returns
    -------
    SparsePwc
        The piecewise-constant function of time :math:`\sum_j v_j(t)`. It
        has the same shape as each of the `terms` that you provided.
    """

    name = "sparse_pwc_sum"
    _module_attr = "get_sparse_pwc_sum"
    args = [forge.arg("terms", type=List[types.SparsePwc])]
    kwargs = {}  # SparsePwcSum doesn't accept `name` as an argument.
    rtype = types.SparsePwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        terms = kwargs.get("terms")
        shape_0 = terms[0].values_shape
        for i in range(1, len(terms)):
            shape = terms[i].values_shape
            check_argument(
                shape == shape_0,
                "All the terms must have the same shape.",
                {"terms": terms},
                {
                    f"terms[{0}].values_shape": shape_0,
                    f"terms[{i}].values_shape": shape,
                },
            )
        return SparsePwcNodeData(_operation, values_shape=shape_0)


class StateEvolutionPwc(CoreNode):
    r"""
    Calculates the time evolution of a state generated by a piecewise-constant
    Hamiltonian by using the Lanczos method.

    Parameters
    ----------
    initial_state : Union[Tensor, np.ndarray]
        The initial state as a Tensor or np.ndarray of shape ``[D]``.
    hamiltonian : SparsePwc
        The control Hamiltonian.
    krylov_subspace_dimension : Union[Tensor, int]
        The dimension of the Krylov subspace `k` for the Lanczos method.
    sample_times :  np.ndarray(1D, real), optional
        The N times at which you want to sample the state. Elements must be non-negative
        and strictly increasing, with a supremum that is the duration of the `hamiltonian`.
        If omitted only the evolved state at the final time of the control Hamiltonian
        is returned.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        Tensor of shape ``[N, D]`` or ``[D]`` if `sample_times` is omitted
        representing the state evolution. The n-th element (along the first
        dimension) represents the state at ``sample_times[n]`` evolved from
        the initial state.

    Notes
    -----
    The Lanczos algorithm calculates the unitary evolution of a state in the Krylov
    subspace. This subspace is spanned by the states resulting from applying the first
    `k` powers of the Hamiltonian on the input state, with `k` being the subspace dimension,
    much smaller that the full Hilbert space dimension. This allows for an efficient
    state propagation in high-dimensional systems compared to calculating the full
    unitary operator.
    """

    name = "state_evolution_pwc"
    _module_attr = "propagate_state_lanczos"
    args = [
        forge.arg("initial_state", type=Union[types.Tensor, np.ndarray]),
        forge.arg("hamiltonian", type=types.SparsePwc),
        forge.arg("krylov_subspace_dimension", type=Union[int, types.Tensor]),
        forge.arg("sample_times", type=Optional[np.ndarray], default=None),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        initial_state = kwargs.get("initial_state")
        hamiltonian = kwargs.get("hamiltonian")
        sample_times = kwargs.get("sample_times")
        check_argument_numeric(initial_state, "initial_state")
        if sample_times is not None:
            check_sample_times(sample_times, "sample_times")
        check_argument(
            isinstance(hamiltonian, SparsePwcNodeData),
            "The Hamiltonian must be a SparsePwc.",
            {"hamiltonian": hamiltonian},
        )
        values_shape_state = validate_shape(initial_state, "initial_state")
        values_shape_hamiltonian = hamiltonian.values_shape
        validate_hamiltonian(hamiltonian, "hamiltonian")
        check_argument(
            values_shape_state[0] == values_shape_hamiltonian[-1],
            "The Hilbert space dimensions of the state and the Hamiltonian must be equal.",
            {"initial_state": initial_state, "hamiltonian": hamiltonian},
            extras={
                "initial_state.shape": values_shape_state,
                "hamiltonian.values_shape": values_shape_hamiltonian,
            },
        )
        if sample_times is None:
            shape = values_shape_state
        else:
            shape = (len(sample_times),) + values_shape_state
        return TensorNodeData(_operation, shape=shape)


class EstimatedKrylovSubspaceDimension(CoreNode):
    """
    Estimates the dimension of the Krylov subspace to be used in the Lanczos integrator for
    a given bound on the total error in the integration.

    You can use this function to find a proper dimension of the Krylov subspace for state
    propagation using the Lanczos algorithm. Note that you can provide your own estimation
    of the Hamiltonian spectral range or use the `spectral_range` operation to
    perform that calculation.

    Parameters
    ----------
    spectral_range : Union[Tensor, float]
        Estimated order of magnitude of Hamiltonian spectral range (difference
        between largest and smallest eigenvalues).
    duration : float
        The total evolution time.
    maximum_segment_duration : float
        The maximum duration of the piecewise-constant Hamiltonian segments.
    error_tolerance : float, optional
        Tolerance for the error in the integration, defined as the Frobenius norm of
        the vectorial difference between the exact state and the estimated state.
        Defaults to 1e-6.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        Estimated dimension of the Krylov subspace for integration.

    See Also
    --------
    spectral_range, state_evolution_pwc
    """

    name = "estimated_krylov_subspace_dimension"
    _module_attr = "recommend_lanczos_k"
    args = [
        forge.arg("spectral_range", type=Union[types.Tensor, float]),
        forge.arg("duration", type=float),
        forge.arg("maximum_segment_duration", type=float),
        forge.arg("error_tolerance", type=float, default=1e-6,),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        duration = kwargs.get("duration")
        maximum_segment_duration = kwargs.get("maximum_segment_duration")
        error_tolerance = kwargs.get("error_tolerance")
        check_argument(
            maximum_segment_duration > 0,
            "The maximum segment duration must be positive.",
            {"maximum_segment_duration": maximum_segment_duration},
        )
        check_argument(
            duration > 0, "The duration must be positive.", {"duration": duration},
        )
        check_argument(
            maximum_segment_duration <= duration,
            "The maximum segment duration must be less than or equal to duration.",
            {
                "maximum_segment_duration": maximum_segment_duration,
                "duration": duration,
            },
        )
        check_argument(
            error_tolerance > 0,
            "The error tolerance must be positive.",
            {"error_tolerance": error_tolerance,},
        )

        return TensorNodeData(_operation, shape=())


class SpectralRange(CoreNode):
    r"""
    Obtains the range of the eigenvalues of a Hermitian operator.

    This function provides an estimate of the difference between the
    highest and the lowest eigenvalues of the operator. You can adjust its
    precision by modifying its default parameters.

    Parameters
    ----------
    operator : np.ndarray or scipy.sparse.coo_matrix or Tensor
        The Hermitian operator :math:`M` whose range of eigenvalues you
        want to determine.
    iteration_count : int, optional
        The number of iterations :math:`N` in the calculation. Defaults to
        3000. Choose a higher number to improve the precision, or a smaller
        number to make the estimation run faster.
    seed : int, optional
        The random seed that the function uses to choose the initial random
        vector :math:`\left| r \right\rangle`. Defaults to ``None``, which
        means that the function uses a different seed in each run.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor (scalar, real)
        The difference between the largest and the smallest eigenvalues of
        the operator.

    Warnings
    --------
    This calculation can be expensive, so we recommend that you run it
    before the optimization, if possible. You can do this by using a
    representative or a worst-case operator.

    Notes
    -----
    This function repeatedly multiplies the operator :math:`M` with a
    random vector :math:`\left| r \right\rangle`. In terms of the operator's
    eigenvalues :math:`\{ v_i \}` and eigenvectors
    :math:`\{\left|v_i \right\rangle\}`, the result of :math:`N` matrix
    multiplications is:

    .. math::
        M^N \left|r\right\rangle = \sum_i v_i^N \left|v_i\right\rangle
        \left\langle v_i \right. \left| r \right\rangle.

    For large :math:`N`, the term corresponding to the eigenvalue with
    largest absolute value :math:`V` will dominate the sum, as long as
    :math:`\left|r\right\rangle` has a non-zero overlap with its
    eigenvector. The function then retrieves the eigenvalue :math:`V` via:

    .. math::
        V \approx \frac{\left\langle r \right| M^{2N+1} \left| r
        \right\rangle}{\left\| M^N \left| r \right\rangle \right\|^2}.

    The same procedure applied to the matrix :math:`M-V` allows the function
    to find the eigenvalue at the opposite end of the spectral range.
    """

    name = "spectral_range"
    _module_attr = "calculate_spectral_range"
    args = [
        forge.arg("operator", type=Union[types.Tensor, np.ndarray, coo_matrix]),
        forge.arg("iteration_count", type=int, default=3000),
        forge.arg("seed", type=Optional[int], default=None),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        operator = kwargs.get("operator")
        iteration_count = kwargs.get("iteration_count")
        check_operator(operator, "operator")
        operator_shape = validate_shape(operator, "operator")
        check_argument(
            len(operator_shape) == 2,
            "Batches of operators are not supported.",
            {"operator": operator},
            extras={"operator.shape": operator_shape},
        )
        check_argument_integer(iteration_count, "iteration_count")
        check_argument(
            iteration_count > 0,
            "The number of iterations must be greater than zero.",
            {"iteration_count": iteration_count},
        )
        if not isinstance(operator, TensorNodeData):
            if issparse(operator):
                check_argument_hermitian(operator.toarray(), "operator")
            else:
                check_argument_hermitian(operator, "operator")
        return TensorNodeData(_operation, shape=())
