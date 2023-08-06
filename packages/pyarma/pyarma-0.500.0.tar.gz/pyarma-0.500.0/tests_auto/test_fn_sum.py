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

def test_fn_sum_1():

    a = pa.linspace(1,5,5)
    b = pa.linspace(1,5,6)

    assert math.isclose(pa.sum(a)[0], 15.0, abs_tol=0.0001) == True
    assert math.isclose(pa.sum(b)[0], 18.0, abs_tol=0.0001) == True

def test_fn_sum_2():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    colsums = pa.mat([ 0.44080, 1.09382, 0.97808, 1.83429 ])

    rowsums = pa.mat([
        [1.21686],
        [1.69436],
        [1.43577]
        ])

    assert math.isclose(pa.accu(pa.abs(colsums - pa.sum(A  ))), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(colsums - pa.sum(A,0))), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(rowsums - pa.sum(A,1))), 0.0, abs_tol=0.0001) == True

def test_fn_sum_3():

    AA = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    A = pa.cx_mat(AA, 0.5*AA)

    re_colsums = pa.mat([ 0.44080, 1.09382, 0.97808, 1.83429 ])

    cx_colsums = pa.cx_mat(re_colsums, 0.5*re_colsums)

    re_rowsums = pa.mat([
        [1.21686],
        [1.69436],
        [1.43577]
        ])

    cx_rowsums = pa.cx_mat(re_rowsums, 0.5*re_rowsums)

    assert math.isclose(pa.accu(pa.abs(cx_colsums - pa.sum(A  ))), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(cx_colsums - pa.sum(A,0))), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(cx_rowsums - pa.sum(A,1))), 0.0, abs_tol=0.0001) == True

def test_fn_sum_4():

    X = pa.mat(100,101, pa.fill.randu)

    assert math.isclose(pa.accu(pa.sum(pa.sum(X))/X.n_elem), 0.5, abs_tol=0.02*0.5) == True
    assert math.isclose(pa.accu(pa.sum(X[:,:])/X.n_elem), 0.5,  abs_tol=0.02*0.5) == True
