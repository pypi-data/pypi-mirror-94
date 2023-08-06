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

import pytest
import pyarma as pa

def test_mat_attributes():

    A = pa.mat(5,6, pa.fill.zeros)
    A[0,0] = 1.0
    A[A.n_rows-1,A.n_cols-1] = 1.0
    assert A.n_rows == 5
    assert A.n_cols == 6
    assert A.n_elem == 30
    assert len(pa.nonzeros(A)) == 2
    assert all(isinstance(a, float) for a in iter(A))

def test_cx_mat_attributes():

    A = pa.cx_mat(5,6, pa.fill.zeros)
    A[0,0] = 1+1j
    A[A.n_rows-1,A.n_cols-1] = 1+1j
    assert A.n_rows == 5
    assert A.n_cols == 6
    assert A.n_elem == 30
    assert len(pa.nonzeros(A)) == 2
    assert all(isinstance(a, complex) for a in iter(A))

def test_umat_attributes():

    A = pa.umat(5,6, pa.fill.zeros)
    A[0,0] = 1
    A[A.n_rows-1,A.n_cols-1] = 1
    assert A.n_rows == 5
    assert A.n_cols == 6
    assert A.n_elem == 30
    assert len(pa.nonzeros(A)) == 2
    assert all(isinstance(a, int) for a in iter(A))

def test_cube_attributes():
    D = pa.cube(5,6,2)
    assert D.n_rows   == 5
    assert D.n_cols   == 6
    assert D.n_slices == 2
    assert D.n_elem   == 60

