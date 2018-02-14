# ******************************************************************************
# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

"""Factory functions for all ngraph ops."""

import numpy as np

from pyngraph import Node
from pyngraph.op import Abs, Add, Broadcast, Ceiling, Constant, Convert, Divide, Equal, Exp, \
    Floor, Greater, GreaterEq, Less, LessEq, Log, Maximum, Minimum, Multiply, Negative, \
    NotEqual, Parameter, Sqrt, Subtract

from ngraph_api.utils.broadcasting import get_broadcast_axes
from ngraph_api.utils.decorators import nameable_op, binary_op, unary_op
from ngraph_api.utils.input_validation import assert_list_of_ints
from ngraph_api.utils.types import NumericType, NumericData, TensorShape, make_constant_node, \
    as_node, NodeInput
from ngraph_api.utils.types import get_element_type


@nameable_op
def parameter(shape, dtype=np.float32, name=None):
    # type: (TensorShape, NumericType, str) -> Parameter
    """Return an ngraph Parameter object."""
    assert_list_of_ints(shape, 'Parameter shape must be a list of integer values.')
    element_type = get_element_type(dtype)
    return Parameter(element_type, shape)


@nameable_op
def constant(value, dtype=None, name=None):  # type: (NumericData, NumericType, str) -> Constant
    """Return an ngraph Constant object with the specified value."""
    return make_constant_node(value, dtype)


# Unary ops
@unary_op
def absolute(node, name=None):  # type: (NodeInput, str) -> Node
    """Return node which applies f(x) = abs(x) to the input node elementwise."""
    node = as_node(node)
    return Abs(node)


@unary_op
def sqrt(node, name=None):  # type: (NodeInput, str) -> Node
    """Return node which applies square root to the input node elementwise."""
    return Sqrt(node)


@unary_op
def exp(node, name=None):  # type: (NodeInput, str) -> Node
    """Return node which applies exp to the input node elementwise."""
    return Exp(node)


@unary_op
def log(node, name=None):  # type: (NodeInput, str) -> Node
    """Return node which applies natural logarithm to the input node elementwise."""
    return Log(node)


@unary_op
def negative(node, name=None):  # type: (NodeInput, str) -> Node
    """Return node which applies f(x) = -x to the input node elementwise."""
    return Negative(node)


@unary_op
def floor(node, name=None):  # type: (NodeInput, str) -> Node
    """Return node which applies floor to the input node elementwise."""
    return Floor(node)


@unary_op
def ceiling(node, name=None):  # type: (NodeInput, str) -> Node
    """Return node which applies ceiling to the input node elementwise."""
    return Ceiling(node)


# Binary ops
@binary_op
def divide(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which applies f(x) = A/B to the input nodes elementwise."""
    return Divide(left_node, right_node)


@binary_op
def multiply(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which applies f(x) = A*B to the input nodes elementwise."""
    return Multiply(left_node, right_node)


@binary_op
def subtract(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which applies f(x) = A-B to the input nodes elementwise."""
    return Subtract(left_node, right_node)


@binary_op
def add(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which applies f(x) = A+B to the input nodes elementwise."""
    return Add(left_node, right_node)


@binary_op
def minimum(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which applies the minimum operation to input nodes elementwise."""
    return Minimum(left_node, right_node)


@binary_op
def maximum(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which applies the maximum operation to input nodes elementwise."""
    return Maximum(left_node, right_node)


@binary_op
def equal(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which checks if input nodes are equal elementwise."""
    return Equal(left_node, right_node)


@binary_op
def not_equal(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which checks if input nodes are unequal elementwise."""
    return NotEqual(left_node, right_node)


@binary_op
def greater(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which checks if left input node is greater than the right node elementwise."""
    return Greater(left_node, right_node)


@binary_op
def greater_eq(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which checks if left node is greater or equal to the right node elementwise."""
    return GreaterEq(left_node, right_node)


@binary_op
def less(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which checks if left input node is less than the right node elementwise."""
    return Less(left_node, right_node)


@binary_op
def less_eq(left_node, right_node, name=None):  # type: (NodeInput, NodeInput, str) -> Node
    """Return node which checks if left node is less or equal to the right node elementwise."""
    return LessEq(left_node, right_node)


# Extend Node class to support binary operators
Node.__add__ = add
Node.__sub__ = subtract
Node.__mul__ = multiply
Node.__div__ = divide
Node.__truediv__ = divide
Node.__radd__ = lambda left, right: add(right, left)
Node.__rsub__ = lambda left, right: subtract(right, left)
Node.__rmul__ = lambda left, right: multiply(right, left)
Node.__rdiv__ = lambda left, right: divide(right, left)
Node.__rtruediv__ = lambda left, right: divide(right, left)
Node.__eq__ = equal
Node.__ne__ = not_equal
Node.__lt__ = less
Node.__le__ = less_eq
Node.__gt__ = greater
Node.__ge__ = greater_eq


# Custom ops
@nameable_op
def broadcast(node, new_shape, axis=None, name=None):  # type: (Node, TensorShape, int, str) -> Node
    """Return node which broadcasts input node values to specified shape."""
    return Broadcast(node, new_shape, get_broadcast_axes(new_shape, node.shape, axis))


@nameable_op
def convert(node, new_type, name=None):  # type: (Node, NumericType, str) -> Node
    """Return node which casts input node values to specified type."""
    new_element_type = get_element_type(new_type)
    return Convert(node, new_element_type)
