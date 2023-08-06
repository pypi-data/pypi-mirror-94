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

def test_fn_all_1():

    A =  pa.mat(5, 6, pa.fill.zeros)
    B = pa.mat(5, 6, pa.fill.zeros)
    B[0,0] = 1.0
    C = pa.mat(5, 6, pa.fill.ones )

    assert pa.all(pa.vectorise(A))[0] == False
    assert pa.all(pa.vectorise(B))[0] == False
    assert pa.all(pa.vectorise(C))[0] == True 

    assert pa.all(pa.vectorise(A[:,:]))[0] == False
    assert pa.all(pa.vectorise(B[:,:]))[0] == False
    assert pa.all(pa.vectorise(C[:,:]))[0] == True 

    assert pa.all(pa.vectorise(  C -  C))[0] == False
    assert pa.all(pa.vectorise(2*C -2*C))[0] == False

    assert pa.all(pa.vectorise(C) < 0.5)[0] == False
    assert pa.all(pa.vectorise(C) > 0.5)[0] == True

def test_fn_all_2():

    A = pa.mat(5, 6, pa.fill.zeros)
    B = pa.mat(5, 6, pa.fill.zeros)
    B[0,0] = 1.0
    C = pa.mat(5, 6, pa.fill.ones )
    D = pa.mat(5, 6, pa.fill.ones )
    D[0,0] = 0.0

    assert pa.accu(pa.all(A)   == pa.umat([0, 0, 0, 0, 0, 0]) ) == 6
    assert pa.accu(pa.all(A,0) == pa.umat([0, 0, 0, 0, 0, 0]) ) == 6
    assert pa.accu(pa.all(A,1) == pa.umat   ([[0], [0], [0], [0], [0]]   ) ) == 5

    assert pa.accu(pa.all(B)   == pa.umat([0, 0, 0, 0, 0, 0]) ) == 6
    assert pa.accu(pa.all(B,0) == pa.umat([0, 0, 0, 0, 0, 0]) ) == 6
    assert pa.accu(pa.all(B,1) == pa.umat   ([[0], [0], [0], [0], [0]]   ) ) == 5

    assert pa.accu(pa.all(C)   == pa.umat([1, 1, 1, 1, 1, 1]) ) == 6
    assert pa.accu(pa.all(C,0) == pa.umat([1, 1, 1, 1, 1, 1]) ) == 6
    assert pa.accu(pa.all(C,1) == pa.umat   ([[1], [1], [1], [1], [1]]   ) ) == 5

    assert pa.accu(pa.all(D)   == pa.umat([0, 1, 1, 1, 1, 1]) ) == 6
    assert pa.accu(pa.all(D,0) == pa.umat([0, 1, 1, 1, 1, 1]) ) == 6
    assert pa.accu(pa.all(D,1) == pa.umat   ([[0], [1], [1], [1], [1]]   ) ) == 5