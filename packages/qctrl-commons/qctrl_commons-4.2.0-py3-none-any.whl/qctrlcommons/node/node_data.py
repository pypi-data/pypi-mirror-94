"""Module for inherited wrapper class"""
from dataclasses import dataclass
from typing import Tuple

import numpy as np

from qctrlcommons.node.attribute import GetAttributeNode
from qctrlcommons.node.tensorflow import TensorNodeData
from qctrlcommons.node.wrapper import (
    NamedNodeData,
    NodeData,
)


@dataclass
class TensorPwcNodeData(NamedNodeData):
    """
    Wrapper class for TensorPwc type Node.
    """

    values_shape: Tuple[int]
    durations: np.ndarray
    batch_shape: Tuple[int]

    @property
    def values(self):
        """
        Access to the values in TensorPwc.
        """
        node_data = GetAttributeNode.create_pf()(self, "values")
        shape = (
            tuple(self.batch_shape) + (len(self.durations),) + tuple(self.values_shape)
        )
        return TensorNodeData(node_data.operation, shape=shape)


@dataclass
class StfNodeData(NodeData):
    """
    Wrapper class for Stf type Node.
    """

    values_shape: Tuple[int]
    batch_shape: Tuple[int]


@dataclass
class SparsePwcNodeData(NodeData):
    """
    Wrapper class for SparsePwc type Node.
    """

    values_shape: Tuple[int]


@dataclass
class TargetNodeData(NamedNodeData):
    """
    Wrapper class for Target type node
    """

    values_shape: Tuple[int]
