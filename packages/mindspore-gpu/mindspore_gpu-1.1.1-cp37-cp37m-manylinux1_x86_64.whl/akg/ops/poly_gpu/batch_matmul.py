# Copyright 2020-2021 Huawei Technologies Co., Ltd
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

"""batch matmul"""
import akg
from akg.topi.cuda import schedule_batch_matmul
from akg.ops.math_gpu import tensorcore_batch_matmul
from akg.ops.math_gpu import batch_matmul


@akg.schedule(schedule_batch_matmul)
def batch_matmul_manual(x, y, bias, layout1="NHDT", layout2="NHDT", layout_out="NHDT"):
    """BatchMatmul with manual schedule."""
    return batch_matmul.batch_matmul(x, y, bias, layout1, layout2, layout_out)

def batch_matmul_auto(x, y, bias, out_dtype="float32", layout1="NHDT", layout2="NHDT", layout_out="NHDT", tensor_core=True, add_bias=False):
    """BatchMatmul with auto poly."""
    if add_bias == False:
        bias = None
    if tensor_core == True:
        return tensorcore_batch_matmul.batch_matmul(x, y, bias, out_dtype, layout1, layout2, layout_out)
    else:
        return batch_matmul.batch_matmul(x, y, bias, out_dtype, layout1, layout2, layout_out)
