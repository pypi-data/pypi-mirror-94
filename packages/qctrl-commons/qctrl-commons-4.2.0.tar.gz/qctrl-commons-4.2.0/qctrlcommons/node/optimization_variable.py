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
"""Module for OptimizationVariableNode."""
import forge

from qctrlcommons.exceptions import QctrlException
from qctrlcommons.node.base import Node

from . import types
from .tensorflow import TensorNodeData


class OptimizationVariableNode(Node):
    """Represent the OptimizationVariableNode class."""

    _attr = None
    optimizable_variable = True

    def _evaluate_node(self, execution_context, args, kwargs):
        func = getattr(execution_context.variable_factory, self._attr, None)

        if func is None:
            raise RuntimeError(f"attr missing from variable factory: {self._attr}")

        return func(*args, **kwargs)


class BoundedOptimizationVariable(OptimizationVariableNode):
    r"""
    Creates bounded optimization variables.

    Use this function to create a sequence of variables that can be tuned by
    the optimizer (within specified bounds) in order to minimize the cost
    function.

    Parameters
    ----------
    count : int
        The number :math:`N` of individual real-valued variables to create.
    lower_bound : float
        The lower bound :math:`v_\mathrm{min}` on the variables.
        The same lower bound applies to all `count` individual variables.
    upper_bound : float
        The upper bound :math:`v_\mathrm{max}` on the variables.
        The same upper bound applies to all `count` individual variables.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The sequence :math:`\{v_n\}` of :math:`N` bounded optimization
        variables, satisfying
        :math:`v_\mathrm{min}\leq v_n\leq v_\mathrm{max}`.

    See Also
    --------
    unbounded_optimization_variable, anchored_difference_bounded_variables
    """

    name = "bounded_optimization_variable"
    _attr = "create_bounded"
    args = [
        forge.arg("count", type=int),
        forge.arg("lower_bound", type=float),
        forge.arg("upper_bound", type=float),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        count = kwargs["count"]
        lower_bound = kwargs["lower_bound"]
        upper_bound = kwargs["upper_bound"]
        if count <= 0:
            raise QctrlException(f"count={count} must be positive.")
        if upper_bound <= lower_bound:
            raise QctrlException(
                f"lower_bound={lower_bound} must be less than upper_bound={upper_bound}."
            )
        return TensorNodeData(_operation, shape=(count,))


class UnboundedOptimizationVariable(OptimizationVariableNode):
    r"""
    Creates unbounded optimization variables.

    Use this function to create a sequence of variables that can be tuned by
    the optimizer (with no bounds) in order to minimize the cost function.

    Parameters
    ----------
    count : int
        The number :math:`N` of individual real-valued variables to create.
    initial_lower_bound : float
        The lower bound on the interval used to initialize the variables.
        The same initial lower bound applies to all `count` individual
        variables.
    initial_upper_bound : float
        The upper bound on the interval used to initialize the variables.
        The same initial upper bound applies to all `count` individual
        variables.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The sequence :math:`\{v_n\}` of :math:`N` unbounded optimization
        variables.

    See Also
    --------
    bounded_optimization_variable, anchored_difference_bounded_variables
    """

    name = "unbounded_optimization_variable"
    _attr = "create_unbounded"
    args = [
        forge.arg("count", type=int),
        forge.arg("initial_lower_bound", type=float),
        forge.arg("initial_upper_bound", type=float),
    ]
    rtype = types.Tensor

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        count = kwargs["count"]
        initial_lower_bound = kwargs["initial_lower_bound"]
        initial_upper_bound = kwargs["initial_upper_bound"]
        if count <= 0:
            raise QctrlException(f"count={count} must be positive.")
        if initial_upper_bound <= initial_lower_bound:
            raise QctrlException(
                f"initial_lower_bound={initial_lower_bound} must be less than "
                f"initial_upper_bound={initial_upper_bound}."
            )
        return TensorNodeData(_operation, shape=(count,))
