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


from pyarma import *
import pytest
import math

class Test_Init_Misc:
  def test_init_misc_1(self):
    n_rows = 5
    n_cols = 6
    
    A = mat(5,6, fill.zeros)
    
    for row in range(n_rows):
      for col in range(n_cols):
        assert A[row,col] == 0
    
    B = mat(5,6, fill.ones)
    
    for row in range(n_rows):
      for col in range(n_cols):
        assert B[row,col] == 1
    
    C = mat(2,3)
    
    C[0,0] = 0
    C[1,0] = 1
    
    C[0,1] = 2
    C[1,1] = 3
    
    C[0,2] = 4
    C[1,2] = 5
    
    assert C[0,0] == 0
    assert C[1,0] == 1
    
    assert C[0,1] == 2
    assert C[1,1] == 3
    
    assert C[0,2] == 4
    assert C[1,2] == 5
    
    D = mat([[0, 2, 4],
            [1, 3, 5]])
    
    assert D[0,0] == 0
    assert D[1,0] == 1
    
    assert D[0,1] == 2
    assert D[1,1] == 3
    
    assert D[0,2] == 4
    assert D[1,2] == 5



  def test_init_misc_2(self):
    A = mat([
      [ -0.78838,  0.69298,  0.41084,  0.90142 ],
      [  0.49345, -0.12020,  0.78987,  0.53124 ],
      [  0.73573,  0.52104, -0.22263,  0.40163 ]
      ])
    
    B = mat("\
      -0.78838,  0.69298,  0.41084,  0.90142;\
      0.49345, -0.12020,  0.78987,  0.53124;\
      0.73573,  0.52104, -0.22263,  0.40163;\
      ")
    
    C = mat("\
      -0.78838  0.69298  0.41084  0.90142;\
      0.49345 -0.12020  0.78987  0.53124;\
      0.73573  0.52104 -0.22263  0.40163;\
      ")
    
    
    assert A.n_rows == 3
    assert A.n_cols == 4
    
    assert math.isclose(A[0,0], -0.78838) == True
    assert math.isclose(A[1,0],  0.49345) == True
    assert math.isclose(A[2,0],  0.73573) == True
    assert math.isclose(A[0,1],  0.69298) == True
    assert math.isclose(A[1,1], -0.12020) == True
    assert math.isclose(A[2,1],  0.52104) == True
    assert math.isclose(A[0,2],  0.41084) == True
    assert math.isclose(A[1,2],  0.78987) == True
    assert math.isclose(A[2,2], -0.22263) == True
    assert math.isclose(A[0,3],  0.90142) == True
    assert math.isclose(A[1,3],  0.53124) == True
    assert math.isclose(A[2,3],  0.40163) == True
    
    assert math.isclose(accu(abs(A-B)), 0.0) == True
    assert math.isclose(accu(abs(A-C)), 0.0) == True



  def test_init_misc_3(self):
    n_rows = 5
    n_cols = 6
    
    A = cx_mat(5,6, fill.zeros)
      
    for row in range(n_rows):
      for col in range(n_cols):
        assert A[row,col] == complex(0,0)
    
    B = cx_mat(5,6, fill.ones)
    
    for row in range(n_rows):
      for col in range(n_cols):
        assert B[row,col] == complex(1,0)
    
    C = cx_mat(2,3)
    
    C[0,0] = complex(0.0,  1.0)
    C[1,0] = complex(1.0,  2.0)
    
    C[0,1] = complex(3.0,  4.0)
    C[1,1] = complex(5.0,  6.0)
    
    C[0,2] = complex(7.0,  8.0)
    C[1,2] = complex(9.0, 10.0)
    
    assert C[0,0] == complex(0.0,  1.0)
    assert C[1,0] == complex(1.0,  2.0)
    
    assert C[0,1] == complex(3.0,  4.0)
    assert C[1,1] == complex(5.0,  6.0)
    
    assert C[0,2] == complex(7.0,  8.0)
    assert C[1,2] == complex(9.0, 10.0)
