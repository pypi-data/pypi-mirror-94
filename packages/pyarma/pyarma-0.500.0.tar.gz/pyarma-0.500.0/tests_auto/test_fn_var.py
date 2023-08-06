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

def test_fn_var_empty():

    m = pa.mat(100,100,pa.fill.zeros)

    result = pa.var(m)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    result = pa.var(m, 0, 0)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    result = pa.var(m, 1, 0)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    result = pa.var(m, 1)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    colres = pa.var(m, 1, 1)

    assert colres.n_cols == 1
    assert colres.n_rows == 100

    for i in range(100):
        assert math.isclose(colres[i], 0.0) == True

    colres = pa.var(m, 0, 1)

    assert colres.n_cols == 1
    assert colres.n_rows == 100

    for i in range(100):
        assert math.isclose(colres[i], 0.0) == True

def test_fn_var_empty_cx():

    m = pa.cx_mat(100,100,pa.fill.zeros)

    result = pa.var(m)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    result = pa.var(m, 0, 0)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    result = pa.var(m, 1, 0)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    result = pa.var(m, 1)

    assert result.n_cols == 100
    assert result.n_rows == 1

    for i in range(100):
        assert math.isclose(result[i], 0.0) == True

    colres = pa.var(m, 1, 1)

    assert colres.n_cols == 1
    assert colres.n_rows == 100

    for i in range(100):
        assert math.isclose(colres[i], 0.0) == True

    colres = pa.var(m, 0, 1)

    assert colres.n_cols == 1
    assert colres.n_rows == 100

    for i in range(100):
        assert math.isclose(colres[i], 0.0) == True

    result = pa.var(m)
