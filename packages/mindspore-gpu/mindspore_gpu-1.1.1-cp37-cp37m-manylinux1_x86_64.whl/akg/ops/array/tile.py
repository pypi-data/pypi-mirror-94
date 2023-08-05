#!/usr/bin/env python3
# coding: utf-8
# Copyright 2019 Huawei Technologies Co., Ltd
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

"""operator dsl function:tile"""
import akg.topi
from akg.utils import validation_check as vc_util


@vc_util.check_input_type(akg.tvm.tensor.Tensor, (list, tuple))
def tile(data, multiples):
    """
    Repeats the data in the specified dimensions according to the multiples.

    Args:
        data (tvm.tensor.Tensor): Tensor of type float16, float32.
        multiples (Union[list, tuple]): Elements must be int. The number of repetitions.

    Returns:
        tvm.tensor.Tensor, has the same dtype as data.
    """
    shape = [x.value for x in data.shape]
    dtype = data.dtype
    vc_util.check_shape(shape)
    vc_util.ops_dtype_check(dtype, vc_util.DtypeForDavinci.ALL_TYPES)
    vc_util.check_int_list(multiples, "multiples")
    output = akg.topi.tile(data, multiples)
    return output
