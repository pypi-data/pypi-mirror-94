# Copyright 2021 Terry Yue Zhuo
# Copyright 2021 Data61/CSIRO

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

def test_fn_hess_non_square():

    A = pa.mat(5, 6, pa.fill.ones)
    U, H = pa.mat(), pa.mat()

    with pytest.raises(RuntimeError):
        pa.hess(U, H, A)

#*****************  tests for real matrix  ****************

def test_fn_hess_empty():

    A = pa.mat(1, 1)
    A.reset()
    U, H, H1, H2 = pa.mat(), pa.mat(), pa.mat(), pa.mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert U.is_empty() == True
    assert H.is_empty() == True
    assert H1.is_empty() == True
    assert H2.is_empty() == True

def test_fn_hess_1():

    A = pa.mat(1, 1)
    A[0, 0] = 0.061198
    U, H, H1, H2 = pa.mat(), pa.mat(), pa.mat(), pa.mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert math.isclose(U[0, 0], 1.0, abs_tol=0.0001) == True
    assert math.isclose(H[0, 0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 0], 0.061198, abs_tol=0.0001) == True

def test_fn_hess_2():

    A = pa.mat("\
            0.061198   0.201990;\
            0.437242   0.058956;\
        ")
    U, H, H1, H2 = pa.mat(), pa.mat(), pa.mat(), pa.mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert math.isclose(U[0, 0], 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1], 1.0, abs_tol=0.0001) == True

    assert math.isclose(H[0, 0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(H[1, 0], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1], 0.058956, abs_tol=0.0001) == True

    assert math.isclose(H1[0, 0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 0], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1], 0.058956, abs_tol=0.0001) == True

    assert math.isclose(H2[0, 0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 0], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1], 0.058956, abs_tol=0.0001) == True

def test_fn_hess_3():

    A = pa.mat("\
            0.061198   0.201990   0.019678;\
            0.437242   0.058956  -0.149362;\
            -0.492474  -0.031309   0.314156;\
        ")
    U, H, H1, H2 = pa.mat(), pa.mat(), pa.mat(), pa.mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert math.isclose(U[0, 0], 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 2], 0.0, abs_tol=0.0001) == True

    assert math.isclose(U[1, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1], -0.663928864062532, abs_tol=0.0001) == True
    assert math.isclose(U[1, 2], 0.747795736457915, abs_tol=0.0001) == True

    assert math.isclose(U[2, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[2, 1], 0.747795736457915, abs_tol=0.0001) == True
    assert math.isclose(U[2, 2], 0.663928864062532, abs_tol=0.0001) == True


    assert math.isclose(H[0, 0], 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1], -0.119391866749972, abs_tol=0.0001) == True
    assert math.isclose(H[0, 2], 0.164112052994157, abs_tol=0.0001) == True

    assert math.isclose(H[1, 0], -0.658567541896805, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1], 0.291363559380149, abs_tol=0.0001) == True
    assert math.isclose(H[1, 2], 0.175033560375766, abs_tol=0.0001) == True

    assert math.isclose(H[2, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 1], 0.056980560375766, abs_tol=0.0001) == True
    assert math.isclose(H[2, 2], 0.081748440619851, abs_tol=0.0001) == True


    assert math.isclose(H1[0, 0], 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1], -0.119391866749972, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 2], 0.164112052994157, abs_tol=0.0001) == True

    assert math.isclose(H1[1, 0], -0.658567541896805, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1], 0.291363559380149, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 2], 0.175033560375766, abs_tol=0.0001) == True

    assert math.isclose(H1[2, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 1], 0.056980560375766, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 2], 0.081748440619851, abs_tol=0.0001) == True

def test_fn_hess_4():

    A = pa.mat("\
            0.061198   0.201990   0.019678  -0.493936;\
            0.437242   0.058956  -0.149362  -0.045465;\
            -0.492474  -0.031309   0.314156   0.419733;\
            0.336352   0.411541   0.458476  -0.393139;\
        ")
    U, H, H1, H2 = pa.mat(), pa.mat(), pa.mat(), pa.mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert math.isclose(U[0, 0], 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 2], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 3], 0.0, abs_tol=0.0001) == True

    assert math.isclose(U[1, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1], -0.591275924818639, abs_tol=0.0001) == True
    assert math.isclose(U[1, 2], -0.462981984254642, abs_tol=0.0001) == True
    assert math.isclose(U[1, 3], 0.660333599770220, abs_tol=0.0001) == True

    assert math.isclose(U[2, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[2, 1], 0.665965345962041, abs_tol=0.0001) == True
    assert math.isclose(U[2, 2], 0.181491258046004, abs_tol=0.0001) == True
    assert math.isclose(U[2, 3], 0.723568297557693, abs_tol=0.0001) == True

    assert math.isclose(U[3, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[3, 1], -0.454843861899358, abs_tol=0.0001) == True
    assert math.isclose(U[3, 2], 0.867587808529208, abs_tol=0.0001) == True
    assert math.isclose(U[3, 3], 0.201018545870685, abs_tol=0.0001) == True


    assert math.isclose(H[0, 0], 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1], 0.118336799794845, abs_tol=0.0001) == True
    assert math.isclose(H[0, 2], -0.518479197817449, abs_tol=0.0001) == True
    assert math.isclose(H[0, 3], 0.048328864303744, abs_tol=0.0001) == True

    assert math.isclose(H[1, 0], -0.739488928344434, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1], -0.017815019577445, abs_tol=0.0001) == True
    assert math.isclose(H[1, 2], 0.549585804168668, abs_tol=0.0001) == True
    assert math.isclose(H[1, 3], 0.001541438669749, abs_tol=0.0001) == True

    assert math.isclose(H[2, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 1], 0.268224897826587, abs_tol=0.0001) == True
    assert math.isclose(H[2, 2], -0.266514530817371, abs_tol=0.0001) == True
    assert math.isclose(H[2, 3], 0.544078897369960, abs_tol=0.0001) == True

    assert math.isclose(H[3, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[3, 1], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[3, 2], 0.163125252889179, abs_tol=0.0001) == True
    assert math.isclose(H[3, 3], 0.264302550394816, abs_tol=0.0001) == True


    assert math.isclose(H1[0, 0], 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1], 0.118336799794845, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 2], -0.518479197817449, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 3], 0.048328864303744, abs_tol=0.0001) == True

    assert math.isclose(H1[1, 0], -0.739488928344434, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1], -0.017815019577445, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 2], 0.549585804168668, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 3], 0.001541438669749, abs_tol=0.0001) == True

    assert math.isclose(H1[2, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 1], 0.268224897826587, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 2], -0.266514530817371, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 3], 0.544078897369960, abs_tol=0.0001) == True

    assert math.isclose(H1[3, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 1], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 2], 0.163125252889179, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 3], 0.264302550394816, abs_tol=0.0001) == True


    assert math.isclose(H2[0, 0], 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1], 0.118336799794845, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 2], -0.518479197817449, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 3], 0.048328864303744, abs_tol=0.0001) == True

    assert math.isclose(H2[1, 0], -0.739488928344434, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1], -0.017815019577445, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 2], 0.549585804168668, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 3], 0.001541438669749, abs_tol=0.0001) == True

    assert math.isclose(H2[2, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 1], 0.268224897826587, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 2], -0.266514530817371, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 3], 0.544078897369960, abs_tol=0.0001) == True

    assert math.isclose(H2[3, 0], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 1], 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 2], 0.163125252889179, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 3], 0.264302550394816, abs_tol=0.0001) == True

#*****************  tests for complex matrix  ****************

def test_fn_hess_cx_empty():

    A = pa.cx_mat(1, 1)
    A.reset()
    U, H, H1, H2 = pa.cx_mat(), pa.cx_mat(), pa.cx_mat(), pa.cx_mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert U.is_empty() == True
    assert H.is_empty() == True
    assert H1.is_empty() == True
    assert H2.is_empty() == True

def test_fn_hess_cx_1():

    A = pa.cx_mat(1, 1)
    A[0, 0] = complex(0.061198, 1.012234)
    U, H, H1, H2 = pa.cx_mat(), pa.cx_mat(), pa.cx_mat(), pa.cx_mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert math.isclose(U[0, 0].real, 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 0].imag, 0.0, abs_tol=0.0001) == True

    assert math.isclose(H[0, 0].real, 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H[0, 0].imag, 1.012234, abs_tol=0.0001) == True

    assert math.isclose(H1[0, 0].real, 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 0].imag, 1.012234, abs_tol=0.0001) == True

    assert math.isclose(H2[0, 0].real, 0.061198, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 0].imag, 1.012234, abs_tol=0.0001) == True

def test_fn_hess_cx_2():

    B = pa.mat("\
            0.061198   0.201990;\
            0.437242   0.058956;\
        ")
    A = pa.cx_mat(B, B*B)
    U, H, H1, H2 = pa.cx_mat(), pa.cx_mat(), pa.cx_mat(), pa.cx_mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert math.isclose(U[0, 0].real, 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1].real, 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1].imag, 0.0, abs_tol=0.0001) == True

    assert math.isclose(H[0, 0].real, 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H[0, 0].imag, 0.092063706784000, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1].real, 0.201990000000000, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1].imag, 0.024269906460000, abs_tol=0.0001) == True
    assert math.isclose(H[1, 0].real, 0.437242000000000, abs_tol=0.0001) == True
    assert math.isclose(H[1, 0].imag, 0.052536375268000, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1].real, 0.058956000000000, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1].imag, 0.091794321516000, abs_tol=0.0001) == True

    assert math.isclose(H1[0, 0].real, 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 0].imag, 0.092063706784000, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1].real, 0.201990000000000, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1].imag, 0.024269906460000, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 0].real, 0.437242000000000, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 0].imag, 0.052536375268000, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1].real, 0.058956000000000, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1].imag, 0.091794321516000, abs_tol=0.0001) == True

    assert math.isclose(H2[0, 0].real, 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 0].imag, 0.092063706784000, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1].real, 0.201990000000000, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1].imag, 0.024269906460000, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 0].real, 0.437242000000000, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 0].imag, 0.052536375268000, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1].real, 0.058956000000000, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1].imag, 0.091794321516000, abs_tol=0.0001) == True

def test_fn_hess_cx_3():

    B = pa.mat("\
            0.061198   0.201990   0.019678;\
            0.437242   0.058956  -0.149362;\
            -0.492474  -0.031309   0.314156;\
        ")
    A = pa.cx_mat(B, B*B)
    U, H, H1, H2 = pa.cx_mat(), pa.cx_mat(), pa.cx_mat(), pa.cx_mat()

    pa.hess(U, H, A)
    H1 = pa.hess(A)[1]
    pa.hess(H2, A)

    assert math.isclose(U[0, 0].real, 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 2].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 2].imag, 0.0, abs_tol=0.0001) == True

    assert math.isclose(U[1, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1].real, -0.625250908290361, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1].imag, -0.180311900237219, abs_tol=0.0001) == True
    assert math.isclose(U[1, 2].real, -0.694923841863332, abs_tol=0.0001) == True
    assert math.isclose(U[1, 2].imag, -0.305989827159056, abs_tol=0.0001) == True

    assert math.isclose(U[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[2, 1].real, 0.704232017531224, abs_tol=0.0001) == True
    assert math.isclose(U[2, 1].imag, 0.283912285396078, abs_tol=0.0001) == True
    assert math.isclose(U[2, 2].real, -0.565610163671470, abs_tol=0.0001) == True
    assert math.isclose(U[2, 2].imag, -0.321770449912063, abs_tol=0.0001) == True


    assert math.isclose(H[0, 0].real, 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H[0, 0].imag, 0.082372803412000, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1].real, -0.101702999021493, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1].imag, -0.061668749553784, abs_tol=0.0001) == True
    assert math.isclose(H[0, 2].real, -0.151590948501704, abs_tol=0.0001) == True
    assert math.isclose(H[0, 2].imag, -0.071689748472419, abs_tol=0.0001) == True

    assert math.isclose(H[1, 0].real, -0.699306461138236, abs_tol=0.0001) == True
    assert math.isclose(H[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1].real, 0.298129546829246, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1].imag, 0.178624769103627, abs_tol=0.0001) == True
    assert math.isclose(H[1, 2].real, -0.165941859233838, abs_tol=0.0001) == True
    assert math.isclose(H[1, 2].imag, 0.014927427092653, abs_tol=0.0001) == True

    assert math.isclose(H[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 1].real, -0.061767777059231, abs_tol=0.0001) == True
    assert math.isclose(H[2, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 2].real, 0.074982453170754, abs_tol=0.0001) == True
    assert math.isclose(H[2, 2].imag, 0.011525391092373, abs_tol=0.0001) == True


    assert math.isclose(H1[0, 0].real, 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 0].imag, 0.082372803412000, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1].real, -0.101702999021493, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1].imag, -0.061668749553784, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 2].real, -0.151590948501704, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 2].imag, -0.071689748472419, abs_tol=0.0001) == True

    assert math.isclose(H1[1, 0].real, -0.699306461138236, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1].real, 0.298129546829246, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1].imag, 0.178624769103627, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 2].real, -0.165941859233838, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 2].imag, 0.014927427092653, abs_tol=0.0001) == True

    assert math.isclose(H1[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 1].real, -0.061767777059231, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 2].real, 0.074982453170754, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 2].imag, 0.011525391092373, abs_tol=0.0001) == True


    assert math.isclose(H2[0, 0].real, 0.061198000000000, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 0].imag, 0.082372803412000, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1].real, -0.101702999021493, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1].imag, -0.061668749553784, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 2].real, -0.151590948501704, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 2].imag, -0.071689748472419, abs_tol=0.0001) == True

    assert math.isclose(H2[1, 0].real, -0.699306461138236, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1].real, 0.298129546829246, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1].imag, 0.178624769103627, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 2].real, -0.165941859233838, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 2].imag, 0.014927427092653, abs_tol=0.0001) == True

    assert math.isclose(H2[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 1].real, -0.061767777059231, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 2].real, 0.074982453170754, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 2].imag, 0.011525391092373, abs_tol=0.0001) == True

def test_fn_hess_cx_4():

    B = pa.mat("\
            0.061198   0.201990   0.019678  -0.493936;\
            0.437242   0.058956  -0.149362  -0.045465;\
            -0.492474  -0.031309   0.314156   0.419733;\
            0.336352   0.411541   0.458476  -0.393139;\
        ")
    A = pa.cx_mat(B, B*B)
    U, H, H1, H2 = pa.cx_mat(), pa.cx_mat(), pa.cx_mat(), pa.cx_mat()

    pa.hess(U, H, A*A)
    H1 = pa.hess(A*A)[1]
    pa.hess(H2, A*A)

    assert math.isclose(U[0, 0].real, 1.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 2].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 2].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 3].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[0, 3].imag, 0.0, abs_tol=0.0001) == True

    assert math.isclose(U[1, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1].real, -0.310409361344421, abs_tol=0.0001) == True
    assert math.isclose(U[1, 1].imag, 0.134965522927510, abs_tol=0.0001) == True
    assert math.isclose(U[1, 2].real, 0.368370931495079, abs_tol=0.0001) == True
    assert math.isclose(U[1, 2].imag, 0.620286967761253, abs_tol=0.0001) == True
    assert math.isclose(U[1, 3].real, -0.461565151978241, abs_tol=0.0001) == True
    assert math.isclose(U[1, 3].imag, 0.389788251419862, abs_tol=0.0001) == True

    assert math.isclose(U[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[2, 1].real, 0.090510343531288, abs_tol=0.0001) == True
    assert math.isclose(U[2, 1].imag, 0.435448214446087, abs_tol=0.0001) == True
    assert math.isclose(U[2, 2].real, -0.629572243863963, abs_tol=0.0001) == True
    assert math.isclose(U[2, 2].imag, 0.277252591049466, abs_tol=0.0001) == True
    assert math.isclose(U[2, 3].real, 0.331725833624923, abs_tol=0.0001) == True
    assert math.isclose(U[2, 3].imag, 0.467889401534022, abs_tol=0.0001) == True

    assert math.isclose(U[3, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[3, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(U[3, 1].real, 0.662749913792672, abs_tol=0.0001) == True
    assert math.isclose(U[3, 1].imag, -0.498383003349854, abs_tol=0.0001) == True
    assert math.isclose(U[3, 2].real, -0.073218600583049, abs_tol=0.0001) == True
    assert math.isclose(U[3, 2].imag, -0.030915392543373, abs_tol=0.0001) == True
    assert math.isclose(U[3, 3].real, -0.297561059397637, abs_tol=0.0001) == True
    assert math.isclose(U[3, 3].imag, 0.466387847936125, abs_tol=0.0001) == True


    assert math.isclose(H[0, 0].real, -0.059498334460944, abs_tol=0.0001) == True
    assert math.isclose(H[0, 0].imag, 0.187834910202221, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1].real, -0.017930467829804, abs_tol=0.0001) == True
    assert math.isclose(H[0, 1].imag, -0.366928547670200, abs_tol=0.0001) == True
    assert math.isclose(H[0, 2].real, -0.021913405453089, abs_tol=0.0001) == True
    assert math.isclose(H[0, 2].imag, -0.128142818524165, abs_tol=0.0001) == True
    assert math.isclose(H[0, 3].real, 0.012590549436907, abs_tol=0.0001) == True
    assert math.isclose(H[0, 3].imag, -0.036787529849029, abs_tol=0.0001) == True

    assert math.isclose(H[1, 0].real, -0.212856818153491, abs_tol=0.0001) == True
    assert math.isclose(H[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1].real, 0.173480548915683, abs_tol=0.0001) == True
    assert math.isclose(H[1, 1].imag, -0.119570582029397, abs_tol=0.0001) == True
    assert math.isclose(H[1, 2].real, -0.098222486822866, abs_tol=0.0001) == True
    assert math.isclose(H[1, 2].imag, -0.073492477972392, abs_tol=0.0001) == True
    assert math.isclose(H[1, 3].real, -0.088126641335837, abs_tol=0.0001) == True
    assert math.isclose(H[1, 3].imag, 0.107905518898551, abs_tol=0.0001) == True

    assert math.isclose(H[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 1].real, 0.125544511009417, abs_tol=0.0001) == True
    assert math.isclose(H[2, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[2, 2].real, 0.374057080595739, abs_tol=0.0001) == True
    assert math.isclose(H[2, 2].imag, 0.061223114296791, abs_tol=0.0001) == True
    assert math.isclose(H[2, 3].real, 0.231175819260595, abs_tol=0.0001) == True
    assert math.isclose(H[2, 3].imag, -0.224564151240434, abs_tol=0.0001) == True

    assert math.isclose(H[3, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[3, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[3, 1].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[3, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[3, 2].real, -0.238973358869022, abs_tol=0.0001) == True
    assert math.isclose(H[3, 2].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H[3, 3].real, -0.101771291133878, abs_tol=0.0001) == True
    assert math.isclose(H[3, 3].imag, 0.212030655387598, abs_tol=0.0001) == True


    assert math.isclose(H1[0, 0].real, -0.059498334460944, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 0].imag, 0.187834910202221, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1].real, -0.017930467829804, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 1].imag, -0.366928547670200, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 2].real, -0.021913405453089, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 2].imag, -0.128142818524165, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 3].real, 0.012590549436907, abs_tol=0.0001) == True
    assert math.isclose(H1[0, 3].imag, -0.036787529849029, abs_tol=0.0001) == True

    assert math.isclose(H1[1, 0].real, -0.212856818153491, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1].real, 0.173480548915683, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 1].imag, -0.119570582029397, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 2].real, -0.098222486822866, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 2].imag, -0.073492477972392, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 3].real, -0.088126641335837, abs_tol=0.0001) == True
    assert math.isclose(H1[1, 3].imag, 0.107905518898551, abs_tol=0.0001) == True

    assert math.isclose(H1[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 1].real, 0.125544511009417, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 2].real, 0.374057080595739, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 2].imag, 0.061223114296791, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 3].real, 0.231175819260595, abs_tol=0.0001) == True
    assert math.isclose(H1[2, 3].imag, -0.224564151240434, abs_tol=0.0001) == True

    assert math.isclose(H1[3, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 1].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 2].real, -0.238973358869022, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 2].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 3].real, -0.101771291133878, abs_tol=0.0001) == True
    assert math.isclose(H1[3, 3].imag, 0.212030655387598, abs_tol=0.0001) == True


    assert math.isclose(H2[0, 0].real, -0.059498334460944, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 0].imag, 0.187834910202221, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1].real, -0.017930467829804, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 1].imag, -0.366928547670200, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 2].real, -0.021913405453089, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 2].imag, -0.128142818524165, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 3].real, 0.012590549436907, abs_tol=0.0001) == True
    assert math.isclose(H2[0, 3].imag, -0.036787529849029, abs_tol=0.0001) == True

    assert math.isclose(H2[1, 0].real, -0.212856818153491, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1].real, 0.173480548915683, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 1].imag, -0.119570582029397, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 2].real, -0.098222486822866, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 2].imag, -0.073492477972392, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 3].real, -0.088126641335837, abs_tol=0.0001) == True
    assert math.isclose(H2[1, 3].imag, 0.107905518898551, abs_tol=0.0001) == True

    assert math.isclose(H2[2, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 1].real, 0.125544511009417, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 2].real, 0.374057080595739, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 2].imag, 0.061223114296791, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 3].real, 0.231175819260595, abs_tol=0.0001) == True
    assert math.isclose(H2[2, 3].imag, -0.224564151240434, abs_tol=0.0001) == True

    assert math.isclose(H2[3, 0].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 0].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 1].real, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 1].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 2].real, -0.238973358869022, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 2].imag, 0.0, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 3].real, -0.101771291133878, abs_tol=0.0001) == True
    assert math.isclose(H2[3, 3].imag, 0.212030655387598, abs_tol=0.0001) == True