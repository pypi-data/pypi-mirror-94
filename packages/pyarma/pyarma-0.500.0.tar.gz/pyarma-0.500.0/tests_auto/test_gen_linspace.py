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

def test_gen_linspace_1():
  a = pa.linspace(1,5,5)
  
  assert math.isclose(a[0], 1.0) == True
  assert math.isclose(a[1], 2.0) == True
  assert math.isclose(a[2], 3.0) == True
  assert math.isclose(a[3], 4.0) == True
  assert math.isclose(a[4], 5.0) == True
  
  b = pa.linspace(1,5,6)
  
  assert math.isclose(b[0], 1.0) == True
  assert math.isclose(b[1], 1.8) == True
  assert math.isclose(b[2], 2.6) == True
  assert math.isclose(b[3], 3.4) == True
  assert math.isclose(b[4], 4.2) == True
  assert math.isclose(b[5], 5.0) == True
  
  c = pa.linspace(1,5,6)
  
  assert math.isclose(c[0], 1.0) == True
  assert math.isclose(c[1], 1.8) == True
  assert math.isclose(c[2], 2.6) == True
  assert math.isclose(c[3], 3.4) == True
  assert math.isclose(c[4], 4.2) == True
  assert math.isclose(c[5], 5.0) == True
  
  X = pa.linspace(1,5,6)
  
  assert X.n_rows == 6
  assert X.n_cols == 1
