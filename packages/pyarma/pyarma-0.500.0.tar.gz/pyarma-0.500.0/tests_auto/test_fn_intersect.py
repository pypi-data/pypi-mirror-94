# Copyright 2015 Conrad Sanderson (http://conradsanderson.id.au)
# Copyright 2015 National ICT Australia (NICTA)
# Copyright 2020-2021 Jason Rumengan
# Copyright 2020-2021 Data61/CSIRO
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

from pyarma import *
import pytest
import math

class Test_Intersect:
  def test_fn_intersect_1(self):
    A = regspace(5, 1)  # 5, 4, 3, 2, 1
    B = regspace(3, 7)  # 3, 4, 5, 6, 7
    
    C = intersect(A,B)       # 3, 4, 5
    
    assert C[0] == 3
    assert C[1] == 4
    assert C[2] == 5
    
    assert accu(C) == 12
    
    CC = mat()
    iA = umat()
    iB = umat()
    
    intersect(CC, iA, iB, A, B)
    
    assert accu(abs(C-CC)) == 0
    
    assert iA[0] == 2
    assert iA[1] == 1
    assert iA[2] == 0
    
    assert accu(iA) == 3
    
    assert iB[0] == 0
    assert iB[1] == 1
    assert iB[2] == 2
    
    assert accu(iB) == 3


  def test_fn_intersect_2(self):
    A = regspace(5, 1).t()  # 5, 4, 3, 2, 1
    B = regspace(3, 7).t()  # 3, 4, 5, 6, 7
    
    C = intersect(A,B)       # 3, 4, 5
    
    assert C[0] == 3
    assert C[1] == 4
    assert C[2] == 5
    
    assert accu(C) == 12
    
    CC = mat()
    iA = umat()
    iB = umat()
    
    intersect(CC, iA, iB, A, B)
    
    assert accu(abs(C-CC)) == 0
    
    assert iA[0] == 2
    assert iA[1] == 1
    assert iA[2] == 0
    
    assert accu(iA) == 3
    
    assert iB[0] == 0
    assert iB[1] == 1
    assert iB[2] == 2
    
    assert accu(iB) == 3
