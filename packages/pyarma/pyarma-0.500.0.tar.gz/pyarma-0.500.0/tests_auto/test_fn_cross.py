# Copyright 2020-2021 Terry Yue Zhuo
# Copyright 2020-2021 Data61/CSIRO

# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

import sys
import math
import pytest
import pyarma as pa

def test_fn_cross_1():

    a = pa.mat([ [0.1],  [2.3],  [4.5] ])
    b = pa.mat([ [6.7],  [8.9], [10.0] ])

    c = pa.mat([[-17.050], [29.150], [-14.520] ])

    assert math.isclose(pa.accu(pa.abs(pa.cross(a,b) - c)), 0.0, abs_tol=0.0001) == True

    x = pa.mat()

    with pytest.raises(RuntimeError):
        x = pa.cross(pa.mat(4,1,pa.fill.randu), pa.mat(4,1))