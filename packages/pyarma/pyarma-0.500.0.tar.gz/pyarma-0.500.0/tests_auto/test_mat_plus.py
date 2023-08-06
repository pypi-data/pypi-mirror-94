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

class Test_Mat_Plus:
  def test_mat_plus_1(self):
    A = mat(
      "\
      0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
      0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
      -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
      0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
      0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
      ")
    
    B = fliplr(A)
    
    A_plus_B = mat(
      "\
      0.112606   0.075245  -0.474258  -0.474258   0.075245   0.112606;\
      0.472679   0.355109  -0.194827  -0.194827   0.355109   0.472679;\
      -0.946973   0.037008   0.733889   0.733889   0.037008  -0.946973;\
      0.710185   0.276501   0.065337   0.065337   0.276501   0.710185;\
      0.498289  -0.782681  -0.697973  -0.697973  -0.782681   0.498289;\
      ")
    
    X = A + B
    
    assert math.isclose(X[0,0],  0.112606) == True
    assert math.isclose(X[1,0],  0.472679) == True
    assert math.isclose(X[2,0], -0.946973) == True
    assert math.isclose(X[3,0],  0.710185) == True
    assert math.isclose(X[4,0],  0.498289) == True
    
    assert math.isclose(X[0,1],  0.075245) == True
    assert math.isclose(X[1,1],  0.355109) == True
    assert math.isclose(X[2,1],  0.037008) == True
    assert math.isclose(X[3,1],  0.276501) == True
    assert math.isclose(X[4,1], -0.782681) == True
    
    assert math.isclose(X[0,5],  0.112606) == True
    assert math.isclose(X[1,5],  0.472679) == True
    assert math.isclose(X[2,5], -0.946973) == True
    assert math.isclose(X[3,5],  0.710185) == True
    assert math.isclose(X[4,5],  0.498289) == True
    
    
    Y = (2*A + 2*B)/2
    
    assert math.isclose(Y[0,0],  0.112606) == True
    assert math.isclose(Y[1,0],  0.472679) == True
    assert math.isclose(Y[2,0], -0.946973) == True
    assert math.isclose(Y[3,0],  0.710185) == True
    assert math.isclose(Y[4,0],  0.498289) == True
    
    assert math.isclose(Y[0,1],  0.075245) == True
    assert math.isclose(Y[1,1],  0.355109) == True
    assert math.isclose(Y[2,1],  0.037008) == True
    assert math.isclose(Y[3,1],  0.276501) == True
    assert math.isclose(Y[4,1], -0.782681) == True
    
    assert math.isclose(Y[0,5],  0.112606) == True
    assert math.isclose(Y[1,5],  0.472679) == True
    assert math.isclose(Y[2,5], -0.946973) == True
    assert math.isclose(Y[3,5],  0.710185) == True
    assert math.isclose(Y[4,5],  0.498289) == True
    
    
    assert math.isclose(accu(abs( mat(A+B) - A_plus_B )), 0.0, abs_tol=0.00000001) == True
    assert math.isclose(accu(abs(    (A+B) - A_plus_B )), 0.0, abs_tol=0.00000001) == True
    
    assert math.isclose(accu(abs( 2*(A+B) - 2*A_plus_B )), 0.0, abs_tol=0.00000001) == True

  



  def test_mat_plus_2(self):
    A = mat(5,6); A.fill(1.0)
    B = mat(5,6); B.fill(2.0)
    C = mat(5,6); C.fill(3.0)
    
    assert math.isclose(accu(A + B), float(5*6*3)) == True
    
    assert math.isclose(accu(A + B + C), float(5*6*6)) == True
    
    assert math.isclose(accu(A + B/2 + C), float(5*6*5)) == True
    
    X = mat(6,5)
    with pytest.raises(RuntimeError):
      A+X   # adding non-conformant matrices will throw unless ARMA_NO_DEBUG is defined



