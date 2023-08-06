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
"""Module for ModuleNode."""
from numbers import Number
from types import ModuleType
from typing import (
    Any,
    Callable,
    Dict,
    List,
)

import numpy as np

from qctrlcommons.node.base import Node


class ModuleNode(Node):
    """A Node that is implemented by a python module."""

    _module_name = None
    _module_attr = None

    def _get_module(self, execution_context: "ExecutionContext") -> ModuleType:
        module = getattr(execution_context, self._module_name, None)

        if module is None:
            raise RuntimeError(
                f"module missing from execution_context: {self._module_name}"
            )

        return module

    def _evaluate_node(
        self, execution_context: "ExecutionContext", args: List, kwargs: Dict
    ) -> Any:
        """
        Evaluate the node by executing its callable module attribute.

        Parameters
        ----------
        execution_context : ExecutionContext
            Helper class for evaluating the value of the node.
        args : List
            Argument list for the node.
        kwargs : Dict
            Keyword arguments for the node.

        Returns
        -------
        Any
            The value of the node.
        """
        value: callable = self._get_attr_from_module(
            execution_context, self._module_attr
        )
        return value(*args, **kwargs)

    def _get_attr_from_module(
        self, execution_context: "ExecutionContext", attr_path: str
    ) -> Callable:
        """
        Get attribute from the execution context.

        Parameters
        ----------
        execution_context : ExecutionContext
            Helper class for evaluating the value of node.
        attr_path: str
            The dotted path within our module. (e.g. "calculate_mean", "ions.ms_phases")

        Returns
        -------
        Callable
            Function, method, or class in our module.

        Raises
        ------
        RuntimeError
            When the object cannot be found in our module.
            When the object is not callable.
        """
        return get_attr_from_module(self._get_module(execution_context), attr_path)


def get_attr_from_module(module: ModuleType, attr_path: str) -> Callable:
    """
    Get attribute from the execution context.

    Parameters
    ----------
    module: ModuleType
        The module containing the callable. (e.g. qctrlcore)
    attr_path: str
        The dotted path within the module. (e.g. "calculate_mean", "ions.ms_phases")

    Returns
    -------
    Callable
        Function, method, or class in the module.

    Raises
    ------
    RuntimeError
        When the object cannot be found in the module.
    ValueError
        When the object is not callable.
    """
    value = module
    for name in attr_path.split("."):
        value = getattr(value, name, None)
        if value is None:
            raise RuntimeError(f"attr missing from module: {attr_path}")

    if not callable(value):
        raise ValueError(f"Want {attr_path} to be callable. Got {value!r}")

    return value


class CoreNode(ModuleNode):
    """Abstract class to represent the module is qctrlcore."""

    _module_name = "qctrlcore"


class TensorFlowNode(ModuleNode):
    """Represents TensorFlowNode class."""

    _module_name = "tensorflow"

    # List of numeric argument names of the node (Numbers, np.arrays, tf.Tensors) that should have
    # the same type. When the node is evaluated, if any of these arguments is complex-valued, they
    # are cast into tf.complex128 tf.Tensors. If not, they are cast into tf.float64 tf.Tensors.
    _same_type_args = []

    def _evaluate_node(self, execution_context, args: List, kwargs: Dict):
        """Handle different dtype of value before evaluate the node.

        Parameters
        ----------
        execution_context : ExecutionContext
            helper class for evaluating the value of the node.
        args : List
            argument list for the node.
        kwargs : Dict
            keyword arguments for the node.

        Returns
        -------
        Any
            the value of the node.

        Raises
        ------
        TypeError
            If any of the arguments in _same_type_args is not a tf.Tensor, an np.ndarray, or a
            Number.
        """
        tf = execution_context.tensorflow  # pylint:disable=invalid-name

        def _is_complex(value):
            """
            Returns whether the passed tf.Tensor, np.ndarray, or Number is complex-valued.
            """
            if tf.is_tensor(value):
                return value.dtype.is_complex

            if isinstance(value, (Number, np.ndarray)):
                dtype = type(value) if isinstance(value, Number) else value.dtype
                return np.issubdtype(dtype, np.complexfloating)

            raise TypeError(f"{value} is not a tf.Tensor, an np.ndarray, or a Number.")

        def _cast_or_convert_to_tensor(value, dtype):
            """
            If a tf.Tensor is passed, it is returned cast into the given dtype.
            If a Number or np.ndarray is passed, it is returned as a tf.Tensor of the given dtype.
            """
            if tf.is_tensor(value):
                if value.dtype == dtype:
                    return value
                return tf.cast(value, dtype=dtype)

            return tf.constant(value, dtype=dtype)

        arg_names = [arg.name for arg in self.args]

        # Check if complex-valued _same_type_args have been passed.
        are_complex = [
            _is_complex(arg)
            for arg_name, arg in list(zip(arg_names, args)) + list(kwargs.items())
            if arg_name in self._same_type_args
        ]

        # If any are complex cast to tf.complex128, if not to tf.float64.
        cast_dtype = tf.complex128 if any(are_complex) else tf.float64

        # Cast all args and kwargs in _same_type_args to cast_dtype.
        for index, arg in enumerate(args):
            if arg_names[index] in self._same_type_args:
                args[index] = _cast_or_convert_to_tensor(arg, cast_dtype)

        for key, value in kwargs.items():
            if key in self._same_type_args:
                kwargs[key] = _cast_or_convert_to_tensor(value, cast_dtype)

        return super()._evaluate_node(execution_context, args, kwargs)
