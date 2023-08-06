# Copyright 2021 Terry Yue Zhuo
# Copyright 2021 Data61/CSIRO

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

def test_fn_symmat_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
        ")

    B = pa.symmatu( A[0,0,pa.size(5,5)] )
    C = pa.symmatl( A[0,0,pa.size(5,5)] )

    BB = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.201990   0.058956  -0.149362  -0.045465   0.296153;\
        0.019678  -0.149362   0.314156   0.419733   0.068317;\
        -0.493936  -0.045465   0.419733  -0.393139  -0.135040;\
        -0.126745   0.296153   0.068317  -0.135040  -0.353768;\
        ")

    CC = pa.mat("\
        0.061198   0.437242  -0.492474   0.336352   0.239585;\
        0.437242   0.058956  -0.031309   0.411541  -0.428913;\
        -0.492474  -0.031309   0.314156   0.458476  -0.406953;\
        0.336352   0.411541   0.458476  -0.393139  -0.291020;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
        ")

    assert math.isclose(pa.accu(pa.abs( B - BB )), 0.0) == True
    assert math.isclose(pa.accu(pa.abs( C - CC )), 0.0) == True

    with pytest.raises(RuntimeError):
        X = pa.symmatu(A)

def test_fn_symmat_2():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
        ")

    B1 = pa.symmatu( pa.cx_mat( pa.mat(A[0,0,pa.size(3,3)]), pa.mat(A[0,3,pa.size(3,3)]) ) )
    C1 = pa.symmatl( pa.cx_mat( pa.mat(A[0,0,pa.size(3,3)]), pa.mat(A[0,3,pa.size(3,3)]) ) )

    B2 = pa.symmatu( pa.cx_mat( pa.mat(A[0,0,pa.size(3,3)]), pa.mat(A[0,3,pa.size(3,3)]) ), True )
    C2 = pa.symmatl( pa.cx_mat( pa.mat(A[0,0,pa.size(3,3)]), pa.mat(A[0,3,pa.size(3,3)]) ), True )

    D = pa.symmatu( pa.cx_mat( pa.mat(A[0,0,pa.size(3,3)]), pa.mat(A[0,3,pa.size(3,3)]) ), False )
    E = pa.symmatl( pa.cx_mat( pa.mat(A[0,0,pa.size(3,3)]), pa.mat(A[0,3,pa.size(3,3)]) ), False )

    BB = pa.cx_mat([
        [ complex( 0.06120, -0.49394), complex( 0.20199, -0.12674), complex( 0.01968, +0.05141) ],
        [ complex( 0.20199, +0.12674), complex( 0.05896, +0.29615), complex(-0.14936, +0.03544) ],
        [ complex( 0.01968, -0.05141), complex(-0.14936, -0.03544), complex( 0.31416, -0.45450) ]
    ])

    CC = pa.cx_mat([
        [ complex( 0.06120, -0.49394), complex( 0.43724, +0.04546), complex(-0.49247, -0.41973) ],
        [ complex( 0.43724, -0.04546), complex( 0.05896, +0.29615), complex(-0.03131, -0.06832) ],
        [ complex(-0.49247, +0.41973), complex(-0.03131, +0.06832), complex( 0.31416, -0.45450) ]
    ])

    DD = pa.cx_mat([
        [ complex( 0.06120, -0.49394), complex( 0.20199, -0.12674), complex( 0.01968, +0.05141) ],
        [ complex( 0.20199, -0.12674), complex( 0.05896, +0.29615), complex(-0.14936, +0.03544) ],
        [ complex( 0.01968, +0.05141), complex(-0.14936, +0.03544), complex( 0.31416, -0.45450) ]
    ])

    EE = pa.cx_mat([
        [ complex( 0.06120, -0.49394), complex( 0.43724, -0.04546), complex(-0.49247, +0.41973) ],
        [ complex( 0.43724, -0.04546), complex( 0.05896, +0.29615), complex(-0.03131, +0.06832) ],
        [ complex(-0.49247, +0.41973), complex(-0.03131, +0.06832), complex( 0.31416, -0.45450) ]
    ])

    assert math.isclose(pa.accu(pa.abs( B1 - BB )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs( C1 - CC )), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs( B2 - BB )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs( C2 - CC )), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs( D  - DD )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs( E  - EE )), 0.0, abs_tol=0.0001) == True

    with pytest.raises(RuntimeError):
        X = pa.symmatu( pa.cx_mat(pa.mat(A[0,0,pa.size(2,3)]), pa.mat(A[0,3,pa.size(2,3)])) )
