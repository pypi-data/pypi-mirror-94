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

def test_fn_conj_1():

    re =  pa.linspace(1,5,6)
    im = 2*pa.linspace(1,5,6)

    a = pa.cx_mat(re,im)
    b = pa.conj(a)

    assert math.isclose(pa.accu(pa.abs(pa.real(b) - ( re))), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.imag(b) - (-im))), 0.0, abs_tol=0.0001) == True

def test_fn_conj_2():

    A = pa.cx_mat(5,6,pa.fill.randu)

    B = pa.conj(A)

    assert pa.all(pa.vectorise(pa.real(B) ==  pa.real(A)))[0] == True
    assert pa.all(pa.vectorise(pa.imag(B) == -pa.imag(A)))[0] == True