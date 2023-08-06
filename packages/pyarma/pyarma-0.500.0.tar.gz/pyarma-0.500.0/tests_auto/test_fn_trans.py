# Copyright 2015 Conrad Sanderson (http://conradsanderson.id.au)
# Copyright 2015 National ICT Australia (NICTA)
#
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
import builtins

def test_fn_trans_1():
  A = mat(
    "\
     0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
     0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
    -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
     0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
     0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

  At = mat(
    "\
     0.061198   0.437242  -0.492474   0.336352   0.239585;\
     0.201990   0.058956  -0.031309   0.411541  -0.428913;\
     0.019678  -0.149362   0.314156   0.458476  -0.406953;\
    -0.493936  -0.045465   0.419733  -0.393139  -0.291020;\
    -0.126745   0.296153   0.068317  -0.135040  -0.353768;\
     0.051408   0.035437  -0.454499   0.373833   0.258704;\
    ")

  At_sum0 = mat([ -0.28641, 0.63296, -0.17608, 1.05202, -0.98237 ])

  At_sum1 = mat([
     [0.58190],
     [0.21227],
     [0.23599],
    [-0.80383],
    [-0.25108],
     [0.26488]
  ])


  A_col1_t = mat([ 0.201990, 0.058956, -0.031309, 0.411541, -0.428913 ])

  A_row1_t = mat([
     [0.437242],
     [0.058956],
    [-0.149362],
    [-0.045465],
     [0.296153],
     [0.035437]
  ])

  accu_A_col1_t = 0.21227
  accu_A_row1_t = 0.63296

  assert math.isclose(accu(abs(mat(A.t().t()) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(    A.t().t()  - A)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(mat(A.t()    ) - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(A.st()   ) - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(A.t()   ) - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat( trans(A)) - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(strans(A)) - At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(A.t()     - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(A.st()    - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(A.t()    - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs( trans(A) - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(strans(A) - At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(mat(At.t()    ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(At.st()   ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(At.t()   ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat( trans(At)) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(strans(At)) - A)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(At.t()     - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(At.st()    - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(At.t()    - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs( trans(At) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(strans(At) - A)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((0 + At.t()    ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs((0 + At.st()   ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs((0 + At.t()   ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs((0 +  trans(At)) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs((0 + strans(At)) - A)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(mat(0 + At.t()    ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(0 + At.st()   ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(0 + At.t()   ) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(0 +  trans(At)) - A)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(0 + strans(At)) - A)), 0.0, abs_tol=0.00001) == True


  assert math.isclose(accu(abs(2*A.t()    - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(2*trans(A) - 2*At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((2*A).t()  - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(trans(2*A) - 2*At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((A+A).t()  - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(trans(A+A) - 2*At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((A.t()    + At) - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs((trans(A) + At) - 2*At)), 0.0, abs_tol=0.00001) == True


  assert math.isclose(accu(abs(mat(2*A.t())    - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(2*trans(A)) - 2*At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(mat((2*A).t())  - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(trans(2*A)) - 2*At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(mat((A+A).t())  - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(trans(A+A)) - 2*At)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(mat(A.t()    + At) - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(trans(A) + At) - 2*At)), 0.0, abs_tol=0.00001) == True


  assert math.isclose(accu(abs(mat(A[:, 1].t()) - A_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(mat(A[1, :].t()) - A_row1_t)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(A[:, 1].t() - A_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(A[1, :].t() - A_row1_t)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(2*A[:, 1].t() - 2*A_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(2*A[1, :].t() - 2*A_row1_t)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs( (A[:, 1].t() + A_col1_t) - 2*A_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs( (A[1, :].t() + A_row1_t) - 2*A_row1_t)), 0.0, abs_tol=0.00001) == True


  assert math.isclose(builtins.abs( accu(A[:, 1].t()) - accu_A_col1_t ), 0.0, abs_tol=0.00001) == True
  assert math.isclose(builtins.abs( accu(A[1, :].t()) - accu_A_row1_t ), 0.0, abs_tol=0.00001) == True

  assert math.isclose(builtins.abs( accu(A[:, 1].t()) - accu(A[:, 1]) ), 0.0, abs_tol=0.00001) == True
  assert math.isclose(builtins.abs( accu(A[1, :].t()) - accu(A[1, :]) ), 0.0, abs_tol=0.00001) == True

  assert math.isclose(builtins.abs( as_scalar(sum(A[:, 1].t())) - accu_A_col1_t ), 0.0, abs_tol=0.00001) == True
  assert math.isclose(builtins.abs( as_scalar(sum(A[1, :].t())) - accu_A_row1_t ), 0.0, abs_tol=0.00001) == True

  with pytest.raises(RuntimeError):
    A + A.t()


def test_fn_trans_2():
  A = mat(
    "\
     0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
     0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
    -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
     0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
     0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

  C = cx_mat(A,fliplr(A))

  Ct = cx_mat([
    [ complex( 0.061198, -0.051408), complex( 0.437242, -0.035437), complex(-0.492474, +0.454499), complex( 0.336352, -0.373833), complex( 0.239585, -0.258704) ],
    [ complex( 0.201990, +0.126745), complex( 0.058956, -0.296153), complex(-0.031309, -0.068317), complex( 0.411541, +0.135040), complex(-0.428913, +0.353768) ],
    [ complex( 0.019678, +0.493936), complex(-0.149362, +0.045465), complex( 0.314156, -0.419733), complex( 0.458476, +0.393139), complex(-0.406953, +0.291020) ],
    [ complex(-0.493936, -0.019678), complex(-0.045465, +0.149362), complex( 0.419733, -0.314156), complex(-0.393139, -0.458476), complex(-0.291020, +0.406953) ],
    [ complex(-0.126745, -0.201990), complex( 0.296153, -0.058956), complex( 0.068317, +0.031309), complex(-0.135040, -0.411541), complex(-0.353768, +0.428913) ],
    [ complex( 0.051408, -0.061198), complex( 0.035437, -0.437242), complex(-0.454499, +0.492474), complex( 0.373833, -0.336352), complex( 0.258704, -0.239585) ]
  ])

  C_col1_t = cx_mat([ complex(0.201990, +0.126745), complex(0.058956, -0.296153), complex(-0.031309, -0.068317), complex(0.411541, +0.135040), complex(-0.428913, +0.353768) ])

  C_row1_t = cx_mat([
    [complex( 0.437242, -0.035437)],
    [complex( 0.058956, -0.296153)],
    [complex(-0.149362, +0.045465)],
    [complex(-0.045465, +0.149362)],
    [complex( 0.296153, -0.058956)],
    [complex( 0.035437, -0.437242)]
    ])


  assert math.isclose(accu(abs(C.t().t() - C)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat(C.t()   ) - Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(C.t()  ) - Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(trans(C)) - Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(C.t()    - Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(C.t()   - Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(trans(C) - Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat(Ct.t()   ) - C)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(Ct.t()  ) - C)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(trans(Ct)) - C)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(Ct.t()    - C)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Ct.t()   - C)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(trans(Ct) - C)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(2*C.t()    - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(2*trans(C) - 2*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((2*C).t()  - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(trans(2*C) - 2*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((C+C).t()  - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(trans(C+C) - 2*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(complex(2,3)*C.t()    - complex(2,3)*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(complex(2,3)*trans(C) - complex(2,3)*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat(2*C.t())    - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(2*trans(C)) - 2*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat((2*C).t())  - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(trans(2*C)) - 2*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat((C+C).t())  - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(trans(C+C)) - 2*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat(complex(2,3)*C.t())    - complex(2,3)*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(complex(2,3)*trans(C)) - complex(2,3)*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((C.t()    + Ct) - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs((trans(C) + Ct) - 2*Ct)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat(C[:, 1].t()) - C_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(C[1, :].t()) - C_row1_t)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(C[:, 1].t() - C_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(C[1, :].t() - C_row1_t)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(2*C[:, 1].t() - 2*C_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(2*C[1, :].t() - 2*C_row1_t)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs( (C[:, 1].t() + C_col1_t) - 2*C_col1_t)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs( (C[1, :].t() + C_row1_t) - 2*C_row1_t)), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat(C.st())    - conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(strans(C)) - conj(Ct))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(C.st()    - conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(strans(C) - conj(Ct))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(2*C.st()    - conj(2*Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(2*strans(C) - conj(2*Ct))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(complex(2,3)*C.st()    - complex(2,3)*conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(complex(2,3)*strans(C) - complex(2,3)*conj(Ct))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs((C.st()    + C.st()) - conj(2*Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs((strans(C) + C.st()) - conj(2*Ct))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(cx_mat(C[:, 1].st()) - conj(C_col1_t))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(cx_mat(C[1, :].st()) - conj(C_row1_t))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(C[:, 1].st() - conj(C_col1_t))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(C[1, :].st() - conj(C_row1_t))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs(2*C[:, 1].st() - conj(2*C_col1_t))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(2*C[1, :].st() - conj(2*C_row1_t))), 0.0, abs_tol=0.00001) == True

  assert math.isclose(accu(abs( (C[:, 1].st() + conj(C_col1_t)) - conj(2*C_col1_t))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs( (C[1, :].st() + conj(C_row1_t)) - conj(2*C_row1_t))), 0.0, abs_tol=0.00001) == True

  with pytest.raises(RuntimeError):
    C + C.t() 



def test_fn_trans_3():
  A = mat(
    "\
     0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
     0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
    -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
     0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
     0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

  At = mat(
    "\
     0.061198   0.437242  -0.492474   0.336352   0.239585;\
     0.201990   0.058956  -0.031309   0.411541  -0.428913;\
     0.019678  -0.149362   0.314156   0.458476  -0.406953;\
    -0.493936  -0.045465   0.419733  -0.393139  -0.291020;\
    -0.126745   0.296153   0.068317  -0.135040  -0.353768;\
     0.051408   0.035437  -0.454499   0.373833   0.258704;\
    ")

  B = mat(A[head_cols, 5])

  Bt = mat(At[head_rows, 5])

  X = mat()
  Y = mat()

  X = mat(A);  X = X.t()
  Y = mat(B);  Y = Y.t()

  assert math.isclose(accu(abs(X - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - Bt)), 0.0, abs_tol=0.00001) == True

  X = mat(A);  X = 0 + X.t()
  Y = mat(B);  Y = 0 + Y.t()

  assert math.isclose(accu(abs(X - At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - Bt)), 0.0, abs_tol=0.00001) == True

  X = mat(A);  X = 2*X.t()
  Y = mat(B);  Y = 2*Y.t()

  assert math.isclose(accu(abs(X - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Bt)), 0.0, abs_tol=0.00001) == True

  X = mat(A);  X = 0 + 2*X.t()
  Y = mat(B);  Y = 0 + 2*Y.t()

  assert math.isclose(accu(abs(X - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Bt)), 0.0, abs_tol=0.00001) == True

  X = mat(A);  X = (2*X).t()
  Y = mat(B);  Y = (2*Y).t()

  assert math.isclose(accu(abs(X - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Bt)), 0.0, abs_tol=0.00001) == True

  X = mat(A);  X = (X+X).t()
  Y = mat(B);  Y = (Y+Y).t()

  assert math.isclose(accu(abs(X - 2*At)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Bt)), 0.0, abs_tol=0.00001) == True



def test_fn_trans_4():
  A = mat(
    "\
     0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
     0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
    -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
     0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
     0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

  C = cx_mat(A,fliplr(A))

  Ct = cx_mat([
    [ complex( 0.061198, -0.051408), complex( 0.437242, -0.035437), complex(-0.492474, +0.454499), complex( 0.336352, -0.373833), complex( 0.239585, -0.258704) ],
    [ complex( 0.201990, +0.126745), complex( 0.058956, -0.296153), complex(-0.031309, -0.068317), complex( 0.411541, +0.135040), complex(-0.428913, +0.353768) ],
    [ complex( 0.019678, +0.493936), complex(-0.149362, +0.045465), complex( 0.314156, -0.419733), complex( 0.458476, +0.393139), complex(-0.406953, +0.291020) ],
    [ complex(-0.493936, -0.019678), complex(-0.045465, +0.149362), complex( 0.419733, -0.314156), complex(-0.393139, -0.458476), complex(-0.291020, +0.406953) ],
    [ complex(-0.126745, -0.201990), complex( 0.296153, -0.058956), complex( 0.068317, +0.031309), complex(-0.135040, -0.411541), complex(-0.353768, +0.428913) ],
    [ complex( 0.051408, -0.061198), complex( 0.035437, -0.437242), complex(-0.454499, +0.492474), complex( 0.373833, -0.336352), complex( 0.258704, -0.239585) ]
    ])

  D = cx_mat(C[head_cols, 5])

  Dt = cx_mat(Ct[head_rows, 5])

  X = cx_mat()
  Y = cx_mat()

  X = cx_mat(C);  X = X.t()
  Y = cx_mat(D);  Y = Y.t()

  assert math.isclose(accu(abs(X - Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - Dt)), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = 0 + X.t()
  Y = cx_mat(D);  Y = 0 + Y.t()

  assert math.isclose(accu(abs(X - Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - Dt)), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = 2*X.t()
  Y = cx_mat(D);  Y = 2*Y.t()

  assert math.isclose(accu(abs(X - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Dt)), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = 0 + 2*X.t()
  Y = cx_mat(D);  Y = 0 + 2*Y.t()

  assert math.isclose(accu(abs(X - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Dt)), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = (2*X).t()
  Y = cx_mat(D);  Y = (2*Y).t()

  assert math.isclose(accu(abs(X - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Dt)), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = (X+X).t()
  Y = cx_mat(D);  Y = (Y+Y).t()

  assert math.isclose(accu(abs(X - 2*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*Dt)), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = complex(2,3)*X.t()
  Y = cx_mat(D);  Y = complex(2,3)*Y.t()

  assert math.isclose(accu(abs(X - complex(2,3)*Ct)), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - complex(2,3)*Dt)), 0.0, abs_tol=0.00001) == True


  X = cx_mat(C);  X = X.st()
  Y = cx_mat(D);  Y = Y.st()

  assert math.isclose(accu(abs(X - conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - conj(Dt))), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = 0 + X.st()
  Y = cx_mat(D);  Y = 0 + Y.st()

  assert math.isclose(accu(abs(X - conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - conj(Dt))), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = 2*X.st()
  Y = cx_mat(D);  Y = 2*Y.st()

  assert math.isclose(accu(abs(X - 2*conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*conj(Dt))), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = 0 + 2*X.st()
  Y = cx_mat(D);  Y = 0 + 2*Y.st()

  assert math.isclose(accu(abs(X - 2*conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - 2*conj(Dt))), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = (2*X).st()
  Y = cx_mat(D);  Y = (2*Y).st()

  assert math.isclose(accu(abs(X - conj(2*Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - conj(2*Dt))), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = (X+X).st()
  Y = cx_mat(D);  Y = (Y+Y).st()

  assert math.isclose(accu(abs(X - conj(2*Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - conj(2*Dt))), 0.0, abs_tol=0.00001) == True

  X = cx_mat(C);  X = complex(2,3)*X.st()
  Y = cx_mat(D);  Y = complex(2,3)*Y.st()

  assert math.isclose(accu(abs(X - complex(2,3)*conj(Ct))), 0.0, abs_tol=0.00001) == True
  assert math.isclose(accu(abs(Y - complex(2,3)*conj(Dt))), 0.0, abs_tol=0.00001) == True



# def test_op_trans_sp_mat():
#   {
#   SpMat<unsigned int> a(4, 4);
#   a(1, 0) = 5;
#   a(2, 2) = 3;
#   a(3, 3) = 4;
#   a(1, 3) = 6;
#   a(3, 1) = 8;

#   SpMat<unsigned int> b = trans(a);

#   assert (unsigned int) b(0, 0) == 0
#   assert (unsigned int) b(1, 0) == 0
#   assert (unsigned int) b(2, 0) == 0
#   assert (unsigned int) b(3, 0) == 0
#   assert (unsigned int) b(0, 1) == 5
#   assert (unsigned int) b(1, 1) == 0
#   assert (unsigned int) b(2, 1) == 0
#   assert (unsigned int) b(3, 1) == 6
#   assert (unsigned int) b(0, 2) == 0
#   assert (unsigned int) b(1, 2) == 0
#   assert (unsigned int) b(2, 2) == 3
#   assert (unsigned int) b(3, 2) == 0
#   assert (unsigned int) b(0, 3) == 0
#   assert (unsigned int) b(1, 3) == 8
#   assert (unsigned int) b(2, 3) == 0
#   assert (unsigned int) b(3, 3) == 4

#   b = trans(b); # inplace

#   assert (unsigned int) b(0, 0) == 0
#   assert (unsigned int) b(1, 0) == 5
#   assert (unsigned int) b(2, 0) == 0
#   assert (unsigned int) b(3, 0) == 0
#   assert (unsigned int) b(0, 1) == 0
#   assert (unsigned int) b(1, 1) == 0
#   assert (unsigned int) b(2, 1) == 0
#   assert (unsigned int) b(3, 1) == 8
#   assert (unsigned int) b(0, 2) == 0
#   assert (unsigned int) b(1, 2) == 0
#   assert (unsigned int) b(2, 2) == 3
#   assert (unsigned int) b(3, 2) == 0
#   assert (unsigned int) b(0, 3) == 0
#   assert (unsigned int) b(1, 3) == 6
#   assert (unsigned int) b(2, 3) == 0
#   assert (unsigned int) b(3, 3) == 4

#   b = trans(a + a); # on an op

#   assert (unsigned int) b(0, 0) == 0
#   assert (unsigned int) b(1, 0) == 0
#   assert (unsigned int) b(2, 0) == 0
#   assert (unsigned int) b(3, 0) == 0
#   assert (unsigned int) b(0, 1) == 10
#   assert (unsigned int) b(1, 1) == 0
#   assert (unsigned int) b(2, 1) == 0
#   assert (unsigned int) b(3, 1) == 12
#   assert (unsigned int) b(0, 2) == 0
#   assert (unsigned int) b(1, 2) == 0
#   assert (unsigned int) b(2, 2) == 6
#   assert (unsigned int) b(3, 2) == 0
#   assert (unsigned int) b(0, 3) == 0
#   assert (unsigned int) b(1, 3) == 16
#   assert (unsigned int) b(2, 3) == 0
#   assert (unsigned int) b(3, 3) == 8

#   b = trans(trans(a)); # on another trans

#   assert (unsigned int) b(0, 0) == 0
#   assert (unsigned int) b(1, 0) == 5
#   assert (unsigned int) b(2, 0) == 0
#   assert (unsigned int) b(3, 0) == 0
#   assert (unsigned int) b(0, 1) == 0
#   assert (unsigned int) b(1, 1) == 0
#   assert (unsigned int) b(2, 1) == 0
#   assert (unsigned int) b(3, 1) == 8
#   assert (unsigned int) b(0, 2) == 0
#   assert (unsigned int) b(1, 2) == 0
#   assert (unsigned int) b(2, 2) == 3
#   assert (unsigned int) b(3, 2) == 0
#   assert (unsigned int) b(0, 3) == 0
#   assert (unsigned int) b(1, 3) == 6
#   assert (unsigned int) b(2, 3) == 0
#   assert (unsigned int) b(3, 3) == 4
#   ]


# def test_op_trans_sp_cxmat():
#   {
#   SpMat<complex> a(10, 10);
#   for (uword c = 0; c < 7; ++c)
#   {
#     a(c, c) = complex(1.3, 2.4);
#     a(c + 1, c) = complex(0.0, -1.3);
#     a(c + 2, c) = complex(2.1, 0.0, abs_tol=0.00001);
#   ]

#   SpMat<complex> b = trans(a);

#   assert b.n_nonzero == a.n_nonzero

#   for (uword r = 0; r < 10; ++r)
#     {
#     for (uword c = 0; c < 10; ++c)
#       {
#       double lr = real(complex(a(r, c)));
#       double rr = real(complex(b(c, r)));
#       double li = imag(complex(a(r, c)));
#       double ri = imag(complex(b(c, r)));

#       assert math.isclose(lr, rr) == True
#       assert math.isclose(li, -ri) == True
#       ]
#     ]

#   b = trans(a[3:7, 3:7)];

#   assert b.n_nonzero == a[3:7, 3:7].n_nonzero

#   for (uword r = 0; r < 5; ++r)
#     {
#     for (uword c = 0; c < 5; ++c)
#       {
#       double lr = real(complex(a(r + 3, c + 3)));
#       double rr = real(complex(b(c, r)));
#       double li = imag(complex(a(r + 3, c + 3)));
#       double ri = imag(complex(b(c, r)));

#       assert math.isclose(lr, rr) == True
#       assert math.isclose(li, -ri) == True
#       ]
#     ]
#   ]
