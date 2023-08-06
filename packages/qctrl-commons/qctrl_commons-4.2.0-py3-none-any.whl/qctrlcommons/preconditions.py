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
"""Utilities for running verifications and performing common transformations on inputs."""

from typing import (
    Any,
    Optional,
)

import numpy as np

from qctrlcommons.exceptions import QctrlArgumentsValueError


def check_argument(
    condition: Any, description: str, arguments: dict, extras: Optional[dict] = None
) -> None:
    """
    Raises a QctrlArgumentsValueError with the specified parameters if
    the given condition is false, otherwise does nothing.
    """
    if condition:
        return
    raise QctrlArgumentsValueError(description, arguments, extras=extras)


def check_argument_hermitian(array: np.ndarray, argument_name: str):
    """
    Raises a QctrlArgumentsValueError if the specified array is not a Hermitian operator,
    otherwise does nothing.
    """
    check_argument(
        len(array.shape) == 2,
        "Operator must be Hermitian, but is not 2D.",
        {argument_name: array},
    )
    check_argument(
        array.shape[0] == array.shape[1],
        "Operator must be Hermitian, but is non-square.",
        {argument_name: array},
    )
    check_argument(
        np.allclose(array, array.T.conj()),
        "Operator must be Hermitian, but does not equal its Hermitian conjugate.",
        {argument_name: array},
    )


def check_argument_non_hermitian(array: np.ndarray, argument_name: str):
    """
    Raises a QctrlArgumentsValueError if the specified array is a Hermitian operator,
    otherwise does nothing.
    """
    check_argument(
        len(array.shape) == 2,
        "Operator must be non-Hermitian, but is not 2D.",
        {argument_name: array},
    )
    check_argument(
        array.shape[0] == array.shape[1],
        "Operator must be non-Hermitian, but is non-square.",
        {argument_name: array},
    )
    check_argument(
        not np.allclose(array, array.T.conj()),
        "Operator must be non-Hermitian, but equals its Hermitian conjugate (i.e. is Hermitian).",
        {argument_name: array},
    )


def check_argument_unitary(array: np.ndarray, argument_name: str):
    """
    Raises a QctrlArgumentsValueError if the specified array is not a unitary operator,
    otherwise does nothing.
    """
    check_argument(
        len(array.shape) == 2,
        "Operator must be unitary, but is not 2D.",
        {argument_name: array},
    )
    check_argument(
        array.shape[0] == array.shape[1],
        "Operator must be unitary, but is non-square.",
        {argument_name: array},
    )
    check_argument(
        np.allclose(array @ array.T.conj(), np.identity(array.shape[0])),
        "Operator must be unitary, but its Hermitian conjugate is not its inverse.",
        {argument_name: array},
    )


def check_argument_operator(array: np.ndarray, argument_name: str):
    """
    Raises a QctrlArgumentsValueError if the specified array is not an operator (square),
    otherwise does nothing.
    """
    check_argument(
        len(array.shape) == 2, "Operator must be 2D.", {argument_name: array}
    )
    check_argument(
        array.shape[0] == array.shape[1],
        "Operator must be square.",
        {argument_name: array},
    )


def check_argument_partial_isometry(array: np.ndarray, argument_name: str) -> bool:
    """
    Raises a QctrlArgumentsValueError if the specified array is not a
    partial isometry. (V is a partial isometry iff VV^†V = V)
    """
    check_argument(
        len(array.shape) == 2,
        "Operator must be a partial isometry, but is not 2D.",
        {argument_name: array},
    )
    check_argument(
        array.shape[0] == array.shape[1],
        "Operator must be a partial isometry, but is non-square.",
        {argument_name: array},
    )
    check_argument(
        np.allclose(array @ array.T.conj() @ array, array),
        "Operator must be a partial isometry, but does not yield itself "
        "when multiplied by its adjoint and then itself.",
        {argument_name: array},
    )


def check_argument_orthogonal_projection_operator(
    array: np.ndarray, argument_name: str
):
    """
    Raises a QctrlArgumentsValueError if the specified array is not an orthogonal
    projection operator (Hermitian and idempotent), otherwise does nothing.
    """
    check_argument(
        len(array.shape) == 2,
        "Operator must be an orthogonal projection operator, but is not 2D.",
        {argument_name: array},
    )
    check_argument(
        array.shape[0] == array.shape[1],
        "Operator must be an orthogonal projection operator, but is non-square.",
        {argument_name: array},
    )
    check_argument(
        np.allclose(array, array.T.conj()),
        "Operator must be an orthogonal projection operator, but is not Hermitian.",
        {argument_name: array},
    )
    check_argument(
        np.allclose(array, array @ array),
        "Operator must be an orthogonal projection operator, but is not idempotent (does not equal "
        "its square).",
        {argument_name: array},
    )


def check_argument_nonzero(array: np.ndarray, argument_name: str):
    """
    Raises a QctrlArgumentsValueError if all values in the specified array are zero.
    """
    check_argument(
        np.any(array),
        "Array must contain some non-zero elements.",
        {argument_name: array},
    )


def check_argument_iteratable(argument, argument_name):
    """
    Raises QctrlArgumentsValueError if the argument is not iteratable.
    """
    try:
        iter(argument)
    except TypeError as error:
        raise QctrlArgumentsValueError(
            "The argument must be iteratable.", {argument_name: argument},
        ) from error


def check_argument_integer(argument, argument_name):
    """
    Raises QctrlArgumentsValueError if the argument is not an integer.
    """
    check_argument(
        np.isscalar(argument),
        "The argument must be scalar.",
        {argument_name: argument},
    )
    check_argument(
        np.isreal(argument), "The argument must be real.", {argument_name: argument},
    )
    check_argument(
        argument % 1 == 0,
        "The argument must be an integer.",
        {argument_name: argument},
    )


def check_argument_numeric(argument, argument_name):
    """
    Raises QctrlArgumentsValueError if the argument is a NumPy array of
    a non-numeric data type. Does nothing if the argument doesn't have a
    field `argument.dtype.kind` (which all NumPy arrays have).
    """
    if hasattr(argument, "dtype"):
        if hasattr(argument.dtype, "kind"):
            check_argument(
                argument.dtype.kind in "iufc",
                "The argument must contain data of a numeric type.",
                {argument_name: argument},
                extras={f"{argument_name}.dtype": argument.dtype},
            )


def check_duration(duration, duration_name):
    """
    Checks that the duration is valid.

    A valid duration is a positive real scalar.

    Parameters
    ----------
    duration: number
        The duration to be tested.
    duration_name : str
        The name of the parameter of the duration.
    """
    check_argument(
        np.isscalar(duration),
        "The value of the duration must be scalar.",
        {duration_name: duration},
    )
    check_argument(
        np.isreal(duration),
        "The value of the duration must be real.",
        {duration_name: duration},
    )
    check_argument(
        duration >= 0,
        "The value of the duration must not be negative.",
        {duration_name: duration},
    )


def check_sample_times(sample_times, sample_times_name):
    """
    Checks that the sample_times array is valid.

    A valid sample_times array is one-dimensional, only contains real
    numbers, is ordered, and has at least one element.

    Parameters
    ----------
    sample_times : np.ndarray
        The array to be tested.
    sample_times_name : str
        The name of the array.
    """
    check_argument_numeric(sample_times, sample_times_name)

    # This makes sure that extracting shape doesn't throw an error if the
    # user passes a list. Instead, a list will fail the next test, with a
    # more meaningful message.
    shape = getattr(sample_times, "shape", ())

    check_argument(
        len(shape) == 1,
        "The sample times must be a one-dimensional array.",
        {sample_times_name: sample_times},
    )
    check_argument(
        len(sample_times) > 0,
        "The sample times must be an array with at least one element.",
        {"sample_times": sample_times},
    )
    check_argument(
        np.all(np.isreal(sample_times)),
        "The sample times must be real numbers.",
        {sample_times_name: sample_times},
    )
    check_argument(
        np.all(np.diff(sample_times) >= 0),
        "The sample times must be ordered.",
        {sample_times_name: sample_times},
    )


def check_operator(operator, operator_name):
    """
    Checks that the operator is a square 2D array or tensor, or a batch of them.

    Otherwise, the function raises an exception.

    Parameters
    ----------
    operator : np.ndarray or TensorNodeData
        The operator to be tested for validity.
    operator_name : str
        The name of the operator, used for the error messages.
    """
    check_argument_numeric(operator, operator_name)

    # Obtains shape in a way that doesn't throw an obscure error message if
    # the user passes a list or a TensorPwc by mistake. Instead, an error is
    # thrown in the next check_argument.
    shape = getattr(operator, "shape", ())

    check_argument(
        len(shape) >= 2,
        "The operator must have at least two dimensions.",
        {operator_name: operator},
        extras={f"{operator_name}.shape": shape},
    )
    check_argument(
        shape[-1] == shape[-2],
        "The last two dimensions of the operator must be equal.",
        {operator_name: operator},
        extras={f"{operator_name}.shape": shape},
    )
