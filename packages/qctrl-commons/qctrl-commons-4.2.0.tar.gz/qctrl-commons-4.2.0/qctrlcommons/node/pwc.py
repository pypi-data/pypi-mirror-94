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
"""Module for all the node related to PWC."""
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

import forge
import numpy as np

from qctrlcommons.node import types
from qctrlcommons.node.module import CoreNode
from qctrlcommons.node.node_data import TensorPwcNodeData
from qctrlcommons.node.tensorflow import TensorNodeData
from qctrlcommons.node.utils import (
    validate_hamiltonian,
    validate_shape,
    validate_values_and_batch_shape,
)
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_integer,
    check_argument_iteratable,
    check_argument_numeric,
    check_duration,
    check_sample_times,
)


class TensorPwc(CoreNode):
    r"""
    Creates a piecewise-constant function of time.

    Parameters
    ----------
    durations : np.ndarray (1D, real)
        The durations :math:`\{\delta t_n\}` of the :math:`N` constant
        segments.
    values : np.ndarray or Tensor
        The values :math:`\{v_n\}` of the function on the constant segments.
        The dimension corresponding to `time_dimension` must be the same
        length as `durations`. To create a batch of
        :math:`B_1 \times \ldots \times B_n` piecewise-constant tensors of
        shape :math:`D_1 \times \ldots \times D_m`, provide this `values`
        parameter as an object of shape
        :math:`B_1\times\ldots\times B_n\times N\times D_1\times\ldots\times D_m`.
    time_dimension : int, optional
        The axis along `values` corresponding to time. All dimensions that
        come before the `time_dimension` are batch dimensions: if there are
        :math:`n` batch dimensions, then `time_dimension` is also :math:`n`.
        Defaults to 0, which corresponds to no batch. Note that you can
        pass a negative value to refer to the time dimension.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc
        The piecewise-constant function of time :math:`v(t)`, satisfying
        :math:`v(t)=v_n` for :math:`t_{n-1}\leq t\leq t_n`, where
        :math:`t_0=0` and :math:`t_n=t_{n-1}+\delta t_n`. If you provide a
        batch of values, the returned `TensorPwc` represents a
        corresponding batch of :math:`B_1 \times \ldots \times B_n`
        functions :math:`v(t)`, each of shape
        :math:`D_1 \times \ldots \times D_m`.

    """

    name = "tensor_pwc"
    _module_attr = "TensorPwc"
    args = [
        forge.arg("durations", type=np.ndarray),
        forge.arg("values", type=Union[np.ndarray, types.Tensor]),
        forge.arg("time_dimension", type=int, default=0),
    ]

    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        durations = kwargs.get("durations")
        values = kwargs.get("values")
        time_dimension = kwargs.get("time_dimension")
        check_argument_numeric(durations, "durations")
        check_argument_numeric(values, "values")
        check_argument_integer(time_dimension, "time_dimension")
        values_shape = validate_shape(values, "values")
        durations_shape = validate_shape(durations, "durations")
        check_argument(
            len(durations_shape) == 1,
            "The shape of durations must have exactly one dimension.",
            {"durations": durations},
        )
        check_argument(
            values_shape[time_dimension] == durations_shape[0],
            "The size of the `time_dimension` of `values` must be equal to the length"
            " of `durations`.",
            {"values": values, "durations": durations},
        )
        for index, duration in enumerate(durations):
            check_duration(duration, f"durations[{index}]")
        return TensorPwcNodeData(
            _operation,
            values_shape=values_shape[time_dimension + 1 :],
            durations=durations,
            batch_shape=values_shape[:time_dimension],
        )


class PwcSignal(CoreNode):
    r"""
    Creates a piecewise-constant signal (scalar-valued function of time).

    Use this function to create a piecewise-constant signal in which the
    constant segments all have the same duration.

    Parameters
    ----------
    values : np.ndarray or Tensor
        The values :math:`\{\alpha_n\}` of the :math:`N` constant segments.
        These can represent either a single sequence of segment values or a
        batch of them. To create a batch of
        :math:`B_1 \times \ldots \times B_n` signals, represent these
        `values` as a tensor of shape
        :math:`B_1 \times \ldots \times B_n \times N`.
    duration : float
        The total duration :math:`\tau` of the signal.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc
        The piecewise-constant function of time :math:`\alpha(t)`, satisfying
        :math:`\alpha(t)=\alpha_n` for :math:`t_{n-1}\leq t\leq t_n`, where
        :math:`t_n=n\tau/N` (where :math:`N` is the number of values
        in :math:`\{\alpha_n\}`). If you provide a batch of values, the
        returned `TensorPwc` represents a corresponding batch of
        :math:`B_1 \times \ldots \times B_n` functions :math:`\alpha(t)`.

    See Also
    --------
    tensor_pwc : Corresponding function with support for segments of different
        durations.
    """

    name = "pwc_signal"
    _module_attr = "create_pwc_signal"
    args = [
        forge.arg("values", type=Union[np.ndarray, types.Tensor]),
        forge.arg("duration", type=float),
    ]
    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        values = kwargs.get("values")
        duration = kwargs.get("duration")
        check_argument_numeric(values, "values")
        check_duration(duration, "duration")
        shape = validate_shape(values, "values")
        check_argument(
            len(shape) > 0,
            "The shape of values must have at least one dimension.",
            {"values": values},
        )
        durations = duration / shape[-1] * np.ones(shape[-1])
        return TensorPwcNodeData(
            _operation, values_shape=(), durations=durations, batch_shape=shape[:-1],
        )


class ComplexPwcSignal(CoreNode):
    r"""
    Creates a complex piecewise-constant signal from moduli and phases.

    Use this function to create a complex piecewise-constant signal from
    moduli and phases defined for each segment, in which the constant segments
    all have the same duration.

    Parameters
    ----------
    moduli : np.ndarray(real) or Tensor(real)
        The moduli :math:`\{\Omega_n\}` of the values of :math:`N` constant
        segments. These can represent either the moduli of a single
        sequence of segment values or of a batch of them. To provide a
        batch of sequences of segment values of shape
        :math:`B_1 \times \ldots \times B_n`, represent these moduli as a
        tensor of shape :math:`B_1 \times \ldots \times B_n \times N`.
    phases : np.ndarray(real) or Tensor(real)
        The phases :math:`\{\phi_n\}` of the complex segment values. Must
        have the same length as `moduli` (or same shape, if you're
        providing a batch).
    duration : float
        The total duration :math:`\tau` of the signal.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc(complex)
        The piecewise-constant function of time :math:`v(t)`, satisfying
        :math:`v(t)=\Omega_n e^{i\phi_n}` for :math:`t_{n-1}\leq t\leq t_n`,
        where :math:`t_n=n\tau/N` (where :math:`N` is the number of
        values in :math:`\{\Omega_n\}` and :math:`\{\phi_n\}`). If you
        provide a batch of `moduli` and `phases`, the returned `TensorPwc`
        represents a corresponding batch of
        :math:`B_1 \times \ldots \times B_n` functions :math:`v(t)`.

    See Also
    --------
    pwc_signal : Corresponding function for creating signals from
        (possibly-complex) values.
    """

    name = "complex_pwc_signal"
    _module_attr = "create_complex_pwc_signal"
    args = [
        forge.arg("moduli", type=Union[np.ndarray, types.Tensor]),
        forge.arg("phases", type=Union[np.ndarray, types.Tensor]),
        forge.arg("duration", type=float),
    ]
    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        moduli = kwargs.get("moduli")
        phases = kwargs.get("phases")
        duration = kwargs.get("duration")
        check_argument_numeric(moduli, "moduli")
        check_argument_numeric(phases, "phases")
        check_duration(duration, "duration")
        moduli_shape = validate_shape(moduli, "moduli")
        phases_shape = validate_shape(phases, "phases")
        check_argument(
            len(moduli_shape) > 0,
            "The shape of moduli must have at least one dimension.",
            {"moduli": moduli},
        )
        check_argument(
            moduli_shape == phases_shape,
            "The shape of moduli and phases must be equal.",
            {"moduli": moduli, "phases": phases},
        )
        durations = duration / moduli_shape[-1] * np.ones(moduli_shape[-1])
        return TensorPwcNodeData(
            _operation,
            values_shape=(),
            durations=durations,
            batch_shape=moduli_shape[:-1],
        )


class PwcOperatorHermitianPart(CoreNode):
    r"""
    Creates the Hermitian part of a piecewise-constant operator.

    Parameters
    ----------
    operator : TensorPwc(3D)
        The operator :math:`A(t)`.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc(3D)
        The Hermitian part :math:`\frac{1}{2}(A(t)+A^\dagger(t))`.
    """

    name = "pwc_operator_hermitian_part"
    _module_attr = "get_pwc_operator_hermitian_part"
    args = [
        forge.arg("operator", type=types.TensorPwc),
    ]
    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        operator = kwargs.get("operator")
        check_argument(
            isinstance(operator, TensorPwcNodeData),
            "The operator must be a TensorPwc.",
            {"operator": operator},
        )
        values_shape, batch_shape = validate_values_and_batch_shape(
            operator, "operator",
        )
        return TensorPwcNodeData(
            _operation,
            values_shape=values_shape,
            durations=operator.durations,
            batch_shape=batch_shape,
        )


class PwcSum(CoreNode):
    r"""
    Creates the sum of multiple piecewise-constant terms.

    Parameters
    ----------
    terms : list[TensorPwc]
        The individual piecewise-constant terms :math:`\{v_j(t)\}` to sum. All
        terms must have the same duration and values of the same shape, but
        may have different segmentations (different numbers of segments of
        different durations).
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc
        The piecewise-constant function of time :math:`\sum_j v_j(t)`. It
        has the same shape as each of the `terms` that you provided.
    """

    name = "pwc_sum"
    _module_attr = "get_pwc_sum"
    args = [forge.arg("terms", type=List[types.TensorPwc])]
    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        terms = kwargs.get("terms")
        check_argument_iteratable(terms, "terms")
        check_argument(
            all([isinstance(term, TensorPwcNodeData) for term in terms]),
            "Each of the terms must be a TensorPwc.",
            {"terms": terms},
        )
        values_shape, batch_shape = validate_values_and_batch_shape(
            terms[0], "terms[0]",
        )
        check_argument(
            all(
                [
                    (
                        (term.values_shape == values_shape)
                        and (term.batch_shape == batch_shape)
                    )
                    for term in terms[1:]
                ]
            ),
            "All the terms must have the same shape.",
            {"terms": terms},
        )
        check_argument(
            all(
                [
                    np.allclose(np.sum(terms[0].durations), np.sum(term.durations))
                    for term in terms
                ]
            ),
            "All the terms must have the same total duration.",
            {"terms": terms},
            extras={
                "total duration of each term": [
                    np.sum(term.durations) for term in terms
                ]
            },
        )
        upsampled_durations = np.diff(
            np.insert(
                np.unique(
                    np.concatenate([np.cumsum(term.durations) for term in terms])
                ),
                0,
                0,
            )
        )
        return TensorPwcNodeData(
            _operation,
            values_shape=values_shape,
            durations=upsampled_durations,
            batch_shape=batch_shape,
        )


class RealFourierPwcSignal(CoreNode):
    r"""
    Creates a piecewise-constant signal constructed from Fourier components.

    Use this function to create a signal defined in terms of Fourier
    (sine/cosine) basis signals that can be optimized by varying their
    coefficients and, optionally, their frequencies.

    This function supports three different modes: fixed frequencies (you
    directly provide the frequencies for the basis signals), optimizable
    frequencies (you provide the number of frequencies, and the frequency
    values can be tuned by the optimizer), and randomized frequencies (you
    provide the number of frequencies, and the frequency values are chosen at
    random at the start of each optimization and then held constant).

    Parameters
    ----------
    duration : float
        The total duration :math:`\tau` of the signal.
    segments_count : int
        The number of segments :math:`N` to use for the piecewise-constant
        approximation.
    initial_coefficient_lower_bound : float, optional
        The lower bound :math:`c_\mathrm{min}` on the initial coefficient
        values. Defaults to -1.
    initial_coefficient_upper_bound : float, optional
        The upper bound :math:`c_\mathrm{max}` on the initial coefficient
        values. Defaults to 1.
    fixed_frequencies : list[float], optional
        The fixed non-zero frequencies :math:`\{f_m\}` to use for the Fourier
        basis. Must be non-empty if provided. Must be specified in the inverse
        units of `duration` (for example if `duration` is in seconds, these
        values must be given in Hertz).
    optimizable_frequencies_count : int, optional
        The number of non-zero frequencies :math:`M` to use, if the
        frequencies can be optimized. Must be greater than zero if provided.
    randomized_frequencies_count : int, optional
        The number of non-zero frequencies :math:`M` to use, if the
        frequencies are to be randomized but fixed. Must be greater than zero
        if provided.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc(1D, real)
        The optimizable, real-valued, piecewise-constant signal built from the
        appropriate Fourier components.

    Notes
    -----
    This function sets the basis signal frequencies :math:`\{f_m\}`
    depending on the chosen mode:

    * For fixed frequencies, you provide the frequencies directly.
    * For optimizable frequencies, you provide the number of frequencies
      :math:`M`, and this function creates :math:`M` unbounded optimizable
      variables :math:`\{f_m\}`, with initial values in the ranges
      :math:`\{[(m-1)/\tau, m/\tau]\}`.
    * For randomized frequencies, you provide the number of frequencies
      :math:`M`, and this function creates :math:`M` randomized constants
      :math:`\{f_m\}` in the ranges :math:`\{[(m-1)/\tau, m/\tau]\}`.

    After this function creates the :math:`M` frequencies :math:`\{f_m\}`, it
    produces the signal

    .. math::
        \alpha^\prime(t) = v_0 +
        \sum_{m=1}^M [ v_m \cos(2\pi t f_m) + w_m \sin(2\pi t f_m) ],

    where :math:`\{v_m,w_m\}` are (unbounded) optimizable variables, with
    initial values bounded by :math:`c_\mathrm{min}` and
    :math:`c_\mathrm{max}`. This function produces the final
    piecewise-constant signal :math:`\alpha(t)` by sampling
    :math:`\alpha^\prime(t)` at :math:`N` equally spaced points along the
    duration :math:`\tau`, and using those sampled values as the constant
    segment values.

    You can use the signals created by this function for chopped random basis
    (CRAB) optimization [1]_.

    References
    ----------
    .. [1] `P. Doria, T. Calarco, and S. Montangero, Physical Review Letters 106, 190501 (2011).
           <https://doi.org/10.1103/PhysRevLett.106.190501>`_
    """

    name = "real_fourier_pwc_signal"
    optimizable_variable = True
    _module_attr = "create_real_fourier_pwc_signal"
    args = [
        forge.arg("duration", type=float),
        forge.arg("segments_count", type=int),
        forge.arg("initial_coefficient_lower_bound", type=float, default=-1),
        forge.arg("initial_coefficient_upper_bound", type=float, default=1),
        forge.arg("fixed_frequencies", type=Optional[List[float]], default=None),
        forge.arg("optimizable_frequencies_count", type=Optional[int], default=None),
        forge.arg("randomized_frequencies_count", type=Optional[int], default=None),
    ]
    rtype = types.TensorPwc

    def _evaluate_node(
        self, execution_context: "ExecutionContext", args: List, kwargs: Dict
    ) -> Any:
        """Add variable factory to args.

        Parameters
        ----------
        execution_context : ExecutionContext
            helper class for evaluating the value of the node.
        args: List
            argument list for the node.
        kwargs: Dict
            keyword arguments for the node.

        Returns
        -------
        Any
            the value of the node.
        """
        variable_factory = execution_context.variable_factory
        args.insert(0, variable_factory)
        return super()._evaluate_node(execution_context, args, kwargs)

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        duration = kwargs.get("duration")
        segments_count = kwargs.get("segments_count")
        check_duration(duration, "duration")
        check_argument_integer(segments_count, "segments_count")
        check_argument(
            segments_count > 0,
            "The segments count must be greater than zero.",
            {"segments_count": segments_count},
        )
        durations = duration / segments_count * np.ones(segments_count)
        return TensorPwcNodeData(
            _operation, values_shape=(), durations=durations, batch_shape=(),
        )


class SymmetrizePwc(CoreNode):
    r"""
    Creates the symmetrization of a piecewise-constant function.

    Parameters
    ----------
    pwc : TensorPwc
        The piecewise-constant function :math:`v(t)` to symmetrize.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc
        The piecewise-constant function :math:`w(t)` defined by
        :math:`w(t)=v(t)` for :math:`0\leq t\leq \tau` and
        :math:`w(t)=v(2\tau-t)` for :math:`\tau\leq t\leq 2\tau`, where
        :math:`\tau` is the duration of :math:`v(t)`.
    """

    name = "symmetrize_pwc"
    _module_attr = "symmetrize_pwc"
    args = [forge.arg("pwc", type=types.TensorPwc)]
    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        pwc = kwargs.get("pwc")
        check_argument(
            isinstance(pwc, TensorPwcNodeData),
            "The pwc parameter must be a TensorPwc.",
            {"pwc": pwc},
        )
        values_shape, batch_shape = validate_values_and_batch_shape(pwc, "pwc",)
        symmetrized_durations = np.concatenate((pwc.durations, pwc.durations[::-1]))
        return TensorPwcNodeData(
            _operation,
            values_shape=values_shape,
            durations=symmetrized_durations,
            batch_shape=batch_shape,
        )


class TimeEvolutionOperatorsPwc(CoreNode):
    """
    Calculates the unitary time-evolution operators for a system defined by a piecewise-constant
    Hamiltonian.

    Parameters
    ----------
    hamiltonian : TensorPwc
        The control Hamiltonian, or batch of control Hamiltonians.
    sample_times : np.ndarray(1D, real)
        The N times at which you want to sample the unitaries. Must be ordered and contain
        at least one element.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        Tensor of shape [..., N, D, D], representing the unitary time evolution.
        The n-th element (along the -3 dimension) represents the unitary (or batch of unitaries)
        from t = 0 to ``sample_times[n]``.
    """

    name = "time_evolution_operators_pwc"
    _module_attr = "create_unitaries_from_pwc_hamiltonian"
    args = [
        forge.arg("hamiltonian", type=types.TensorPwc),
        forge.arg("sample_times", type=np.ndarray),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        hamiltonian = kwargs.get("hamiltonian")
        sample_times = kwargs.get("sample_times")
        check_argument(
            isinstance(hamiltonian, TensorPwcNodeData),
            "The Hamiltonian must be a TensorPwc.",
            {"hamiltonian": hamiltonian},
        )
        values_shape, batch_shape = validate_values_and_batch_shape(
            hamiltonian, "hamiltonian",
        )
        check_sample_times(sample_times, "sample_times")
        validate_hamiltonian(hamiltonian, "hamiltonian")
        time_count = len(sample_times)
        shape = batch_shape + (time_count,) + values_shape
        return TensorNodeData(_operation, shape=shape)
