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
"""Argument and result types for nodes."""

# pylint:disable=too-few-public-methods


class Target:
    """
    A target gate for an infidelity calculation.
    """


class Tensor:
    """
    A multi-dimensional array of data.

    Most functions accepting a :obj:`.Tensor` object can alternatively accept a NumPy array.
    """


class TensorPwc:
    """
    A piecewise-constant tensor-valued function of time (or batch of such functions).

    Attributes
    ----------
    values : Tensor
        The values of the function on the piecewise-constant segments.
    """


class SparsePwc:
    """
    A piecewise-constant sparse-matrix-valued function of time.
    """


class Stf:
    """
    A sampleable tensor-valued function of time (or batch of such functions).

    Notes
    -----
    Stf represents an arbitrary function of time. Piecewise-constant (PWC) or constant functions
    are special cases of Stfs and Q-CTRL python package provides specific APIs to support them.
    Note that as the PWC property can simplify the calculation, you should always consider using
    PWC-related APIs if your system parameters or controls are described by PWC functions.
    """


class Function:
    """
    A generic callable function.
    """


# Registry of all types created by operations.
TYPE_REGISTRY = [
    Target,
    Tensor,
    TensorPwc,
    SparsePwc,
    Stf,
    Function,
]
