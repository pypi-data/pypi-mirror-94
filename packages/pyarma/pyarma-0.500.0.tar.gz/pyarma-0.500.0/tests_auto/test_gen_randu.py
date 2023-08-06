# Copyright 2015 Conrad Sanderson (http://conradsanderson.id.au)
# Copyright 2015 National ICT Australia (NICTA)
# Copyright 2020-2021 Jason Rumengan
# Copyright 2020-2021 Data61/CSIRO
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

import pytest
import pyarma as pa
import math

class Test_Gen_Randu:
  def test_gen_randu_1(self):
    
    n_rows = 100
    n_cols = 101

    A = pa.mat(n_rows,n_cols, pa.fill.randu)

    B = pa.mat(n_rows,n_cols) 
    
    B.randu()

    C = pa.mat()

    C.randu(n_rows,n_cols)

    D = pa.randu(n_rows, n_cols)

    E = pa.randu(pa.size(n_rows, n_cols))

    assert math.isclose((pa.accu(A)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(B)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(C)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(D)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(E)/A.n_elem), 0.5, abs_tol=0.02) == True

    assert math.isclose((pa.as_scalar(pa.mean(pa.vectorise(A)))), 0.5, abs_tol=0.02) == True
    
  def test_gen_randu_2(self):
    
    A = pa.mat(50,60,pa.fill.zeros)

    A[1:48,1:58].randu()

    assert math.isclose(pa.accu(A[pa.head_cols, 1]), 0.0) == True
    assert math.isclose(pa.accu(A[pa.head_rows, 1]), 0.0) == True

    assert math.isclose(pa.accu(A[pa.tail_cols, 1]), 0.0) == True
    assert math.isclose(pa.accu(A[pa.tail_rows, 1]), 0.0) == True

    assert math.isclose(pa.as_scalar(pa.mean(pa.vectorise(A[1:48,1:58]))), float(0.5), abs_tol=0.02) == True

  def test_gen_randu_3(self):

    A = pa.randu()

    assert isinstance(A, float)


  def test_gen_randu_4(self):

    n_elem = 100

    A = pa.randu(n_elem)

    assert A.is_colvec() == True

    assert math.isclose(((pa.accu(A))/A.n_elem), 0.5, abs_tol=0.05) == True

    assert math.isclose((pa.as_scalar(pa.mean(pa.vectorise(A)))), 0.5, abs_tol=0.05) == True

  def test_gen_randu_5(self):
    
    n_rows = 100
    n_cols = 101
    n_slices = 102

    A = pa.cube(n_rows,n_cols,n_slices, pa.fill.randu)

    B = pa.cube(n_rows,n_cols,n_slices) 
    
    B.randu()

    C = pa.cube()

    C.randu(n_rows,n_cols,n_slices)

    D = pa.randu(n_rows, n_cols, n_slices)

    E = pa.randu(pa.size(n_rows, n_cols, n_slices))

    assert math.isclose((pa.accu(A)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(B)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(C)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(D)/A.n_elem), 0.5, abs_tol=0.02) == True
    assert math.isclose((pa.accu(E)/A.n_elem), 0.5, abs_tol=0.02) == True

    assert math.isclose((pa.as_scalar(pa.mean(pa.vectorise(A)))), 0.5, abs_tol=0.02) == True