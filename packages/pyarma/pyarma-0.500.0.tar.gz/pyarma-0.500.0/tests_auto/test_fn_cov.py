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

def test_fn_cov_1():

    a = pa.linspace(1,5,6)
    b = 0.5*pa.linspace(1,5,6)
    c = pa.flipud(b)

    assert math.isclose(pa.as_scalar(pa.cov(a,b) - (+1.12)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.as_scalar(pa.cov(a,c) - (-1.12)), 0.0, abs_tol=0.0001) == True

def test_fn_cov_2():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    B = 0.5 * A

    C = pa.fliplr(B)

    AA = pa.mat("\
     1.00000  -0.54561  -0.28838  -0.99459;\
    -0.54561   1.00000  -0.64509   0.45559;\
    -0.28838  -0.64509   1.00000   0.38630;\
    -0.99459   0.45559   0.38630   1.00000;\
    ")

    AB = pa.mat("\
     1.00000  -0.54561  -0.28838  -0.99459;\
    -0.54561   1.00000  -0.64509   0.45559;\
    -0.28838  -0.64509   1.00000   0.38630;\
    -0.99459   0.45559   0.38630   1.00000;\
    ")

    AC = pa.mat("\
    -0.99459  -0.28838  -0.54561   1.00000;\
     0.45559  -0.64509   1.00000  -0.54561;\
     0.38630   1.00000  -0.64509  -0.28838;\
     1.00000   0.38630   0.45559  -0.99459;\
    ")

    assert math.isclose(pa.accu(pa.abs(pa.cor(A)   - AA)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.cor(A,B) - AA)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.cor(A,C) - AC)), 0.0, abs_tol=0.0001) == True