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

def test_fn_cond_1():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    assert math.isclose(pa.cond(A), 1.7455, abs_tol=0.0001) == True
    assert math.isclose(pa.cond(A[:,:]), 1.7455, abs_tol=0.0001) == True

def test_fn_cond_2():

    A = pa.mat(5,6,pa.fill.zeros)

    assert math.isfinite(pa.cond(A)) == False