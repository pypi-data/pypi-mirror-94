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

def test_fn_cumsum_1():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    B = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [ -0.29493,  0.57278,  1.20071,  1.43266 ],
        [  0.44080,  1.09382,  0.97808,  1.83429 ]
    ])

    C = pa.mat([
        [-0.78838, -0.09540,  0.31544,  1.21686 ],
        [ 0.49345,  0.37325,  1.16312,  1.69436 ],
        [ 0.73573,  1.25677,  1.03414,  1.43577 ]
    ])

    assert math.isclose(pa.accu(pa.abs(pa.cumsum(A)   - B)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.cumsum(A,0) - B)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.cumsum(A,1) - C)), 0.0, abs_tol=0.0001) == True