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


def test_mat_neg_1():
  A = mat(
    "\
     0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
     0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
    -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
     0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
     0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")
  
  B = mat(-A)
  
  assert math.isclose(B[0,0], -0.061198) == True
  assert math.isclose(B[1,0], -0.437242) == True
  assert math.isclose(B[2,0], +0.492474) == True
  assert math.isclose(B[3,0], -0.336352) == True
  assert math.isclose(B[4,0], -0.239585) == True
  
  assert math.isclose(B[0,1], -0.201990) == True
  assert math.isclose(B[1,1], -0.058956) == True
  assert math.isclose(B[2,1], +0.031309) == True
  assert math.isclose(B[3,1], -0.411541) == True
  assert math.isclose(B[4,1], +0.428913) == True
  
  assert math.isclose(B[0,5], -0.051408) == True
  assert math.isclose(B[1,5], -0.035437) == True
  assert math.isclose(B[2,5], +0.454499) == True
  assert math.isclose(B[3,5], -0.373833) == True
  assert math.isclose(B[4,5], -0.258704) == True
  
  assert math.isclose(accu(B + A), 0.0) == True
