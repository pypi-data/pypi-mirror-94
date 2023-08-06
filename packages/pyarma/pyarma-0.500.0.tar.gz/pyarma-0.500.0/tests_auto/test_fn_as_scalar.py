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

def test_fn_as_scalar_1():

    A = pa.mat(1,1)
    A.fill(2.0)
    B = pa.mat(2,2)
    B.fill(2.0)

    assert math.isclose(pa.as_scalar(A), 2.0, abs_tol=0.0001) == True

    assert math.isclose(pa.as_scalar(2+A), 4.0, abs_tol=0.0001) == True

    assert math.isclose(pa.as_scalar(B[0:0, 0:0]), 2.0, abs_tol=0.0001) == True

    with pytest.raises(RuntimeError):
        pa.as_scalar(B)

def test_fn_as_scalar_2():

    r = pa.linspace(1,5,6)
    pa.inplace_trans(r)
    q = pa.linspace(1,5,6)
    X = 0.5*pa.toeplitz(q)

    assert math.isclose(pa.as_scalar(r*q), 65.2, abs_tol=0.0001) == True

    assert math.isclose(pa.as_scalar(r*X*q), 380.848, abs_tol=0.0001) == True

    assert math.isclose(pa.as_scalar(r*pa.diagmat(X)*q), 32.6, abs_tol=0.0001) == True
    assert math.isclose(pa.as_scalar(r*pa.inv(pa.diagmat(X))*q), 130.4, abs_tol=0.0001) == True

def test_fn_as_scalar_3():

    A = pa.cube(1,1,1)
    A.fill(2.0)
    B = pa.cube(2,2,2)
    B.fill(2.0)

    assert math.isclose(pa.as_scalar(A), 2.0, abs_tol=0.0001) == True

    assert math.isclose(pa.as_scalar(2+A), 4.0, abs_tol=0.0001) == True

    assert math.isclose(pa.as_scalar(B[0:0, 0:0, 0:0]), 2.0, abs_tol=0.0001) == True

    with pytest.raises(RuntimeError):
        pa.as_scalar(B)