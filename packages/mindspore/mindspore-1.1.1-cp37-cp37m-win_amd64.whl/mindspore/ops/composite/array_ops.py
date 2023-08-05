# Copyright 2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""array Operations."""
from mindspore.ops.composite.multitype_ops import _constexpr_utils as const_utils
from mindspore.common import dtype as mstype
from mindspore._checkparam import Validator as validator
from mindspore._checkparam import Rel
from mindspore.ops.primitive import constexpr
from mindspore.ops import functional as F
from .. import operations as P
from ..operations import _inner_ops as inner


@constexpr
def _check_is_int(arg_value, arg_name, op_name):
    arg_value = validator.check_is_int(arg_value, arg_name, op_name)
    return arg_value


@constexpr
def _check_positive_int(arg_value, arg_name, op_name):
    arg_value = validator.check_positive_int(arg_value, arg_name, op_name)
    return arg_value


@constexpr
def _check_axis_range(arg_value, limit, arg_name, op_name):
    arg_value = validator.check_int_range(arg_value, -limit, limit, Rel.INC_LEFT, arg_name, op_name)
    return arg_value


@constexpr
def _cal_repeat_dims(x_rank, rep, expand_axis):
    rep_dims = [1] * (x_rank + 1)
    rep_dims[expand_axis] = rep
    return tuple(rep_dims)


@constexpr
def _cal_reshape(x_shape, rep, axis):
    x_reshape = list(x_shape)
    x_reshape[axis] *= rep
    return tuple(x_reshape)


def repeat_elements(x, rep, axis=0):
    """
    Repeat elements of a tensor along an axis, like np.repeat.

    Args:
        x (Tensor): The tensor to repeat values for. Must be of type: float16,
            float32, int8, uint8, int16, int32, or int64.
        rep (int): The number of times to repeat, must be positive, required.
        axis (int): The axis along which to repeat, default 0.

    Outputs:
        One tensor with values repeated along the specified axis. If x has shape
        (s1, s2, ..., sn) and axis is i, the output will have shape (s1, s2, ...,
        si * rep, ..., sn). The output type will be the same as the type of `x`.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``

    Examples:
        >>> x = Tensor(np.array([[0, 1, 2], [3, 4, 5]]), mindspore.int32)
        >>> output = C.repeat_elements(x, rep = 2, axis = 0)
        >>> print(output)
        [[0 1 2]
         [0 1 2]
         [3 4 5]
         [3 4 5]]
    """
    const_utils.check_valid_type(F.dtype(x), mstype.number_type, 'input x')
    rep = _check_positive_int(rep, "rep", "repeat_elements")
    axis = _check_is_int(axis, "axis", "repeat_elements")

    shape_op = P.Shape()
    rank_op = P.Rank()
    tile_op = P.Tile()
    expand_dims_op = P.ExpandDims()
    reshape_op = P.Reshape()

    x_rank = rank_op(x)
    axis = _check_axis_range(axis, x_rank, "axis", "repeat_elements")

    expand_axis = axis + 1
    x_expand = expand_dims_op(x, expand_axis)
    rep_dims = _cal_repeat_dims(x_rank, rep, expand_axis)
    x_expand = tile_op(x_expand, rep_dims)
    x_shape = shape_op(x)
    x_reshape = _cal_reshape(x_shape, rep, axis)
    x_rep = reshape_op(x_expand, x_reshape)

    return x_rep

def sequence_mask(lengths, maxlen):
    """
    Returns a mask tensor representing the first N positions of each cell.

    If lengths has shape [d_1, d_2, ..., d_n], then the resulting tensor mask has type dtype and shape
    [d_1, d_2, ..., d_n, maxlen], with mask[i_1, i_2, ..., i_n, j] = (j < lengths[i_1, i_2, ..., i_n])

    Inputs:
        - **lengths** (Tensor) - Tensor to calculate the mask for. All values in this tensor should be
          less than or equal to `maxlen`. Values greater than `maxlen` will be treated as `maxlen`.
          Must be type int32 or int64.

        - **maxlen** (int) - size of the last dimension of returned tensor. Must be positive and same
          type as elements in `lengths`.

    Outputs:
        One mask tensor of shape lengths.shape + (maxlen,).

    Supported Platforms:
        ``GPU``

    Examples:
        >>> x = Tensor(np.array([[1, 3], [2, 0]]))
        >>> output = C.sequence_mask(x, 3)
        >>> print(output)
        [[[True, False, False],
          [True, True, True]],
         [[True, True, False],
          [False, False, False]]]
    """
    return inner.SequenceMask()(lengths, maxlen)
