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
"""ADA_GRAD"""
from mindspore.ops import functional as F, composite as C, operations as P
from mindspore._checkparam import Validator as validator
from .optimizer import Optimizer

_ada_grad_opt = C.MultitypeFuncGraph("ada_grad_opt")


@_ada_grad_opt.register("Function", "Tensor", "Tensor", "Tensor", "Tensor")
def _tensor_run_opt(opt, learning_rate, weight, accum, gradient):
    """Apply ada_grad optimizer to the weight parameter."""
    success = True
    success = F.depend(success, opt(weight, accum, learning_rate, gradient))
    return success


def _check_param_value(accum, update_slots, prim_name=None):
    """Check inputs param."""
    validator.check_value_type("accum", accum, [float], prim_name)
    validator.check_value_type("update_slots", update_slots, [bool], prim_name)
    validator.check_non_negative_float(accum, "accum", prim_name)


class Adagrad(Optimizer):
    """
    Implements the Adagrad algorithm with ApplyAdagrad Operator.

    Adagrad is an online Learning and Stochastic Optimization.
    Refer to paper `Efficient Learning using Forward-Backward Splitting
    <https://proceedings.neurips.cc/paper/2009/file/621bf66ddb7c962aa0d22ac97d69b793-Paper.pdf>`_.

    Note:
        When separating parameter groups, the weight decay in each group will be applied on the parameters if the
        weight decay is positive. When not separating parameter groups, the `weight_decay` in the API will be applied
        on the parameters without 'beta' or 'gamma' in their names if `weight_decay` is positive.

        To improve parameter groups performance, the customized order of parameters can be supported.

    Args:
        params (Union[list[Parameter], list[dict]]): When the `params` is a list of `Parameter` which will be updated,
            the element in `params` must be class `Parameter`. When the `params` is a list of `dict`, the "params",
            "lr", "weight_decay" and "order_params" are the keys can be parsed.

            - params: Required. The value must be a list of `Parameter`.

            - lr: Optional. If "lr" in the keys, the value of corresponding learning rate will be used.
              If not, the `learning_rate` in the API will be used.

            - weight_decay: Optional. If "weight_decay" in the keys, the value of corresponding weight decay
              will be used. If not, the `weight_decay` in the API will be used.

            - order_params: Optional. If "order_params" in the keys, the value must be the order of parameters and
              the order will be followed in optimizer. There are no other keys in the `dict` and the parameters which
              in the value of 'order_params' must be in one of group parameters.

        accum (float): The starting value for accumulators, must be zero or positive values. Default: 0.1.
        learning_rate (Union[float, Tensor, Iterable, LearningRateSchedule]): A value or a graph for the learning rate.
            When the learning_rate is an Iterable or a Tensor in a 1D dimension, use dynamic learning rate, then
            the i-th step will take the i-th value as the learning rate. When the learning_rate is LearningRateSchedule,
            use dynamic learning rate, the i-th learning rate will be calculated during the process of training
            according to the formula of LearningRateSchedule. When the learning_rate is a float or a Tensor in a zero
            dimension, use fixed learning rate. Other cases are not supported. The float learning rate must be
            equal to or greater than 0. If the type of `learning_rate` is int, it will be converted to float.
            Default: 0.001.
        update_slots (bool): If true, update accumulation. Default: True.
        loss_scale (float): Value for the loss scale. It must be greater than 0.0. Default: 1.0.
        weight_decay (float): Weight decay value to multiply weight, must be zero or positive value. Default: 0.0.

    Inputs:
        - **grads** (tuple[Tensor]) - The gradients of `params` in the optimizer, the shape is the same as the `params`
          in optimizer.

    Outputs:
        Tensor[bool], the value is True.

    Supported Platforms:
        ``Ascend`` ``CPU`` ``GPU``

    Examples:
        >>> net = Net()
        >>> #1) All parameters use the same learning rate and weight decay
        >>> optim = nn.Adagrad(params=net.trainable_params())
        >>>
        >>> #2) Use parameter groups and set different values
        >>> conv_params = list(filter(lambda x: 'conv' in x.name, net.trainable_params()))
        >>> no_conv_params = list(filter(lambda x: 'conv' not in x.name, net.trainable_params()))
        >>> group_params = [{'params': conv_params, 'weight_decay': 0.01},
        ...                 {'params': no_conv_params, 'lr': 0.01},
        ...                 {'order_params': net.trainable_params()}]
        >>> optim = nn.Adagrad(group_params, learning_rate=0.1, weight_decay=0.0)
        >>> # The conv_params's parameters will use default learning rate of 0.1 and weight decay of 0.01.
        >>> # The no_conv_params's parameters will use learning rate of 0.01 and default weight decay of 0.0.
        >>> # The final parameters order in which the optimizer will be followed is the value of 'order_params'.
        >>>
        >>> loss = nn.SoftmaxCrossEntropyWithLogits()
        >>> model = Model(net, loss_fn=loss, optimizer=optim)
    """

    def __init__(self, params, accum=0.1, learning_rate=0.001,
                 update_slots=True, loss_scale=1.0, weight_decay=0.0):
        super(Adagrad, self).__init__(learning_rate, params, weight_decay, loss_scale)
        _check_param_value(accum, update_slots, self.cls_name)
        self.accum = self.parameters.clone(prefix="accum", init=accum)
        self.hyper_map = C.HyperMap()
        self.update_slots = update_slots
        self.opt = P.ApplyAdagrad(update_slots=update_slots)

    def construct(self, grads):
        params = self.parameters
        accum = self.accum
        grads = self.decay_weight(grads)
        grads = self.scale_grad(grads)
        lr = self.get_lr()
        if self.is_group_lr:
            success = self.map_(F.partial(_ada_grad_opt, self.opt), lr, params, accum,
                                grads)
        else:
            success = self.map_(F.partial(_ada_grad_opt, self.opt, lr), params, accum,
                                grads)
        return success
