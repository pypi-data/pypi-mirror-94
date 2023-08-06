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

class Test_Gen_Ones:
  def test_gen_ones_1(self):
    
    A = pa.mat(5,6,pa.fill.ones)
    
    assert math.isclose( pa.accu(A), float(5*6) ) == True
    assert A.n_rows == 5 
    assert A.n_cols == 6 
    
    B = pa.mat(5,6,pa.fill.randu)
    
    B.ones()
    
    assert math.isclose(pa.accu(B), float(5*6) ) == True
    assert B.n_rows == 5 
    assert B.n_cols == 6
    
    C = pa.ones(5,6)
    
    assert math.isclose( pa.accu(C), float(5*6) ) == True
    assert C.n_rows == 5 
    assert C.n_cols == 6
    
    D = pa.ones(pa.size(5,6))
    
    assert math.isclose( pa.accu(D), float(5*6) ) == True
    assert D.n_rows == 5 
    assert D.n_cols == 6
    
    E = 2*pa.ones(5,6)
    
    assert math.isclose(pa.accu(E), float(2*5*6) ) == True
    assert E.n_rows == 5 
    assert E.n_cols == 6
    
  def test_gen_ones_2(self):
    
    A = pa.mat(5,6,pa.fill.zeros)
    
    A[:, 1].ones()
    
    assert math.isclose(pa.accu(A[:,0]), 0.0             ) == True
    assert math.isclose(pa.accu(A[:, 1]), float(A.n_rows)) == True
    assert math.isclose(pa.accu(A[:, 2]), 0.0             ) == True
    
    B = pa.mat(5,6,pa.fill.zeros)
    
    B[1, :].ones()
    
    assert math.isclose(pa.accu(B[0, :]), 0.0             ) == True
    assert math.isclose(pa.accu(B[1, :]), float(B.n_cols)) == True
    assert math.isclose(pa.accu(B[2, :]), 0.0            ) == True
    
    C = pa.mat(5,6,pa.fill.zeros)
    
    C[1:3,1:4].ones()
    
    assert math.isclose(pa.accu(C[pa.head_cols, 1]), 0.0) == True
    assert math.isclose(pa.accu(C[pa.head_rows, 1]), 0.0) == True
    
    assert math.isclose(pa.accu(C[pa.tail_cols,1]), 0.0) == True
    assert math.isclose(pa.accu(C[pa.tail_rows,1]), 0.0) == True
    
    assert math.isclose(pa.accu(C[1:3,1:4]), float(3*4)) == True

    D = pa.mat(5,6,pa.fill.zeros)
    
    D[pa.diag].ones()
    
    assert math.isclose(pa.accu(D[pa.diag]), float(5)) == True
    
  def test_gen_ones_3(self):
    
    A = pa.mat(5,6,pa.fill.zeros)
    
    indices = pa.umat([2, 4, 6])
    
    A[indices].ones()
    
    assert math.isclose(pa.accu(A), float(3)) == True
    
    assert math.isclose(A[0],          0.0) == True
    assert math.isclose(A[A.n_elem-1], 0.0) == True
    
    assert math.isclose(A[indices[0]], 1.0 ) == True
    assert math.isclose(A[indices[1]], 1.0 ) == True
    assert math.isclose(A[indices[2]], 1.0 ) == True

  def test_gen_ones_4(self):
    
    A = pa.cube(5,6,7,pa.fill.ones)
    
    assert math.isclose( pa.accu(A), float(5*6*7) ) == True
    assert A.n_rows == 5 
    assert A.n_cols == 6 
    assert A.n_slices == 7
    
    B = pa.cube(5,6,7,pa.fill.randu)
    
    B.ones()
    
    assert math.isclose(pa.accu(B), float(5*6*7) ) == True
    assert B.n_rows == 5 
    assert B.n_cols == 6
    assert B.n_slices == 7
    
    C = pa.ones(5,6,7)
    
    assert math.isclose( pa.accu(C), float(5*6*7) ) == True
    assert C.n_rows == 5 
    assert C.n_cols == 6
    assert C.n_slices == 7
    
    D = pa.ones(pa.size(5,6,7))
    
    assert math.isclose( pa.accu(D), float(5*6*7) ) == True
    assert D.n_rows == 5 
    assert D.n_cols == 6
    assert D.n_slices == 7
    
    E = 2*pa.ones(5,6,7)
    
    assert math.isclose(pa.accu(E), float(2*5*6*7) ) == True
    assert E.n_rows == 5 
    assert E.n_cols == 6
    assert E.n_slices == 7
