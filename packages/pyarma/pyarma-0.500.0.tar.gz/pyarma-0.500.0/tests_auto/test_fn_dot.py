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

def test_fn_dot_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
    ")

    a = A[pa.head_cols,1]
    b = A[pa.tail_cols,1]

    c = A[pa.head_rows,1]
    d = A[pa.tail_rows,1]

    assert math.isclose(pa.dot(  a,  b), -0.04208883710200, abs_tol=0.0001) == True
    assert math.isclose(pa.dot(2*a,2+b), 2.24343432579600, abs_tol=0.0001) == True

    assert math.isclose(pa.dot(    c,  d), 0.108601544706000, abs_tol=0.0001) == True
    assert math.isclose(pa.dot(0.5*c,2-d), -0.392115772353000, abs_tol=0.0001) == True

    assert math.isclose(pa.dot(a,b), pa.dot(A[pa.head_cols,1], A[pa.tail_cols,1]), abs_tol=0.0001) == True
    assert math.isclose(pa.dot(c,d), pa.dot(A[pa.head_rows,1], A[pa.tail_rows,1]), abs_tol=0.0001) == True

def test_fn_dot_2():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
    ")

    a = pa.cx_mat(pa.mat(A[:,0]), pa.mat(A[:,1]))
    b = pa.cx_mat(pa.mat(A[:,2]), pa.mat(A[:,3]))

    c = pa.cx_mat(pa.mat(A[0,:]), pa.mat(A[1,:]))
    d = pa.cx_mat(pa.mat(A[2,:]), pa.mat(A[3,:]))

    assert math.isclose(abs(pa.dot(a,b) - complex(-0.009544718641000, -0.110209641379000)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(abs(pa.dot(c,d) - complex(-0.326993347830000, +0.061084261990000)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(abs(pa.cdot(a,b) - complex(-0.314669805873000, -0.807333974477000)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(abs(pa.cdot(c,d) - complex(-0.165527940664000, +0.586984291846000)), 0.0, abs_tol=0.0001) == True
