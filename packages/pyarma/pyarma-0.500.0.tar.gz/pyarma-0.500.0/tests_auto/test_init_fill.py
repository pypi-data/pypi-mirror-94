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

class Test_Init_Fill:
  def test_init_fill_1(self):
    Z = mat( 5,  6, fill.zeros)
    O = mat( 5,  6, fill.ones)
    I = mat( 5,  6, fill.eye)
    U = mat(50, 60, fill.randu)
    N = mat(50, 60, fill.randn)
    
    assert accu(Z != 0) == 0  
    assert accu(O != 0) == 5*6
    assert accu(I != 0) == 5  
    
    assert math.isclose(  as_scalar(mean(vectorise(U))), 0.500, abs_tol=0.05) == True
    assert math.isclose(as_scalar(stddev(vectorise(U))), 0.288, abs_tol=0.05) == True
    
    assert math.isclose(  as_scalar(mean(vectorise(N))), 0.0, abs_tol=0.05) == True
    assert math.isclose(as_scalar(stddev(vectorise(N))), 1.0, abs_tol=0.05) == True
    
    X = mat(5, 6, fill.none)   # only to test instantiation



  def test_init_fill_2(self):
    Z = cube( 5,  6, 2, fill.zeros)
    O = cube( 5,  6, 2, fill.ones)
    U = cube(50, 60, 2, fill.randu)
    N = cube(50, 60, 2, fill.randn)
    
    assert accu(Z != 0) == 0    
    assert accu(O != 0) == 5*6*2
    
    assert math.isclose(  as_scalar(mean(vectorise(U))), 0.500, abs_tol=0.05) == True
    assert math.isclose(as_scalar(stddev(vectorise(U))), 0.288, abs_tol=0.05) == True
    
    assert math.isclose(  as_scalar(mean(vectorise(N))), 0.0, abs_tol=0.05) == True
    assert math.isclose(as_scalar(stddev(vectorise(N))), 1.0, abs_tol=0.05) == True
    
    X = cube(5, 6, 2, fill.none)   # only to test instantiation
    
    with pytest.raises(TypeError):
      I = cube(5, 6, 2, fill.eye) 

