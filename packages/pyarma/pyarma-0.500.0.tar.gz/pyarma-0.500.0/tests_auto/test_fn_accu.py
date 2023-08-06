# Copright 2020-2021 Terry Yue Zhuo
# Copright 2020-2021 Data61/CSIRO

# Licensed under the Apache License, Version 2.0 (the "License"
# ou ma not use this file except in compliance with the License.
# ou ma obtain a cop of the License at
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF AN KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

import sys
import math
import pytest
import pyarma as pa

def test_fn_accu_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

    assert math.isclose(pa.accu(A), 0.240136, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A)), 7.845382, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A-A), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A+A), 0.480272, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*A), 0.480272, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(-A), -0.240136, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*A+3*A), 1.200680, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.fliplr(A)), 0.240136, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.flipud(A)), 0.240136, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A[:,1]), 0.212265, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A[1,:]), 0.632961, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*A[:,1]), 0.424530, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*A[1,:]), 1.265922, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(A@A), 2.834218657806, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A*A.t()), 1.218704694166, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A.t()*A), 2.585464740700, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.vectorise(A)), 0.240136, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(A[1:3, 1:4]), 1.273017, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*A[1:3, 1:4]), 2.546034, abs_tol=0.0001) == True

    with pytest.raises(RuntimeError):
        pa.accu(A*A)

def test_fn_accu_2():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

    C = pa.cx_mat(A, 2*pa.fliplr(A))
    D = pa.cx_mat(2*pa.fliplr(A), A)

    # abs or pa.abs?
    assert math.isclose(abs(pa.accu(C) - complex(0.240136, +0.480272)), 0.0, abs_tol=0.0001) == True

    # abs or pa.abs?
    assert math.isclose(abs(pa.accu(complex(2,3)*C) - complex(-0.960544000000001, +1.680951999999999)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(abs(pa.accu(C*D.t() ) - complex(-0.710872588088, +3.656114082498002)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(abs(pa.accu(C*D.st()) - complex(0.0,             +6.093523470830000)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(abs(pa.accu(C.t() *D) - complex(10.341858962800, -7.756394222100000)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(abs(pa.accu(C.st()*D) - complex(0.0,             +1.29273237035e+01)), 0.0, abs_tol=0.0001) == True

    a =  pa.linspace(1,5,5)
    b =  pa.linspace(1,5,6)
    c = -pa.linspace(1,5,6)

    assert math.isclose(pa.accu(a), 15.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(b), 18.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(c), -18.0, abs_tol=0.0001) == True

def test_fn_accu_3():

    a =  pa.linspace(1,5,5)
    b =  pa.linspace(1,5,6)
    c = -pa.linspace(1,5,6)

    assert math.isclose(pa.accu(a), 15.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(b),  18.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(c), -18.0, abs_tol=0.0001) == True

def test_fn_accu_4():

    A = pa.mat(5,6)
    A.fill(2.0)
    B = pa.mat(5,6)
    B.fill(4.0)
    C = pa.mat(6,5)
    C.fill(6.0)

    assert math.isclose(pa.accu(A + B), (2+4)*(A.n_rows*A.n_cols), abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A[:,:] + B[:,:]), (2+4)*(A.n_rows*A.n_cols), abs_tol=0.0001) == True

    assert math.isclose(pa.accu(A @ B), (2*4)*(A.n_rows*A.n_cols), abs_tol=0.0001) == True
    assert math.isclose(pa.accu(A[:,:] @ B[:,:]), (2*4)*(A.n_rows*A.n_cols), abs_tol=0.0001) == True

    with pytest.raises(RuntimeError):
        pa.accu(A @ C)
    with pytest.raises(RuntimeError):
        pa.accu(A[:,:] @ C[:,:])

# def test_fn_accu_spmat():

    # b = pa.sp_mat(4, 4)
    # b[0, 1] = 6
    # b[1, 3] = 15
    # b[3, 1] = 14
    # b[2, 0] = 5
    # b[3, 3] = 12

    # assert pa.accu(b) == 52
    # assert pa.accu(b[1:3, 1:3)] == 41