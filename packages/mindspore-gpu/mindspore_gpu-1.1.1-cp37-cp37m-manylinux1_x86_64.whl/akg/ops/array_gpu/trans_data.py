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

"""operator dsl function: trans data"""
import akg.tvm
import akg.topi
from akg.utils import validation_check as vc_util

@vc_util.check_input_type(akg.tvm.tensor.Tensor, (list, tuple))
def trans_data(data, axes):
    """
    Permute the dimensions of the input data.

    Args:
        data (tvm.tensor.Tensor): Tensor.
        axes (Union[list, tuple]): Elements must be int. The index of each dimensions.

    Returns:
        tvm.tensor.Tensor, has the same dtype as data.
    """
    vc_util.check_shape(data.shape)
    vc_util.check_int_list(axes, "axes")
    output = akg.topi.transpose(data, axes)
    return output