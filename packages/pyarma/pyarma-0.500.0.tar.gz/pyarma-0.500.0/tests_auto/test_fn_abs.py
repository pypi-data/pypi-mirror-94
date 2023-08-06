# Copyright 2020-2021 Terry Yue Zhuo
# Copyright 2020-2021 Data61/CSIRO

# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

import sys
import math
import pytest
import pyarma as pa

def test_fn_abs_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

    abs_A = pa.mat("\
        0.061198   0.201990   0.019678   0.493936   0.126745   0.051408;\
        0.437242   0.058956   0.149362   0.045465   0.296153   0.035437;\
        0.492474   0.031309   0.314156   0.419733   0.068317   0.454499;\
        0.336352   0.411541   0.458476   0.393139   0.135040   0.373833;\
        0.239585   0.428913   0.406953   0.291020   0.353768   0.258704;\
    ")

    X = pa.abs(A)

    assert math.isclose(X[0,0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(X[1,0], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(X[2,0], 0.492474, abs_tol=0.0001) == True
    assert math.isclose(X[3,0], 0.336352, abs_tol=0.0001) == True
    assert math.isclose(X[4,0], 0.239585, abs_tol=0.0001) == True

    assert math.isclose(X[0,1], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(X[1,1], 0.058956, abs_tol=0.0001) == True
    assert math.isclose(X[2,1], 0.031309, abs_tol=0.0001) == True
    assert math.isclose(X[3,1], 0.411541, abs_tol=0.0001) == True
    assert math.isclose(X[4,1], 0.428913, abs_tol=0.0001) == True

    assert math.isclose(X[0,5], 0.051408, abs_tol=0.0001) == True
    assert math.isclose(X[1,5], 0.035437, abs_tol=0.0001) == True
    assert math.isclose(X[2,5], 0.454499, abs_tol=0.0001) == True
    assert math.isclose(X[3,5], 0.373833, abs_tol=0.0001) == True
    assert math.isclose(X[4,5], 0.258704, abs_tol=0.0001) == True

    Y = pa.abs(2*A) / 2

    assert math.isclose(Y[0,0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(Y[1,0], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(Y[2,0], 0.492474, abs_tol=0.0001) == True
    assert math.isclose(Y[3,0], 0.336352, abs_tol=0.0001) == True
    assert math.isclose(Y[4,0], 0.239585, abs_tol=0.0001) == True

    assert math.isclose(Y[0,1], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(Y[1,1], 0.058956, abs_tol=0.0001) == True
    assert math.isclose(Y[2,1], 0.031309, abs_tol=0.0001) == True
    assert math.isclose(Y[3,1], 0.411541, abs_tol=0.0001) == True
    assert math.isclose(Y[4,1], 0.428913, abs_tol=0.0001) == True

    assert math.isclose(Y[0,5], 0.051408, abs_tol=0.0001) == True
    assert math.isclose(Y[1,5], 0.035437, abs_tol=0.0001) == True
    assert math.isclose(Y[2,5], 0.454499, abs_tol=0.0001) == True
    assert math.isclose(Y[3,5], 0.373833, abs_tol=0.0001) == True
    assert math.isclose(Y[4,5], 0.258704, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(A) - abs_A), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*pa.abs(A) - 2*abs_A), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(-A) - abs_A), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*pa.abs(-A) - 2*abs_A), 0.0, abs_tol=0.0001) == True

def test_fn_abs_2():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

    C = pa.cx_mat(A,pa.fliplr(A))

    abs_C = pa.mat("\
        0.079925   0.238462   0.494328   0.494328   0.238462   0.079925;\
        0.438676   0.301964   0.156128   0.156128   0.301964   0.438676;\
        0.670149   0.075150   0.524280   0.524280   0.075150   0.670149;\
        0.502876   0.433130   0.603952   0.603952   0.433130   0.502876;\
        0.352603   0.555984   0.500303   0.500303   0.555984   0.352603;\
    ")

    X = pa.abs(C)

    assert math.isclose(X[0,0], 0.079925, abs_tol=0.0001) == True
    assert math.isclose(X[1,0], 0.438676, abs_tol=0.0001) == True
    assert math.isclose(X[2,0], 0.670149, abs_tol=0.0001) == True
    assert math.isclose(X[3,0], 0.502876, abs_tol=0.0001) == True
    assert math.isclose(X[4,0], 0.352603, abs_tol=0.0001) == True

    assert math.isclose(X[0,1], 0.238462, abs_tol=0.0001) == True
    assert math.isclose(X[1,1], 0.301964, abs_tol=0.0001) == True
    assert math.isclose(X[2,1], 0.075150, abs_tol=0.0001) == True
    assert math.isclose(X[3,1], 0.433130, abs_tol=0.0001) == True
    assert math.isclose(X[4,1], 0.555984, abs_tol=0.0001) == True

    assert math.isclose(X[0,5], 0.079925, abs_tol=0.0001) == True
    assert math.isclose(X[1,5], 0.438676, abs_tol=0.0001) == True
    assert math.isclose(X[2,5], 0.670149, abs_tol=0.0001) == True
    assert math.isclose(X[3,5], 0.502876, abs_tol=0.0001) == True
    assert math.isclose(X[4,5], 0.352603, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(C) - abs_C), 0.0, abs_tol=0.0001) == True

def test_fn_abs_cube_1():

    A = pa.cube([[[0.061198 ,   0.201990,   0.019678,  -0.493936,  -0.126745,   0.051408],
                  [0.437242 ,   0.058956,  -0.149362,  -0.045465,   0.296153,   0.035437],
                  [-0.492474,  -0.031309,   0.314156,   0.419733,   0.068317,  -0.454499],
                  [0.336352 ,   0.411541,   0.458476,  -0.393139,  -0.135040,   0.373833],
                  [0.239585 ,  -0.428913,  -0.406953,  -0.291020,  -0.353768,   0.258704]],
                 [[0.061198 ,   0.201990,   0.019678,  -0.493936,  -0.126745,   0.051408],
                  [0.437242 ,   0.058956,  -0.149362,  -0.045465,   0.296153,   0.035437],
                  [-0.492474,  -0.031309,   0.314156,   0.419733,   0.068317,  -0.454499],
                  [0.336352 ,   0.411541,   0.458476,  -0.393139,  -0.135040,   0.373833],
                  [0.239585 ,  -0.428913,  -0.406953,  -0.291020,  -0.353768,   0.258704]]])

    abs_A = pa.cube([[[0.061198,   0.201990,   0.019678,   0.493936,   0.126745,   0.051408],
                      [0.437242,   0.058956,   0.149362,   0.045465,   0.296153,   0.035437],
                      [0.492474,   0.031309,   0.314156,   0.419733,   0.068317,   0.454499],
                      [0.336352,   0.411541,   0.458476,   0.393139,   0.135040,   0.373833],
                      [0.239585,   0.428913,   0.406953,   0.291020,   0.353768,   0.258704]],
                     [[0.061198,   0.201990,   0.019678,   0.493936,   0.126745,   0.051408],
                      [0.437242,   0.058956,   0.149362,   0.045465,   0.296153,   0.035437],
                      [0.492474,   0.031309,   0.314156,   0.419733,   0.068317,   0.454499],
                      [0.336352,   0.411541,   0.458476,   0.393139,   0.135040,   0.373833],
                      [0.239585,   0.428913,   0.406953,   0.291020,   0.353768,   0.258704]]])

    X = pa.abs(A)

    assert math.isclose(X[0,0,0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(X[1,0,0], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(X[2,0,0], 0.492474, abs_tol=0.0001) == True
    assert math.isclose(X[3,0,0], 0.336352, abs_tol=0.0001) == True
    assert math.isclose(X[4,0,0], 0.239585, abs_tol=0.0001) == True

    assert math.isclose(X[0,1,0], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(X[1,1,0], 0.058956, abs_tol=0.0001) == True
    assert math.isclose(X[2,1,0], 0.031309, abs_tol=0.0001) == True
    assert math.isclose(X[3,1,0], 0.411541, abs_tol=0.0001) == True
    assert math.isclose(X[4,1,0], 0.428913, abs_tol=0.0001) == True

    assert math.isclose(X[0,5,0], 0.051408, abs_tol=0.0001) == True
    assert math.isclose(X[1,5,0], 0.035437, abs_tol=0.0001) == True
    assert math.isclose(X[2,5,0], 0.454499, abs_tol=0.0001) == True
    assert math.isclose(X[3,5,0], 0.373833, abs_tol=0.0001) == True
    assert math.isclose(X[4,5,0], 0.258704, abs_tol=0.0001) == True

    assert math.isclose(X[0,0,1], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(X[1,0,1], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(X[2,0,1], 0.492474, abs_tol=0.0001) == True
    assert math.isclose(X[3,0,1], 0.336352, abs_tol=0.0001) == True
    assert math.isclose(X[4,0,1], 0.239585, abs_tol=0.0001) == True

    assert math.isclose(X[0,1,1], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(X[1,1,1], 0.058956, abs_tol=0.0001) == True
    assert math.isclose(X[2,1,1], 0.031309, abs_tol=0.0001) == True
    assert math.isclose(X[3,1,1], 0.411541, abs_tol=0.0001) == True
    assert math.isclose(X[4,1,1], 0.428913, abs_tol=0.0001) == True

    assert math.isclose(X[0,5,1], 0.051408, abs_tol=0.0001) == True
    assert math.isclose(X[1,5,1], 0.035437, abs_tol=0.0001) == True
    assert math.isclose(X[2,5,1], 0.454499, abs_tol=0.0001) == True
    assert math.isclose(X[3,5,1], 0.373833, abs_tol=0.0001) == True
    assert math.isclose(X[4,5,1], 0.258704, abs_tol=0.0001) == True

    Y = pa.abs(2*A) / 2

    assert math.isclose(Y[0,0,0], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(Y[1,0,0], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(Y[2,0,0], 0.492474, abs_tol=0.0001) == True
    assert math.isclose(Y[3,0,0], 0.336352, abs_tol=0.0001) == True
    assert math.isclose(Y[4,0,0], 0.239585, abs_tol=0.0001) == True

    assert math.isclose(Y[0,1,0], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(Y[1,1,0], 0.058956, abs_tol=0.0001) == True
    assert math.isclose(Y[2,1,0], 0.031309, abs_tol=0.0001) == True
    assert math.isclose(Y[3,1,0], 0.411541, abs_tol=0.0001) == True
    assert math.isclose(Y[4,1,0], 0.428913, abs_tol=0.0001) == True

    assert math.isclose(Y[0,5,0], 0.051408, abs_tol=0.0001) == True
    assert math.isclose(Y[1,5,0], 0.035437, abs_tol=0.0001) == True
    assert math.isclose(Y[2,5,0], 0.454499, abs_tol=0.0001) == True
    assert math.isclose(Y[3,5,0], 0.373833, abs_tol=0.0001) == True
    assert math.isclose(Y[4,5,0], 0.258704, abs_tol=0.0001) == True

    assert math.isclose(Y[0,0,1], 0.061198, abs_tol=0.0001) == True
    assert math.isclose(Y[1,0,1], 0.437242, abs_tol=0.0001) == True
    assert math.isclose(Y[2,0,1], 0.492474, abs_tol=0.0001) == True
    assert math.isclose(Y[3,0,1], 0.336352, abs_tol=0.0001) == True
    assert math.isclose(Y[4,0,1], 0.239585, abs_tol=0.0001) == True

    assert math.isclose(Y[0,1,1], 0.201990, abs_tol=0.0001) == True
    assert math.isclose(Y[1,1,1], 0.058956, abs_tol=0.0001) == True
    assert math.isclose(Y[2,1,1], 0.031309, abs_tol=0.0001) == True
    assert math.isclose(Y[3,1,1], 0.411541, abs_tol=0.0001) == True
    assert math.isclose(Y[4,1,1], 0.428913, abs_tol=0.0001) == True

    assert math.isclose(Y[0,5,1], 0.051408, abs_tol=0.0001) == True
    assert math.isclose(Y[1,5,1], 0.035437, abs_tol=0.0001) == True
    assert math.isclose(Y[2,5,1], 0.454499, abs_tol=0.0001) == True
    assert math.isclose(Y[3,5,1], 0.373833, abs_tol=0.0001) == True
    assert math.isclose(Y[4,5,1], 0.258704, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(A) - abs_A), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*pa.abs(A) - 2*abs_A), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(-A) - abs_A), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(2*pa.abs(-A) - 2*abs_A), 0.0, abs_tol=0.0001) == True
