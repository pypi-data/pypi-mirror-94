# Copyright 2020-2021 Jason Rumengan, Terry Yue Zhuo
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

def test_fn_conv_to_1():

    A = pa.mat(5,6)
    A.fill(0.1)

    uA = pa.umat(A)
    iA = pa.imat(A)

    assert (uA.n_rows - A.n_rows) == 0
    assert (iA.n_rows - A.n_rows) == 0

    assert (uA.n_cols - A.n_cols) == 0
    assert (iA.n_cols - A.n_cols) == 0

    assert pa.any(pa.vectorise(uA)) == False
    assert pa.any(pa.vectorise(iA)) == False

def test_fn_conv_to_2():

    A = pa.mat(5,6); A.fill(1.0)

    uA = pa.umat(A)
    iA = pa.imat(A)

    assert pa.all(pa.vectorise(uA)) == True
    assert pa.all(pa.vectorise(iA)) == True

def test_fn_conv_to_4():

    A =   pa.linspace(1,5,6)
    pa.inplace_trans(A)
    B = 2*pa.linspace(1,5,6)
    C = pa.randu(5,6)

    assert math.isclose(pa.as_scalar(A * B), 130.40, abs_tol=0.0001) == True
