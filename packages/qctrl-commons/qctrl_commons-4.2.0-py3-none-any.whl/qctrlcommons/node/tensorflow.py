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

# pylint: disable=too-many-lines
"""Module for TensorFlowNode."""
from dataclasses import dataclass
from typing import (
    List,
    Optional,
    Tuple,
    Union,
)

import forge
import numpy as np

from qctrlcommons.exceptions import QctrlException
from qctrlcommons.node.module import TensorFlowNode
from qctrlcommons.node.utils import (
    validate_broadcasted_shape,
    validate_shape,
)
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_numeric,
)

from . import types
from .attribute import GetItemNode
from .wrapper import NamedNodeData


@dataclass
class TensorNodeData(NamedNodeData):
    """
    Wrapper class for tensor type Node. Override the
    numeric method to support
    binary arithmetic operations with Number/numpy array/Tensor.

    By default ``arr + pf.func_op(*)`` throws an error, since NumPy doesn't know how to add
    `pf.func_op` objects to arrays. Even the fact that the func ops override `__radd__` doesn't
    help, since the NumPy addition takes precedence. We can instead tell NumPy to delegate all
    binary operations to the other operand, by explicitly clearing the `__array_ufunc__` attribute.
    """

    shape: Tuple[int]
    __array_ufunc__ = None

    def __add__(self, other):
        return Addition.create_pf()(self, other)

    def __radd__(self, other):
        return Addition.create_pf()(other, self)

    def __sub__(self, other):
        return Subtract.create_pf()(self, other)

    def __rsub__(self, other):
        return Subtract.create_pf()(other, self)

    def __matmul__(self, other):
        return Matmul.create_pf()(self, other)

    def __rmatmul__(self, other):
        return Matmul.create_pf()(other, self)

    def __mul__(self, other):
        return Multiply.create_pf()(self, other)

    def __rmul__(self, other):
        return Multiply.create_pf()(other, self)

    def __floordiv__(self, other):
        return FloorDivision.create_pf()(self, other)

    def __rfloordiv__(self, other):
        return FloorDivision.create_pf()(other, self)

    def __pow__(self, power):
        return Exponent.create_pf()(self, power)

    def __rpow__(self, other):
        return Exponent.create_pf()(other, self)

    def __truediv__(self, other):
        return Truediv.create_pf()(self, other)

    def __rtruediv__(self, other):
        return Truediv.create_pf()(other, self)

    def __abs__(self):
        return Absolute.create_pf()(self)

    def __neg__(self):
        return Negative.create_pf()(self)

    def __getitem__(self, item) -> "Operation":
        """
        refer to item in pythonflow operation.

        Returns
        -------
        Operation
            getitem operation.
        """
        node_data = GetItemNode.create_pf()(self, item)
        shape = np.empty(self.shape)[item].shape
        return TensorNodeData(node_data.operation, shape=shape)


class Truediv(TensorFlowNode):
    """
    Divides two values element-wise.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The numerator, :math:`x`.
    y : number or np.ndarray or Tensor
        The denominator, :math:`y`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise value of :math:`x/y`.
    """

    name = "truediv"
    _module_attr = "truediv"
    args = [
        forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor]),
        forge.arg("y", type=Union[float, complex, np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["x", "y"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        y_value = kwargs.get("y")
        check_argument_numeric(x_value, "x")
        check_argument_numeric(y_value, "y")
        x_shape = validate_shape(x_value, "x")
        y_shape = validate_shape(y_value, "y")
        shape = validate_broadcasted_shape(x_shape, y_shape, "x", "y")
        return TensorNodeData(_operation, shape=shape)


class Multiply(TensorFlowNode):
    r"""
    Multiplies two values element-wise.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The left multiplicand, :math:`x`.
    y : number or np.ndarray or Tensor
        The right multiplicand, :math:`y`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise value of :math:`x\times y`.
    """

    name = "mul"
    _module_attr = "multiply"
    args = [
        forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor]),
        forge.arg("y", type=Union[float, complex, np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["x", "y"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        y_value = kwargs.get("y")
        check_argument_numeric(x_value, "x")
        check_argument_numeric(y_value, "y")
        x_shape = validate_shape(x_value, "x")
        y_shape = validate_shape(y_value, "y")
        shape = validate_broadcasted_shape(x_shape, y_shape, "x", "y")
        return TensorNodeData(_operation, shape=shape)


class Addition(TensorFlowNode):
    """
    Adds two values element-wise.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The left summand, :math:`x`.
    y : number or np.ndarray or Tensor
        The right summand, :math:`y`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise value of :math:`x+y`.
    """

    name = "add"
    _module_attr = "add"
    args = [
        forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor]),
        forge.arg("y", type=Union[float, complex, np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["x", "y"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        y_value = kwargs.get("y")
        check_argument_numeric(x_value, "x")
        check_argument_numeric(y_value, "y")
        x_shape = validate_shape(x_value, "x")
        y_shape = validate_shape(y_value, "y")
        shape = validate_broadcasted_shape(x_shape, y_shape, "x", "y")
        return TensorNodeData(_operation, shape=shape)


class Subtract(TensorFlowNode):
    """
    Subtracts one value from another element-wise.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value from which to subtract, :math:`x`.
    y : number or np.ndarray or Tensor
        The value to subtract, :math:`y`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise value of :math:`x-y`.
    """

    name = "sub"
    _module_attr = "subtract"
    args = [
        forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor]),
        forge.arg("y", type=Union[float, complex, np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["x", "y"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        y_value = kwargs.get("y")
        check_argument_numeric(x_value, "x")
        check_argument_numeric(y_value, "y")
        x_shape = validate_shape(x_value, "x")
        y_shape = validate_shape(y_value, "y")
        shape = validate_broadcasted_shape(x_shape, y_shape, "x", "y")
        return TensorNodeData(_operation, shape=shape)


class Absolute(TensorFlowNode):
    r"""
    Returns the element-wise absolute value.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise absolute value :math:`\left|x\right|`.
    """

    name = "abs"
    _module_attr = "abs"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Exponent(TensorFlowNode):
    """
    Raises one value to the power of another element-wise.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The base, :math:`x`.
    y : number or np.ndarray or Tensor
        The exponent, :math:`y`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise value of :math:`x^y`.
    """

    name = "pow"
    _module_attr = "pow"
    args = [
        forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor]),
        forge.arg("y", type=Union[float, complex, np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["x", "y"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        y_value = kwargs.get("y")
        check_argument_numeric(x_value, "x")
        check_argument_numeric(y_value, "y")
        x_shape = validate_shape(x_value, "x")
        y_shape = validate_shape(y_value, "y")
        shape = validate_broadcasted_shape(x_shape, y_shape, "x", "y")
        return TensorNodeData(_operation, shape=shape)


class FloorDivision(TensorFlowNode):
    r"""
    Divides two values and then takes the floor of the result, element-wise.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The numerator, :math:`x`.
    y : number or np.ndarray or Tensor
        The denominator, :math:`y`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise value of :math:`\lfloor x/y \rfloor`.
    """

    name = "floordiv"
    _module_attr = "math.floordiv"
    args = [
        forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor]),
        forge.arg("y", type=Union[float, complex, np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["x", "y"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        y_value = kwargs.get("y")
        check_argument_numeric(x_value, "x")
        check_argument_numeric(y_value, "y")
        x_shape = validate_shape(x_value, "x")
        y_shape = validate_shape(y_value, "y")
        shape = validate_broadcasted_shape(x_shape, y_shape, "x", "y")
        return TensorNodeData(_operation, shape=shape)


class ComplexValue(TensorFlowNode):
    """
    Creates a complex number from real and imaginary parts.

    Parameters
    ----------
    real : float or np.ndarray or Tensor
        The real part, :math:`a`.
    imag : float or np.ndarray or Tensor
        The imaginary part, :math:`b`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The complex number :math:`a+ib` element-wise.
    """

    name = "complex_value"
    _module_attr = "complex"
    args = [
        forge.arg("real", type=Union[float, np.ndarray, types.Tensor]),
        forge.arg("imag", type=Union[float, np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["real", "imag"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        real = kwargs.get("real")
        imag = kwargs.get("imag")
        check_argument_numeric(real, "real")
        check_argument_numeric(imag, "imag")
        real_shape = validate_shape(real, "real")
        imag_shape = validate_shape(imag, "imag")
        shape = validate_broadcasted_shape(real_shape, imag_shape, "real", "imag")
        return TensorNodeData(_operation, shape=shape)


class Real(TensorFlowNode):
    r"""
    Returns the element-wise real part.

    Parameters
    ----------
    input : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise real part :math:`\mathop{\mathrm{Re}}(x)`.
    """

    name = "real"
    _module_attr = "math.real"
    args = [forge.arg("input", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        input_value = kwargs.get("input")
        check_argument_numeric(input_value, "input")
        shape = validate_shape(input_value, "input")
        return TensorNodeData(_operation, shape=shape)


class Imag(TensorFlowNode):
    r"""
    Returns the element-wise imaginary part.

    Parameters
    ----------
    input : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise imaginary part :math:`\mathop{\mathrm{Im}}(x)`.
    """

    name = "imag"
    _module_attr = "math.imag"
    args = [forge.arg("input", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        input_value = kwargs.get("input")
        check_argument_numeric(input_value, "input")
        shape = validate_shape(input_value, "input")
        return TensorNodeData(_operation, shape=shape)


class Angle(TensorFlowNode):
    r"""
    Returns the element-wise complex argument.

    Parameters
    ----------
    input : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise argument :math:`\arg(x)`.
    """

    name = "angle"
    _module_attr = "math.angle"
    args = [forge.arg("input", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    # we use _same_type_args to make sure input is cast into float/complex
    # (int values throw an error)
    _same_type_args = ["input"]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        input_value = kwargs.get("input")
        check_argument_numeric(input_value, "input")
        shape = validate_shape(input_value, "input")
        return TensorNodeData(_operation, shape=shape)


class Sqrt(TensorFlowNode):
    r"""
    Returns the element-wise square root.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise square root :math:`\sqrt{x}`.
    """

    name = "sqrt"
    _module_attr = "sqrt"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Exp(TensorFlowNode):
    r"""
    Returns the element-wise exponential.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise exponential :math:`\exp{x}`.
    """

    name = "exp"
    _module_attr = "exp"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Sin(TensorFlowNode):
    r"""
    Returns the element-wise sine.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise sine :math:`\sin{x}`.
    """

    name = "sin"
    _module_attr = "sin"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Cos(TensorFlowNode):
    r"""
    Returns the element-wise cosine.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise cosine :math:`\cos{x}`.
    """

    name = "cos"
    _module_attr = "cos"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Tan(TensorFlowNode):
    r"""
    Returns the element-wise tangent.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise tangent :math:`\tan{x}`.
    """

    name = "tan"
    _module_attr = "tan"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Arcsin(TensorFlowNode):
    r"""
    Returns the element-wise arcsine.

    Parameters
    ----------
    x : float or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise arcsine :math:`\arcsin{x}`.
        Outputs will be in the range of :math:`[-\pi/2, \pi/2]`.
    """

    name = "arcsin"
    _module_attr = "asin"
    args = [forge.arg("x", type=Union[float, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Arccos(TensorFlowNode):
    r"""
    Returns the element-wise arccosine.

    Parameters
    ----------
    x : float or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise arccosine :math:`\arccos{x}`.
        Outputs will be in the range of :math:`[0, \pi]`.
    """

    name = "arccos"
    _module_attr = "acos"
    args = [forge.arg("x", type=Union[float, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Arctan(TensorFlowNode):
    r"""
    Returns the element-wise arctangent.

    Parameters
    ----------
    x : float or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise arctangent :math:`\arctan{x}`.
        Outputs will be in the range of :math:`(-\pi/2, \pi/2)`.
    """

    name = "arctan"
    _module_attr = "atan"
    args = [forge.arg("x", type=Union[float, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Sum(TensorFlowNode):
    """
    Returns the sum of all the elements in a tensor (or a list of tensors with the same shape).

    Parameters
    ----------
    input_tensor : np.ndarray or Tensor or List[Tensor]
        The tensor whose elements you want to sum.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The single-element tensor containing the input tensor's sum.
    """

    name = "sum"
    _module_attr = "reduce_sum"
    args = [
        forge.arg(
            "input_tensor", type=Union[np.ndarray, types.Tensor, List[types.Tensor]],
        )
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        input_tensor = kwargs.get("input_tensor")
        check_argument_numeric(input_tensor, "input_tensor")
        if isinstance(input_tensor, list):
            shapes = [
                validate_shape(tensor, f"input_tensor[{n}]")
                for n, tensor in enumerate(input_tensor)
            ]
            for index, shape in enumerate(shapes[1:]):
                check_argument(
                    shape == shapes[0],
                    "All elements of the input_tensor list must have the same shape.",
                    {"input_tensor": input_tensor},
                    extras={
                        "input_tensor[0].shape": shapes[0],
                        f"input_tensor[{index}].shape": shape,
                    },
                )
        return TensorNodeData(_operation, shape=())


class Log(TensorFlowNode):
    r"""
    Returns the element-wise natural logarithm.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise natural logarithm :math:`\ln{x}`.
    """

    name = "log"
    _module_attr = "math.log"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        shape = validate_shape(x_value, "x")
        check_argument_numeric(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Cosh(TensorFlowNode):
    r"""
    Returns the element-wise hyperbolic cosine.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise hyperbolic cosine :math:`\cosh{x}`.
    """

    name = "cosh"
    _module_attr = "cosh"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Sinh(TensorFlowNode):
    r"""
    Returns the element-wise hyperbolic sine.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise hyperbolic sine :math:`\sinh{x}`.
    """

    name = "sinh"
    _module_attr = "sinh"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Tanh(TensorFlowNode):
    r"""
    Returns the element-wise hyperbolic tangent.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise hyperbolic tangent :math:`\tanh{x}`.
    """

    name = "tanh"
    _module_attr = "tanh"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Negative(TensorFlowNode):
    """
    Returns element-wise negative value.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise negative value :math:`-x`.
    """

    name = "neg"
    _module_attr = "negative"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Reverse(TensorFlowNode):
    """
    Reverses a tensor along some specified dimensions.

    Parameters
    ----------
    tensor : np.ndarray or Tensor
        The tensor that you want to reverse.
    axis : List[int]
        The dimensions along which you want to reverse the tensor.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The reversed tensor.
    """

    name = "reverse"
    _module_attr = "reverse"
    args = [
        forge.arg("tensor", type=Union[np.ndarray, types.Tensor]),
        forge.arg("axis", type=List[int]),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        tensor = kwargs.get("tensor")
        check_argument_numeric(tensor, "tensor")
        shape = validate_shape(tensor, "tensor")
        return TensorNodeData(_operation, shape=shape)


class CumulativeSum(TensorFlowNode):
    """
    Calculates the cumulative sum of a tensor along a specified dimension.

    Parameters
    ----------
    x : np.ndarray or Tensor
        The tensor whose elements you want to sum. It must have at least
        one dimension.
    axis : int, optional
        The dimension along which you want to sum the tensor. Defaults to 0.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The cumulative sum of `x` along dimension `axis`.
    """

    name = "cumulative_sum"
    _module_attr = "cumsum"
    args = [
        forge.arg("x", type=Union[np.ndarray, types.Tensor]),
        forge.arg("axis", default=0, type=int),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        if len(shape) == 0:
            raise QctrlException(
                f"The shape of x={x_value} must have at least 1 dimension."
            )
        return TensorNodeData(_operation, shape=shape)


class Conjugate(TensorFlowNode):
    r"""
    Returns the element-wise conjugate.

    Parameters
    ----------
    x : number or np.ndarray or Tensor
        The value, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The element-wise conjugate :math:`x^\ast`.
    """

    name = "conjugate"
    _module_attr = "math.conj"
    args = [forge.arg("x", type=Union[float, complex, np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        shape = validate_shape(x_value, "x")
        return TensorNodeData(_operation, shape=shape)


class Adjoint(TensorFlowNode):
    r"""
    Returns the conjugate of the input tensor representing a 2D matrix with the two innermost
    dimensions transposed.

    Parameters
    ----------
    matrix : np.ndarray or Tensor
        The matrix (or batch of matrices), :math:`A`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The adjoint tensor :math:`A^\dagger`.
    """

    name = "adjoint"
    _module_attr = "linalg.adjoint"
    args = [forge.arg("matrix", type=Union[np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        matrix = kwargs.get("matrix")
        check_argument_numeric(matrix, "matrix")
        matrix_shape = validate_shape(matrix, "matrix")
        if len(matrix_shape) < 2:
            raise QctrlException(
                f"The shape of matrix={matrix} must have at least 2 dimensions."
            )
        shape = matrix_shape[:-2] + (matrix_shape[-1], matrix_shape[-2])
        return TensorNodeData(_operation, shape=shape)


class Trace(TensorFlowNode):
    r"""
    Returns the sum of the diagonals of each innermost matrix of the input tensor.

    Parameters
    ----------
    x : np.ndarray or Tensor
        The matrix whose trace you want to calculate, :math:`x`.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The trace of the input tensor :math:`\mathop{\mathrm{Tr}}(x)`.
    """

    name = "trace"
    _module_attr = "linalg.trace"
    args = [forge.arg("x", type=Union[np.ndarray, types.Tensor])]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        x_value = kwargs.get("x")
        check_argument_numeric(x_value, "x")
        x_shape = validate_shape(x_value, "x")
        if len(x_shape) < 2:
            raise QctrlException(
                f"The shape of x={x_value} must have at least 2 dimensions."
            )
        shape = x_shape[:-2]
        return TensorNodeData(_operation, shape=shape)


class Transpose(TensorFlowNode):
    """
    Returns the input tensor with its dimensions reordered.

    Parameters
    ----------
    a : np.ndarray or Tensor
        The tensor whose dimensions you want to permute, :math:`x`.
    perm : List[int] or np.ndarray(int), optional
        The order of the input dimensions for the returned tensor. If you provide it, it must
        be a permutation of all integers between 0 and ``N-1``, where `N` is the rank of `a`.
        If you don't provide it, the order of the dimensions is inverted, that is to say,
        it defaults to ``[N-1, …, 1, 0]``.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The input tensor with its dimensions permuted. The `i`-th dimension of the returned tensor
        corresponds to the `perm[i]`-th input dimension.
    """

    name = "transpose"
    _module_attr = "transpose"
    args = [
        forge.arg("a", type=Union[np.ndarray, types.Tensor]),
        forge.arg("perm", type=Optional[Union[List[int], np.ndarray]], default=None,),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        a_value = kwargs.get("a")
        perm = kwargs.get("perm")
        check_argument_numeric(a_value, "a")
        check_argument_numeric(perm, "perm")
        a_shape = validate_shape(a_value, "a")
        if perm is None:
            shape = a_shape[::-1]
        else:
            sorted_perm = np.sort(np.array(perm) % len(perm))
            check_argument(
                np.all(sorted_perm == range(len(a_shape))),
                "The value of perm must be a valid permutation of the indices of a.",
                {"perm": perm},
                extras={"a.shape": a_shape},
            )
            shape = tuple(a_shape[dimension] for dimension in perm)
        return TensorNodeData(_operation, shape=shape)


class Matmul(TensorFlowNode):
    """
    Performs the matrix multiplication with the two innermost dimensions of two tensors.
    That is, if the tensors have shapes ``[…, N, M]`` and ``[…, M, P]`` (where ``…`` indicates
    compatible batching dimension) the product is a ``[…, N, P]`` tensor.

    Parameters
    ----------
    a : np.ndarray or Tensor
        The left multiplicand.
    b : np.ndarray or Tensor
        The right multiplicand.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The matrix product between `a` and `b`. If the rank of `a` or `b` is larger than 2, the
        product is carried out between their innermost dimensions.
    """

    name = "matmul"
    _module_attr = "matmul"
    args = [
        forge.arg("a", type=Union[np.ndarray, types.Tensor]),
        forge.arg("b", type=Union[np.ndarray, types.Tensor]),
    ]
    _same_type_args = ["a", "b"]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        a_value = kwargs.get("a")
        b_value = kwargs.get("b")
        check_argument_numeric(a_value, "a")
        check_argument_numeric(b_value, "b")
        a_shape = validate_shape(a_value, "a")
        b_shape = validate_shape(b_value, "b")
        if len(a_shape) < 2:
            raise QctrlException(
                f"The shape of a={a_value} must have at least 2 dimensions."
            )
        if len(b_shape) < 2:
            raise QctrlException(
                f"The shape of b={b_value} must have at least 2 dimensions."
            )
        batch_shape = validate_broadcasted_shape(a_shape[:-2], b_shape[:-2], "a", "b")
        check_argument(
            a_shape[-1] == b_shape[-2],
            "The last dimension of a and the second-to-last dimension of b must be equal",
            {"a": a_value, "b": b_value},
        )
        shape = batch_shape + (a_shape[-2], b_shape[-1])
        return TensorNodeData(_operation, shape=shape)
