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
"""Module for OperatorNode."""
from typing import (
    Dict,
    List,
)

import forge
import numpy as np

from qctrlcommons.node.module import ModuleNode
from qctrlcommons.node.utils import (
    validate_shape,
    validate_values_and_batch_shape,
)
from qctrlcommons.preconditions import (
    check_argument,
    check_duration,
    check_operator,
)

from . import types
from .node_data import (
    StfNodeData,
    TensorPwcNodeData,
)


class OperatorNode(ModuleNode):
    """Represents OperatorNode class."""

    _module_name = "qctrlcore"

    def _evaluate_node(
        self, execution_context: "ExecutionContext", args: List, kwargs: Dict
    ):
        """Create the Operator object and then evaluate the node.

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
        # create Operator object
        if kwargs.get("operator", None) is not None:
            kwargs["operator"] = self._get_attr_from_module(
                execution_context, "Operator"
            )(kwargs["operator"])
        else:
            args_list = [arg.name for arg in self.args]
            operator_index = args_list.index("operator")
            args[operator_index] = self._get_attr_from_module(
                execution_context, "Operator"
            )(args[operator_index])
        return super()._evaluate_node(execution_context, args, kwargs)


class PwcOperator(OperatorNode):
    """
    Creates a constant operator multiplied by a piecewise-constant signal.

    Parameters
    ----------
    signal : TensorPwc
        The piecewise-constant signal :math:`a(t)`, or a batch of
        piecewise-constant signals.
    operator : np.ndarray
        The operator :math:`A`. It must have two equal dimensions.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc
        The piecewise-constant operator :math:`a(t)A` (or a batch of
        piecewise-constant operators, if you provide a batch of
        piecewise-constant signals).
    """

    name = "pwc_operator"
    _module_attr = "create_pwc_operator"
    args = [
        forge.arg("signal", type=types.TensorPwc),
        forge.arg("operator", type=np.ndarray),
    ]
    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        signal = kwargs.get("signal")
        operator = kwargs.get("operator")
        check_argument(
            isinstance(signal, TensorPwcNodeData),
            "The signal must be a TensorPwc.",
            {"signal": signal},
        )
        _, batch_shape = validate_values_and_batch_shape(signal, "signal")
        values_shape = validate_shape(operator, "operator")
        check_operator(operator, "operator")
        check_argument(
            len(values_shape) == 2,
            "The operator must be a matrix, not a batch.",
            {"operator": operator},
            extras={"operator.shape": values_shape},
        )
        return TensorPwcNodeData(
            _operation,
            values_shape=values_shape,
            durations=signal.durations,
            batch_shape=batch_shape,
        )


class ConstantPwcOperator(OperatorNode):
    r"""
    Creates a constant piecewise-constant operator over a specified duration.

    Parameters
    ----------
    duration : float
        The duration :math:`\tau` for the resulting piecewise-constant
        operator.
    operator : np.ndarray
        The operator :math:`A`, or a batch of operators. It must have at
        least two dimensions, and its last two dimensions must be equal.
    name : str, optional
        The name of the node.

    Returns
    -------
    TensorPwc
        The constant operator :math:`t\mapsto A` (for :math:`0\leq t\leq\tau`)
        (or a batch of constant operators, if you provide a batch of operators).
    """

    name = "constant_pwc_operator"
    _module_attr = "create_constant_pwc_operator"
    args = [forge.arg("duration", type=float), forge.arg("operator", type=np.ndarray)]
    rtype = types.TensorPwc

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        duration = kwargs.get("duration")
        operator = kwargs.get("operator")
        check_duration(duration, "duration")
        shape = validate_shape(operator, "operator")
        check_operator(operator, "operator")
        return TensorPwcNodeData(
            _operation,
            values_shape=shape[-2:],
            durations=np.array([duration]),
            batch_shape=shape[:-2],
        )


class StfOperator(OperatorNode):
    """
    Creates a constant operator multiplied by a sampleable signal.

    Parameters
    ----------
    signal : Stf
        A sampleable function representing the signal :math:`a(t)`
        or a batch of sampleable functions.
    operator : np.ndarray
        The operator :math:`A`. It must have two equal dimensions.

    Returns
    -------
    Stf
        The sampleable operator :math:`a(t)A` (or batch of sampleable operators, if
        you provide a batch of signals).
    """

    name = "stf_operator"
    _module_attr = "create_stf_operator"
    args = [forge.arg("signal", type=types.Stf), forge.arg("operator", type=np.ndarray)]
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = types.Stf

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        signal = kwargs.get("signal")
        operator = kwargs.get("operator")
        check_argument(
            isinstance(signal, StfNodeData),
            "The signal must be an Stf.",
            {"signal": signal},
        )
        _, batch_shape = validate_values_and_batch_shape(signal, "signal")
        values_shape = validate_shape(operator, "operator")
        check_operator(operator, "operator")
        check_argument(
            len(values_shape) == 2,
            "The operator must be a matrix, not a batch.",
            {"operator": operator},
            extras={"operator.shape": values_shape},
        )
        return StfNodeData(
            _operation, values_shape=values_shape, batch_shape=batch_shape,
        )


class ConstantStfOperator(OperatorNode):
    r"""
    Creates a constant operator.

    Parameters
    ----------
    operator : np.ndarray
        The operator :math:`A`, or a batch of operators. It must have at
        least two dimensions, and its last two dimensions must be equal.

    Returns
    -------
    Stf(3D)
        The operator :math:`t\mapsto A` (or batch of
        operators, if you provide a batch of operators).
    """

    name = "constant_stf_operator"
    _module_attr = "create_constant_stf_operator"
    args = [forge.arg("operator", type=np.ndarray)]
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = types.Stf

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        operator = kwargs.get("operator")
        shape = validate_shape(operator, "operator")
        check_operator(operator, "operator")
        return StfNodeData(_operation, values_shape=shape[-2:], batch_shape=shape[:-2],)
