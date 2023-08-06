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

def test_fn_cumprod_1():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    B = pa.mat([
        [ -0.788380,  0.692980,  0.410840,  0.901420 ],
        [ -0.389026, -0.083296,  0.324510,  0.478870 ],
        [ -0.286218, -0.043401, -0.072246,  0.192329 ]
    ])

    C = pa.mat([
        [ -0.788380, -0.546332, -0.224455, -0.202328 ],
        [  0.493450, -0.059313, -0.046849, -0.024888 ],
        [  0.735730,  0.383345, -0.085344, -0.034277 ]
    ])

    assert math.isclose(pa.accu(pa.abs(pa.cumprod(A)   - B)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.cumprod(A,0) - B)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.cumprod(A,1) - C)), 0.0, abs_tol=0.0001) == True