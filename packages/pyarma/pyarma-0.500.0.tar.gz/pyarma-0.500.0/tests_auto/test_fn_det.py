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

def test_fn_det_1():

    A = pa.mat("\
    0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
    0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
    -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
    0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
    0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

    assert math.isclose(pa.det(A[0,0,pa.size(0,0)]), +1.0, abs_tol=0.0001) == True
    assert math.isclose(pa.det(A[0,0,pa.size(1,1)]), +0.0611980000000000, abs_tol=0.0001) == True
    assert math.isclose(pa.det(A[0,0,pa.size(2,2)]), -0.0847105222920000, abs_tol=0.0001) == True
    assert math.isclose(pa.det(A[0,0,pa.size(3,3)]), -0.0117387923199772, abs_tol=0.0001) == True
    assert math.isclose(pa.det(A[0,0,pa.size(4,4)]), +0.0126070917169865, abs_tol=0.0001) == True
    assert math.isclose(pa.det(A[0,0,pa.size(5,5)]), +0.0100409091117668, abs_tol=0.0001) == True

    with pytest.raises(RuntimeError):
        pa.det(A)

def test_fn_det_2():

    A = pa.toeplitz(pa.linspace(1,5,6))

    assert math.isclose(pa.det(A), -31.45728, abs_tol=0.0001) == True


    B = pa.mat(6, 6, pa.fill.zeros)
    B[pa.diag] = pa.linspace(1,5,6)

    assert math.isclose(pa.det(B), 334.152, abs_tol=0.0001) == True

    assert math.isclose(pa.det(pa.diagmat(B)), 334.152, abs_tol=0.0001) == True


    C = pa.mat(5, 6, pa.fill.randu)

    with pytest.raises(RuntimeError):
        pa.det(C)

    with pytest.raises(RuntimeError):
        pa.det(pa.diagmat(C))

# TODO: uses different form unavailable in PA
# def test_fn_det_3():

#     A = pa.toeplitz(pa.linspace(1,5,6))

#     val = float()
#     sign = float()

#     pa.log_det(val, sign, A)

#     assert math.isclose(pa.val, 3.44863, abs_tol=0.0001) == True
#     assert math.isclose(pa.sign, -1.0, abs_tol=0.0001) == True

#     assert math.isclose((pa.exp(val)*sign), pa.det(A), abs_tol=0.0001) == True

#     B = pa.mat(5,6, pa.fill.randu)

#     with pytest.raises(RuntimeError):
#         pa.log_det(val, sign, B)
