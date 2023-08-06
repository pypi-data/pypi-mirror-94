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

class Test_Instantiation:
  def test_instantiation_mat_1(self):
    n_rows = 5
    n_cols = 6
    
    A = pa.mat(n_rows,n_cols)
    fB = pa.fmat(n_rows,n_cols)
    uC = pa.umat(n_rows,n_cols)
    iD = pa.imat(n_rows,n_cols)
    
    cx_  = pa.cx_mat(n_rows,n_cols)
    cx_fF = pa.cx_fmat(n_rows,n_cols)
    

  def test_instantiation_cube_1(self):
    n_rows   = 5
    n_cols   = 6
    n_slices = 2
    
    A = pa.cube(n_rows,n_cols,n_slices)
    B = pa.fcube(n_rows,n_cols,n_slices)
    C = pa.ucube(n_rows,n_cols,n_slices)
    D = pa.icube(n_rows,n_cols,n_slices)
    
    E = pa.cx_cube(n_rows,n_cols,n_slices)
    F = pa.cx_fcube(n_rows,n_cols,n_slices)

