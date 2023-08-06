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

class Test_Gen_Zeros:
  def test_gen_zeros_1(self):
    
    A = pa.mat(5,6,pa.fill.zeros)

    assert math.isclose(pa.accu(A) , 0.0) == True
    assert A.n_rows == 5
    assert A.n_cols == 6

    B = pa.mat(5,6,pa.fill.randu)

    B.zeros()

    assert math.isclose(pa.accu(B) , 0.0) == True
    assert B.n_rows == 5
    assert B.n_cols == 6

    C = pa.zeros(5,6)

    assert math.isclose(pa.accu(C) , 0.0) == True
    assert C.n_rows == 5
    assert C.n_cols == 6

    D = pa.zeros(pa.size(5,6))

    assert math.isclose(pa.accu(D) , 0.0) == True
    assert D.n_rows == 5
    assert D.n_cols == 6

    E = 2*pa.zeros(5,6)

    assert math.isclose(pa.accu(E) , 0.0) == True
    assert E.n_rows == 5
    assert E.n_cols == 6
    



  def test_gen_zeros_2(self):
    
    A = pa.mat(5,6,pa.fill.ones)

    A[:, 1].zeros()

    assert math.isclose(pa.accu(A[:, 0]), float(A.n_rows)) == True
    assert math.isclose(pa.accu(A[:, 1]), 0.0) == True
    assert math.isclose(pa.accu(A[:, 2]), float(A.n_rows)) == True

    B = pa.mat(5,6,pa.fill.ones)

    B[1, :].zeros()

    assert math.isclose(pa.accu(B[0, :]), float(B.n_cols)) == True
    assert math.isclose(pa.accu(B[1, :]), 0.0) == True
    assert math.isclose(pa.accu(B[2, :]), float(B.n_cols)) == True

    C = pa.mat(5,6,pa.fill.ones)

    C[1:3,1:4].zeros()

    assert math.isclose(pa.accu(C[pa.head_cols, 1]), float(5)) == True
    assert math.isclose(pa.accu(C[pa.head_rows, 1]), float(6)) == True

    assert math.isclose(pa.accu(C[pa.tail_cols, 1]), float(5)) == True
    assert math.isclose(pa.accu(C[pa.tail_rows, 1]), float(6)) == True

    assert math.isclose(pa.accu(C[1:3,1:4]), 0.0) == True

    D = pa.mat(5,6,pa.fill.ones)

    D[pa.diag].zeros()

    assert math.isclose(pa.accu(D[pa.diag]), 0.0) == True
    



  def test_gen_zeros_3(self):
    
    A = pa.mat(5,6,pa.fill.ones)

    indices = pa.umat([2, 4, 6])

    A[indices].zeros()

    assert math.isclose(pa.accu(A), float(5*6-3)) == True

    assert math.isclose(A[0]         , 1.0) == True
    assert math.isclose(A[A.n_elem-1], 1.0) == True

    assert math.isclose(A[indices[0]], 0.0) == True
    assert math.isclose(A[indices[1]], 0.0) == True
    assert math.isclose(A[indices[2]], 0.0) == True


  def test_gen_zeros_4(self):
    
    A = pa.cube(5,6,7,pa.fill.zeros)

    assert math.isclose(pa.accu(A) , 0.0) == True
    assert A.n_rows == 5
    assert A.n_cols == 6
    assert A.n_slices == 7

    B = pa.cube(5,6,7,pa.fill.randu)

    B.zeros()

    assert math.isclose(pa.accu(B) , 0.0) == True
    assert B.n_rows == 5
    assert B.n_cols == 6
    assert B.n_slices == 7

    C = pa.zeros(5,6,7)

    assert math.isclose(pa.accu(C) , 0.0) == True
    assert C.n_rows == 5
    assert C.n_cols == 6
    assert C.n_slices == 7

    D = pa.zeros(pa.size(5,6,7))

    assert math.isclose(pa.accu(D) , 0.0) == True
    assert D.n_rows == 5
    assert D.n_cols == 6
    assert D.n_slices == 7

    E = 2*pa.zeros(5,6,7)

    assert math.isclose(pa.accu(E) , 0.0) == True
    assert E.n_rows == 5
    assert E.n_cols == 6
    assert E.n_slices == 7
  # def test_gen_zeros_sp_mat():
    
  #   SpMat<unsigned int> e(2, 2)

  #   e(0, 0) = 3.1
  #   e(1, 1) = 2.2

  #   e *= zeros<SpMat<unsigned int> >(2, 2)

  #   assert e.n_nonzero == 0
  #   assert (unsigned int) e(0, 0) == 0
  #   assert (unsigned int) e(1, 0) == 0
  #   assert (unsigned int) e(0, 1) == 0
  #   assert (unsigned int) e(1, 1) == 0

  #   # Just test compilation here.
  #   e = zeros<SpMat<unsigned int> >(5, 5)
  #   e *= zeros<SpMat<unsigned int> >(5, 5)
  #   e %= zeros<SpMat<unsigned int> >(5, 5)
