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

"""HSwish"""
import akg.topi as topi
import akg.tvm as tvm
from akg.topi import tag
import akg


@tvm.tag_scope(tag=tag.ELEMWISE)
def topi_nn_HSwish(x):
    """
    topi HSwish
    Args:
        x:

    Returns:

    """
    return tvm.compute(x.shape, lambda *i: tvm.if_then_else(x(*i) <= -3, 0,
                                                            tvm.if_then_else(x(*i) >= 3, x(*i),
                                                                             x(*i) * (x(*i) + 3) / 6)))

@akg.schedule(topi.cuda.schedule_injective)
def HSwish(x):
    """
    HSwish
    Args:
        x:

    Returns:

    """
    return topi_nn_HSwish(x)
