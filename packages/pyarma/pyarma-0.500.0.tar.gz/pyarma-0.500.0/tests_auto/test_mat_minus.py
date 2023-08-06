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

import pyarma as pa
import pytest
import math


def test_mat_minus_1():
  A = pa.mat(
    "\
     0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
     0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
    -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
     0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
     0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")
  
  B = pa.fliplr(A)
  
  A_minus_B = pa.mat(
    "\
     0.0097900   0.3287350   0.5136140  -0.5136140  -0.3287350  -0.0097900;\
     0.4018050  -0.2371970  -0.1038970   0.1038970   0.2371970  -0.4018050;\
    -0.0379750  -0.0996260  -0.1055770   0.1055770   0.0996260   0.0379750;\
    -0.0374810   0.5465810   0.8516150  -0.8516150  -0.5465810   0.0374810;\
    -0.0191190  -0.0751450  -0.1159330   0.1159330   0.0751450   0.0191190;\
    ")
  
  neg_of_A_minus_B = pa.mat(
    "\
    -0.0097900  -0.3287350  -0.5136140  +0.5136140  +0.3287350  +0.0097900;\
    -0.4018050  +0.2371970  +0.1038970  -0.1038970  -0.2371970  +0.4018050;\
    +0.0379750  +0.0996260  +0.1055770  -0.1055770  -0.0996260  -0.0379750;\
    +0.0374810  -0.5465810  -0.8516150  +0.8516150  +0.5465810  -0.0374810;\
    +0.0191190  +0.0751450  +0.1159330  -0.1159330  -0.0751450  -0.0191190;\
    ")
  
  X = A - B
  
  assert math.isclose(X[0,0],  0.0097900) == True
  assert math.isclose(X[1,0],  0.4018050) == True
  assert math.isclose(X[2,0], -0.0379750) == True
  assert math.isclose(X[3,0], -0.0374810) == True
  assert math.isclose(X[4,0], -0.0191190) == True
  
  assert math.isclose(X[0,1],  0.3287350) == True
  assert math.isclose(X[1,1], -0.2371970) == True
  assert math.isclose(X[2,1], -0.0996260) == True
  assert math.isclose(X[3,1],  0.5465810) == True
  assert math.isclose(X[4,1], -0.0751450) == True
  
  assert math.isclose(X[0,5], -0.0097900) == True
  assert math.isclose(X[1,5], -0.4018050) == True
  assert math.isclose(X[2,5],  0.0379750) == True
  assert math.isclose(X[3,5],  0.0374810) == True
  assert math.isclose(X[4,5],  0.0191190) == True
  
  Y = pa.mat = (2*A - 2*B) / 2
  
  assert math.isclose(Y[0,0],  0.0097900) == True
  assert math.isclose(Y[1,0],  0.4018050) == True
  assert math.isclose(Y[2,0], -0.0379750) == True
  assert math.isclose(Y[3,0], -0.0374810) == True
  assert math.isclose(Y[4,0], -0.0191190) == True
  
  assert math.isclose(Y[0,1],  0.3287350) == True
  assert math.isclose(Y[1,1], -0.2371970) == True
  assert math.isclose(Y[2,1], -0.0996260) == True
  assert math.isclose(Y[3,1],  0.5465810) == True
  assert math.isclose(Y[4,1], -0.0751450) == True
  
  assert math.isclose(Y[0,5], -0.0097900) == True
  assert math.isclose(Y[1,5], -0.4018050) == True
  assert math.isclose(Y[2,5],  0.0379750) == True
  assert math.isclose(Y[3,5],  0.0374810) == True
  assert math.isclose(Y[4,5],  0.0191190) == True
  
  assert math.isclose(pa.accu(   (A-B) + neg_of_A_minus_B), 0.0, abs_tol=0.000000001) == True
  
  assert math.isclose(pa.accu(pa.abs( 2*(A-B) + 2*neg_of_A_minus_B )), 0.0, abs_tol=0.000000001) == True
