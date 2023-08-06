# Copyright 2011-2017 Ryan Curtin (http://www.ratml.org/)
# Copyright 2017 National ICT Australia (NICTA)
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

def test_fn_min_weird_operation():
  a = mat(10, 10)
  b = mat(25, 10)
  a.randn()
  b.randn()

  output = a * b.t()

  mval = output.min()
  other_mval = (a * b.t()).min()

  assert math.isclose(mval, other_mval) == True
    



  # def test_fn_min_weird_sparse_operation():
  #     sp_a = pa.mat(10, 10);
  #   sp_b = pa.mat(25, 10);
  #   a.sprandn(10, 10, 0.3);
  #   b.sprandn(25, 10, 0.3);

  #   sp_o = pa.matutput = a * b.t();

      
  #   mval = output.min(real_min);
  #   other_mval = (a * b.t()).min(operation_min);

  #   assert real_min == operation_min
  #   assert math.isclose(mval, other_mval) == True;
  



# def test_fn_min_sp_subview_test():
#     # We will assume subview.at() works and returns points within the bounds of
#   # the matrix, so we just have to ensure the results are the same as
#   # Mat.min()...
#   for (size_t r = 50; r < 150; ++r)
#         sp_x = pa.mat;
#     x.sprandn(r, r, 0.3);

                
#     mval = x.min(x_min);
#     mval1 = x[0:r - 1, 0:r - 1).min(x_subview_min1];
#     mval2 = x[:, 0:r - 1).min(x_subview_min2].
#     mval3 = x[0:r - 1).min(x_subview_min3, :].

#     if (mval != 0.0)
#             assert x_min == x_subview_min1
#       assert x_min == x_subview_min2
#       assert x_min == x_subview_min3

#       assert math.isclose(mval, mval1) == True;
#       assert math.isclose(mval, mval2) == True;
#       assert math.isclose(mval, mval3) == True;
      
    
  



# def test_fn_min_spsubview_col_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_vec x;
#     x.sprandn(r, 1, 0.3);

            
#     mval = x.min(x_min);
#     mval1 = x[0:r - 1, 0:0).min(x_subview_min1];
#     mval2 = x[0:r - 1).min(x_subview_min2, :].

#     if (mval != 0.0)
#             assert x_min == x_subview_min1
#       assert x_min == x_subview_min2

#       assert math.isclose(mval, mval1) == True;
#       assert math.isclose(mval, mval2) == True;
      
    
  



# def test_fn_min_spsubview_row_min_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_rowvec x;
#     x.sprandn(1, r, 0.3);

            
#     mval = x.min(x_min);
#     mval1 = x[0:0, 0:r - 1).min(x_subview_min1];
#     mval2 = x[:, 0:r - 1).min(x_subview_min2].

#     if (mval != 0.0)
#             assert x_min == x_subview_min1
#       assert x_min == x_subview_min2

#       assert math.isclose(mval, mval1) == True;
#       assert math.isclose(mval, mval2) == True;
      
    
  



# def test_fn_min_spincompletesubview_min_test():
#     for (size_t r = 50; r < 150; ++r)
#         sp_x = pa.mat;
#     x.sprandn(r, r, 0.3);

                
#     mval = x.min(x_min);
#     mval1 = x[1:r - 2, 1:r - 2).min(x_subview_min1];
#     mval2 = x[:, 1:r - 2).min(x_subview_min2].
#     mval3 = x[1:r - 2).min(x_subview_min3, :].

#         x.min(row, col);

#     if (row != 0 && row != r - 1 && col != 0 && col != r - 1 && mval != 0.0)
            
#       srow = x_subview_min1 % (r - 2);
#       scol = x_subview_min1 / (r - 2);
#       assert x_min == (srow + 1) + r * (scol + 1)
#       assert x_min == x_subview_min2 + r

#       srow = x_subview_min3 % (r - 2);
#       scol = x_subview_min3 / (r - 2);
#       assert x_min == (srow + 1) + r * scol

#       assert math.isclose(mval, mval1) == True;
#       assert math.isclose(mval, mval2) == True;
#       assert math.isclose(mval, mval3) == True;
      
    
  



# def test_fn_min_spincompletesubview_col_min_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_vec x;
#     x.sprandu(r, 1, 0.3);

            
#     mval = x.min(x_min);
#     mval1 = x[1:r - 2, 0:0).min(x_subview_min1];
#     mval2 = x[1:r - 2).min(x_subview_min2, :].

#     if (x_min != 0 && x_min != r - 1 && mval != 0.0)
#             assert x_min == x_subview_min1 + 1
#       assert x_min == x_subview_min2 + 1

#       assert math.isclose(mval, mval1) == True;
#       assert math.isclose(mval, mval2) == True;
      
    
  



# def test_fn_min_spincompletesubview_row_min_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_rowvec x;
#     x.sprandn(1, r, 0.3);

            
#     mval = x.min(x_min);
#     mval1 = x[0:0, 1:r - 2).min(x_subview_min1];
#     mval2 = x[:, 1:r - 2).min(x_subview_min2].

#     if (mval != 0.0 && x_min != 0 && x_min != r - 1)
#             assert x_min == x_subview_min1 + 1
#       assert x_min == x_subview_min2 + 1

#       assert math.isclose(mval, mval1) == True;
#       assert math.isclose(mval, mval2) == True;
      
    
  



# def test_fn_min_sp_cx_subview_min_test():
#     # We will assume subview.at() works and returns points within the bounds of
#   # the matrix, so we just have to ensure the results are the same as
#   # Mat.min()...
#   for (size_t r = 50; r < 150; ++r)
#         sp_cx_x = pa.mat;
#     x.sprandn(r, r, 0.3);

                
#     const std::complex<double> mval = x.min(x_min);
#     const std::complex<double> mval1 = x[0:r - 1, 0:r - 1).min(x_subview_min1];
#     const std::complex<double> mval2 = x[:, 0:r - 1).min(x_subview_min2].
#     const std::complex<double> mval3 = x[0:r - 1).min(x_subview_min3, :].

#     if (mval != std::complex<double>(0.0))
#             assert x_min == x_subview_min1
#       assert x_min == x_subview_min2
#       assert x_min == x_subview_min3

#       assert math.isclose(mval.real(), mval1.real()) == True;
#       assert math.isclose(mval.imag(), mval1.imag()) == True;
#       assert math.isclose(mval.real(), mval2.real()) == True;
#       assert math.isclose(mval.imag(), mval2.imag()) == True;
#       assert math.isclose(mval.real(), mval3.real()) == True;
#       assert math.isclose(mval.imag(), mval3.imag()) == True;
      
    
  



# def test_fn_min_sp_cx_subview_col_min_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_cx_vec x;
#     x.sprandn(r, 1, 0.3);

            
#     const std::complex<double> mval = x.min(x_min);
#     const std::complex<double> mval1 = x[0:r - 1, 0:0).min(x_subview_min1];
#     const std::complex<double> mval2 = x[0:r - 1).min(x_subview_min2, :].

#     if (mval != std::complex<double>(0.0))
#             assert x_min == x_subview_min1
#       assert x_min == x_subview_min2

#       assert math.isclose(mval.real(), mval1.real()) == True;
#       assert math.isclose(mval.imag(), mval1.imag()) == True;
#       assert math.isclose(mval.real(), mval2.real()) == True;
#       assert math.isclose(mval.imag(), mval2.imag()) == True;
      
    
  



# def test_fn_min_sp_cx_subview_row_min_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_cx_rowvec x;
#     x.sprandn(1, r, 0.3);

            
#     const std::complex<double> mval = x.min(x_min);
#     const std::complex<double> mval1 = x[0:0, 0:r - 1).min(x_subview_min1];
#     const std::complex<double> mval2 = x[:, 0:r - 1).min(x_subview_min2].

#     if (mval != std::complex<double>(0.0))
#             assert x_min == x_subview_min1
#       assert x_min == x_subview_min2

#       assert math.isclose(mval.real(), mval1.real()) == True;
#       assert math.isclose(mval.imag(), mval1.imag()) == True;
#       assert math.isclose(mval.real(), mval2.real()) == True;
#       assert math.isclose(mval.imag(), mval2.imag()) == True;
      
    
  



# def test_fn_min_sp_cx_incomplete_subview_min_test():
#     for (size_t r = 50; r < 150; ++r)
#         sp_cx_x = pa.mat;
#     x.sprandn(r, r, 0.3);

                
#     const std::complex<double> mval = x.min(x_min);
#     const std::complex<double> mval1 = x[1:r - 2, 1:r - 2).min(x_subview_min1];
#     const std::complex<double> mval2 = x[:, 1:r - 2).min(x_subview_min2].
#     const std::complex<double> mval3 = x[1:r - 2).min(x_subview_min3, :].

#         x.min(row, col);

#     if (row != 0 && row != r - 1 && col != 0 && col != r - 1 && mval != std::complex<double>(0.0))
            
#       srow = x_subview_min1 % (r - 2);
#       scol = x_subview_min1 / (r - 2);
#       assert x_min == (srow + 1) + r * (scol + 1)
#       assert x_min == x_subview_min2 + r

#       srow = x_subview_min3 % (r - 2);
#       scol = x_subview_min3 / (r - 2);
#       assert x_min == (srow + 1) + r * scol

#       assert math.isclose(mval.real(), mval1.real()) == True;
#       assert math.isclose(mval.imag(), mval1.imag()) == True;
#       assert math.isclose(mval.real(), mval2.real()) == True;
#       assert math.isclose(mval.imag(), mval2.imag()) == True;
#       assert math.isclose(mval.real(), mval3.real()) == True;
#       assert math.isclose(mval.imag(), mval3.imag()) == True;
      
    
  



# def test_fn_min_sp_cx_incomplete_subview_col_min_test():
#     for (size_t r = 10; r < 50; ++r)
#         arma::sp_cx_vec x;
#     x.sprandn(r, 1, 0.3);

            
#     const std::complex<double> mval = x.min(x_min);
#     const std::complex<double> mval1 = x[1:r - 2, 0:0).min(x_subview_min1];
#     const std::complex<double> mval2 = x[1:r - 2).min(x_subview_min2, :].

#     if (x_min != 0 && x_min != r - 1 && mval != std::complex<double>(0.0))
#             assert x_min == x_subview_min1 + 1
#       assert x_min == x_subview_min2 + 1

#       assert math.isclose(mval.real(), mval1.real()) == True;
#       assert math.isclose(mval.imag(), mval1.imag()) == True;
#       assert math.isclose(mval.real(), mval2.real()) == True;
#       assert math.isclose(mval.imag(), mval2.imag()) == True;
      
    
  



# def test_fn_min_sp_cx_incomplete_subview_row_min_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_cx_rowvec x;
#     x.sprandn(1, r, 0.3);

            
#     const std::complex<double> mval = x.min(x_min);
#     const std::complex<double> mval1 = x[0:0, 1:r - 2).min(x_subview_min1];
#     const std::complex<double> mval2 = x[:, 1:r - 2).min(x_subview_min2].

#     if (x_min != 0 && x_min != r - 1 && mval != std::complex<double>(0.0))
#             assert x_min == x_subview_min1 + 1
#       assert x_min == x_subview_min2 + 1

#       assert math.isclose(mval.real(), mval1.real()) == True;
#       assert math.isclose(mval.imag(), mval1.imag()) == True;
#       assert math.isclose(mval.real(), mval2.real()) == True;
#       assert math.isclose(mval.imag(), mval2.imag()) == True;
      
    
  
