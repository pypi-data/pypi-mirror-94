# Copyright 2011-2017 Ryan Curtin (http://www.ratml.org/)
# Copyright 2017 National ICT Australia (NICTA)
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

class Test_Max():
  def test_fn_max_subview_test(self):
    # We will assume subview.at() works and returns points within the bounds of
    # the matrix, so we just have to ensure the results are the same as
    # Mat.max()...
    for r in range(50, 150):
      x = mat()
      x.randu(r, r)

      mval = x.max()
      mval1 = x[0:(r-1), 0:(r-1)].max()
      mval2 = x[:, 0:(r-1)].max()
      mval3 = x[0:r-1, :].max()

      assert math.isclose(mval, mval1, abs_tol=0.001) == True
      assert math.isclose(mval, mval2, abs_tol=0.001) == True
      assert math.isclose(mval, mval3, abs_tol=0.001) == True
      


  def test_fn_max_subview_col_test(self):
    for r in range(10, 50):
      x = mat()
      x.randu(r, 1)

      mval = x.max()
      mval1 = x[0:(r - 1), 0:0].max()
      mval2 = x[0:(r - 1), :].max()

      assert math.isclose(mval, mval1, abs_tol=0.001) == True
      assert math.isclose(mval, mval2, abs_tol=0.001) == True
      


  def test_fn_max_subview_row_test(self):
    for r in range(10,50):
      x = mat()
      x.randu(1, r)

      mval = x.max()
      mval1 = x[0:0, 0:(r - 1)].max()
      mval2 = x[:, 0:(r - 1)].max()

      assert math.isclose(mval, mval1, abs_tol=0.001) == True
      assert math.isclose(mval, mval2, abs_tol=0.001) == True
      


  # def test_fn_max_incomplete_subview_test(self):
  #   for r in range(50,150):
  #     x = mat()
  #     x.randu(r, r)

  #     mval = x.max()
  #     mval1 = x[1:(r - 2), 1:(r - 2)].max()
  #     mval2 = x[:, 1:(r - 2)].max()
  #     mval3 = x[1:(r - 2), :].max()

  #     assert math.isclose(mval, mval1, abs_tol=0.001) == True
  #     assert math.isclose(mval, mval2, abs_tol=0.001) == True
  #     assert math.isclose(mval, mval3, abs_tol=0.001) == True
            


  # def test_fn_max_incomplete_subview_col_test(self):
  #   for r in range(10,50):
  #     x = mat()
  #     x.randu(r, 1)

  #     mval = x.max()
  #     mval1 = x[1:(r - 2), 0:0].max()
  #     mval2 = x[1:(r - 2), :].max()

  #     assert math.isclose(mval, mval1, abs_tol=0.001) == True
  #     assert math.isclose(mval, mval2, abs_tol=0.001) == True
            


  def test_fn_max_cx_subview_row_test(self):
    for r in range(10,50):
      x = cx_mat()
      x.randu(1, r)

      mval = x.max()
      mval1 = x[0:0, 0:(r - 1)].max()
      mval2 = x[:, 0:(r - 1)].max()

      assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True
      assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True
      assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True
      assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True
      


  # def test_fn_max_cx_incomplete_subview_test(self):
  #   for r in range(50,150):
  #     x = cx_mat()
  #     x.randu(r, r)

  #     mval = x.max()
  #     mval1 = x[1:(r - 2), 1:(r - 2)].max()
  #     mval2 = x[:, 1:(r - 2)].max()
  #     mval3 = x[1:(r - 2), :].max()

  #     assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True
  #     assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True
  #     assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True
  #     assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True
  #     assert math.isclose(mval.real, mval3.real, abs_tol=0.001) == True
  #     assert math.isclose(mval.imag, mval3.imag, abs_tol=0.001) == True
          


  # def test_fn_max_cx_incomplete_subview_col_test(self):
  #   for r in range(10,50):
  #     x = cx_mat()
  #     x.randu(r, 1)

  #     mval = x.max()
  #     mval1 = x[1:(r - 2), 0:0].max()
  #     mval2 = x[1:(r - 2), :].max()

  #     assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True
  #     assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True
  #     assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True
  #     assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True
            


  # def test_fn_max_cx_incomplete_subview_row_test(self):
  #     for r in range(10,50):
  #       x = cx_mat()
  #       x.randu(1, r)

  #       mval = x.max()
  #       mval1 = x[0:0, 1:(r - 2)].max()
  #       mval2 = x[:, 1:(r - 2)].max()

  #       assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True
  #       assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True
  #       assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True
  #       assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True
              


  def test_fn_max_weird_operation_test(self):
    a = mat(10, 10)
    b = mat(25, 10)
    a.randn()
    b.randn()

    output = a * b.t()

    mval = output.max()
    other_mval = (a * b.t()).max()

    assert math.isclose(mval, other_mval, abs_tol=0.001) == True
    


# def test_fn_max_weird_sse_operation_test():
#     sp_a = mat(10, 10);
#   sp_b = mat(25, 10);
#   a.sprandn(10, 10, 0.3);
#   b.sprandn(25, 10, 0.3);

#   sp_o = matutput = a * b.t();

#   uword real_max;
#   uword operation_max;

#   mval = output.max(real_max);
#   other_mval = (a * b.t()).max(operation_max);

#   assert real_max == operation_max
#   assert math.isclose(mval, other_mval, abs_tol=0.001) == True;
  


# def test_fn_max_spsubview_test():
#     # We will assume subview.at() works and returns points within the bounds of
#   # the matrix, so we just have to ensure the results are the same as
#   # Mat.max()...
#   for (size_t r = 50; r < 150; ++r)
#         sp_x = mat;
#     x.sprandn(r, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;
#     uword x_subview_max3;

#     mval = x.max(x_max);
#     mval1 = x[0:r - 1, 0:r - 1).max(x_subview_max1];
#     mval2 = x[:, 0:r - 1).max(x_subview_max2].
#     mval3 = x[0:r - 1).max(x_subview_max3, :].

#     if (mval != 0.0)
#             assert x_max == x_subview_max1
#       assert x_max == x_subview_max2
#       assert x_max == x_subview_max3

#       assert math.isclose(mval, mval1, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval2, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval3, abs_tol=0.001) == True;
            


# def test_fn_max_spsubview_col_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_vec x;
#     x.sprandn(r, 1, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[0:r - 1, 0:0).max(x_subview_max1];
#     mval2 = x[0:r - 1).max(x_subview_max2, :].

#     if (mval != 0.0)
#             assert x_max == x_subview_max1
#       assert x_max == x_subview_max2

#       assert math.isclose(mval, mval1, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval2, abs_tol=0.001) == True;
            


# def test_fn_max_spsubview_row_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_rowvec x;
#     x.sprandn(1, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[0:0, 0:r - 1).max(x_subview_max1];
#     mval2 = x[:, 0:r - 1).max(x_subview_max2].

#     if (mval != 0.0)
#             assert x_max == x_subview_max1
#       assert x_max == x_subview_max2

#       assert math.isclose(mval, mval1, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval2, abs_tol=0.001) == True;
            


# def test_fn_max_spincompletesubview_test():
#     for (size_t r = 50; r < 150; ++r)
#         sp_x = mat;
#     x.sprandn(r, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;
#     uword x_subview_max3;

#     mval = x.max(x_max);
#     mval1 = x[1:r - 2, 1:r - 2).max(x_subview_max1];
#     mval2 = x[:, 1:r - 2).max(x_subview_max2].
#     mval3 = x[1:r - 2).max(x_subview_max3, :].

#     uword row, col;
#     x.max(row, col);

#     if (row != 0 && row != r - 1 && col != 0 && col != r - 1 && mval != 0.0)
#             uword srow, scol;

#       srow = x_subview_max1 % (r - 2);
#       scol = x_subview_max1 / (r - 2);
#       assert x_max == (srow + 1) + r * (scol + 1)
#       assert x_max == x_subview_max2 + r

#       srow = x_subview_max3 % (r - 2);
#       scol = x_subview_max3 / (r - 2);
#       assert x_max == (srow + 1) + r * scol

#       assert math.isclose(mval, mval1, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval2, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval3, abs_tol=0.001) == True;
            


# def test_fn_max_spincompletesubview_col_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_vec x;
#     x.sprandu(r, 1, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[1:r - 2, 0:0).max(x_subview_max1];
#     mval2 = x[1:r - 2).max(x_subview_max2, :].

#     if (x_max != 0 && x_max != r - 1 && mval != 0.0)
#             assert x_max == x_subview_max1 + 1
#       assert x_max == x_subview_max2 + 1

#       assert math.isclose(mval, mval1, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval2, abs_tol=0.001) == True;
            


# def test_fn_max_spincompletesubview_row_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_rowvec x;
#     x.sprandn(1, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[0:0, 1:r - 2).max(x_subview_max1];
#     mval2 = x[:, 1:r - 2).max(x_subview_max2].

#     if (mval != 0.0 && x_max != 0 && x_max != r - 1)
#             assert x_max == x_subview_max1 + 1
#       assert x_max == x_subview_max2 + 1

#       assert math.isclose(mval, mval1, abs_tol=0.001) == True;
#       assert math.isclose(mval, mval2, abs_tol=0.001) == True;
            


# def test_fn_max_cx_spsubview_test():
#     # We will assume subview.at() works and returns points within the bounds of
#   # the matrix, so we just have to ensure the results are the same as
#   # Mat.max()...
#   for (size_t r = 50; r < 150; ++r)
#         sp_cx_x = mat;
#     x.sprandn(r, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;
#     uword x_subview_max3;

#     mval = x.max(x_max);
#     mval1 = x[0:r - 1, 0:r - 1).max(x_subview_max1];
#     mval2 = x[:, 0:r - 1).max(x_subview_max2].
#     mval3 = x[0:r - 1).max(x_subview_max3, :].

#     if (mval != std::complex<double>(0.0))
#             assert x_max == x_subview_max1
#       assert x_max == x_subview_max2
#       assert x_max == x_subview_max3

#       assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval3.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval3.imag, abs_tol=0.001) == True;
            


# def test_fn_max_cx_spsubview_col_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_cx_vec x;
#     x.sprandn(r, 1, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[0:r - 1, 0:0).max(x_subview_max1];
#     mval2 = x[0:r - 1).max(x_subview_max2, :].

#     if (mval != std::complex<double>(0.0))
#             assert x_max == x_subview_max1
#       assert x_max == x_subview_max2

#       assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True;
            


# def test_fn_max_cx_spsubview_row_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_cx_rowvec x;
#     x.sprandn(1, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[0:0, 0:r - 1).max(x_subview_max1];
#     mval2 = x[:, 0:r - 1).max(x_subview_max2].

#     if (mval != std::complex<double>(0.0))
#             assert x_max == x_subview_max1
#       assert x_max == x_subview_max2

#       assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True;
            


# def test_fn_max_cx_spincompletesubview_test():
#     for (size_t r = 50; r < 150; ++r)
#         sp_cx_x = mat;
#     x.sprandn(r, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;
#     uword x_subview_max3;

#     mval = x.max(x_max);
#     mval1 = x[1:r - 2, 1:r - 2).max(x_subview_max1];
#     mval2 = x[:, 1:r - 2).max(x_subview_max2].
#     mval3 = x[1:r - 2).max(x_subview_max3, :].

#     uword row, col;
#     x.max(row, col);

#     if (row != 0 && row != r - 1 && col != 0 && col != r - 1 && mval != std::complex<double>(0.0))
#             uword srow, scol;

#       srow = x_subview_max1 % (r - 2);
#       scol = x_subview_max1 / (r - 2);
#       assert x_max == (srow + 1) + r * (scol + 1)
#       assert x_max == x_subview_max2 + r

#       srow = x_subview_max3 % (r - 2);
#       scol = x_subview_max3 / (r - 2);
#       assert x_max == (srow + 1) + r * scol

#       assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval3.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval3.imag, abs_tol=0.001) == True;
            


# def test_fn_max_cx_spincompletesubview_col_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_cx_vec x;
#     x.sprandn(r, 1, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[1:r - 2, 0:0).max(x_subview_max1];
#     mval2 = x[1:r - 2).max(x_subview_max2, :].

#     if (x_max != 0 && x_max != r - 1 && mval != std::complex<double>(0.0))
#             assert x_max == x_subview_max1 + 1
#       assert x_max == x_subview_max2 + 1

#       assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True;
            


# def test_fn_max_cx_spincompletesubview_row_test():
#     for (size_t r = 10; r < 50; ++r)
#         sp_cx_rowvec x;
#     x.sprandn(1, r, 0.3);

#     uword x_max;
#     uword x_subview_max1;
#     uword x_subview_max2;

#     mval = x.max(x_max);
#     mval1 = x[0:0, 1:r - 2).max(x_subview_max1];
#     mval2 = x[:, 1:r - 2).max(x_subview_max2].

#     if (x_max != 0 && x_max != r - 1 && mval != std::complex<double>(0.0))
#             assert x_max == x_subview_max1 + 1
#       assert x_max == x_subview_max2 + 1

#       assert math.isclose(mval.real, mval1.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval1.imag, abs_tol=0.001) == True;
#       assert math.isclose(mval.real, mval2.real, abs_tol=0.001) == True;
#       assert math.isclose(mval.imag, mval2.imag, abs_tol=0.001) == True;
            