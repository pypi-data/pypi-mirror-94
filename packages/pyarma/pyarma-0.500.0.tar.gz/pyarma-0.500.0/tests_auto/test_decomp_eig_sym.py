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

def test_decomp_eig_sym_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
    ")

    A = A*A.t()

    eigvals1 = pa.mat([
        [0.0044188],
        [0.0697266],
        [0.3364172],
        [0.8192910],
        [1.1872184]
    ])

    eigvals2 = pa.eig_sym(A)[0]

    eigvals3 = pa.mat()
    status = pa.eig_sym(eigvals3, A)

    eigvals4 = pa.mat()
    eigvecs4 = pa.mat()
    pa.eig_sym(eigvals4, eigvecs4, A)

    B = eigvecs4 * pa.diagmat(eigvals4) * eigvecs4.t()

    assert status == True
    # Orginal Epsilon is set to sys.float_info.epsilon
    assert math.isclose(pa.accu(pa.abs(eigvals2 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals3 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals4 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A - B)), 0.0, abs_tol=0.0001) == True

def test_decomp_eig_sym_2():

    A = pa.cx_mat([
        [ complex( 0.111205, +0.074101), complex(-0.225872, -0.068474), complex(-0.192660, +0.236887), complex( 0.355204, -0.355735) ],
        [ complex( 0.119869, +0.217667), complex(-0.412722, +0.366157), complex( 0.069916, -0.222238), complex( 0.234987, -0.072355) ],
        [ complex( 0.003791, +0.183253), complex(-0.212887, -0.172758), complex( 0.168689, -0.393418), complex( 0.008795, -0.289654) ],
        [ complex(-0.331639, -0.166660), complex( 0.436969, -0.313498), complex(-0.431574, +0.017421), complex(-0.104165, +0.145246) ]
    ])

    A = A*A.t()

    eigvals1 = pa.mat([
        [0.030904],
        [0.253778],
        [0.432459],
        [1.204726]
    ])

    eigvals2 = pa.eig_sym(A)[0]

    eigvals3 = pa.mat()
    status = pa.eig_sym(eigvals3, A)

    eigvals4 = pa.mat()
    eigvecs4 = pa.cx_mat()
    pa.eig_sym(eigvals4, eigvecs4, A)

    B = eigvecs4 * pa.diagmat(pa.cx_mat(eigvals4)) * eigvecs4.t()

    assert status == True
    # Orginal Epsilon is set to sys.float_info.epsilon
    assert math.isclose(pa.accu(pa.abs(eigvals2 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals3 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals4 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A - B)), 0.0, abs_tol=0.0001) == True

def test_decomp_eig_sym_3():

    A = pa.mat(5, 6, pa.fill.randu)

    eigvals = pa.mat()
    eigvecs = pa.mat()

    with pytest.raises(RuntimeError):
        pa.eig_sym(eigvals, eigvecs, A)