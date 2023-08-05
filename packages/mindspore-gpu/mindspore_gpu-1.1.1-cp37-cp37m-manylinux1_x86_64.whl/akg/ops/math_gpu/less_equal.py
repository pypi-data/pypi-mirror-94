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

"""operator dsl function: lessequal"""
import akg.tvm
import akg.topi
from akg.utils.dsl_create import produce_shapes
from akg.utils import validation_check as vc_util


@vc_util.check_input_type(akg.tvm.tensor.Tensor, akg.tvm.tensor.Tensor)
def less_equal(input1, input2):
    """
    Check whether input1 lessequals to input2.

    Args:
        input1 (tvm.tensor.Tensor): Tensor.
        input2 (tvm.tensor.Tensor): Tensor.

    Returns:
        tvm.tensor.Tensor. If input1 lessequal to input2 return True, else return False.
    """
    shape1 = [x.value for x in input1.shape]
    shape2 = [x.value for x in input2.shape]
    vc_util.check_shape(shape1)
    vc_util.check_shape(shape2)

    shape1, shape2, shape = produce_shapes(shape1, shape2)

    vc_util.elemwise_dtype_check(input1.dtype, input2.dtype)
    dtype = input1.dtype

    # get lessequal compute
    t_value = akg.tvm.compute(shape, lambda *indice: akg.tvm.const(1, dtype), "T")
    f_value = akg.tvm.compute(shape, lambda *indice: akg.tvm.const(0, dtype), "F")

    input1_bro = akg.topi.broadcast_to(input1, shape)
    input2_bro = akg.topi.broadcast_to(input2, shape)
    c_out = akg.tvm.compute(shape, lambda *indice: akg.tvm.expr.Select(input1_bro[indice] <= input2_bro[indice],
                                                                         t_value[indice], f_value[indice]), name="C")
    res = akg.tvm.compute(shape, lambda *indice: c_out(*indice).astype("bool"), name="res")

    return res
