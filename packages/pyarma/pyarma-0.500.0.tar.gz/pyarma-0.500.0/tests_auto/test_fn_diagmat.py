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

def test_fn_diagmat_1():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    Ap1 = pa.mat([
        [ -0.0    ,  0.69298,  0.0    ,  0.0     ],
        [  0.0    ,  0.0    ,  0.78987,  0.0     ],
        [  0.0    ,  0.0    ,  0.0    ,  0.40163 ]
    ])

    Amain = pa.mat([
        [ -0.78838,  0.0    ,  0.0    ,  0.0     ],
        [  0.0    , -0.12020,  0.0    ,  0.0     ],
        [  0.0    ,  0.0    , -0.22263,  0.0     ]
    ])

    Am1 = pa.mat([
        [  0.0    ,  0.0    ,  0.0    ,  0.0     ],
        [  0.49345,  0.0    ,  0.0    ,  0.0     ],
        [  0.0    ,  0.52104,  0.0    ,  0.0     ]
    ])
      
    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A   ) - Amain)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A, 0) - Amain)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A, 1) - Ap1  )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A,-1) - Am1  )), 0.0, abs_tol=0.0001) == True

def test_fn_diagmat_2():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    dp1 = pa.mat([
        [   0.69298,  0.78987,  0.40163 ]
    ])

    dmain = pa.mat([
        [ -0.78838, -0.12020, -0.22263 ]
    ])

    dm1 = pa.mat([
        [  0.49345,  0.52104           ]
    ])

    Ap1 = pa.mat(pa.size(A),pa.fill.zeros)
    Ap1[pa.diag,1] = dp1

    Amain = pa.mat(pa.size(A),pa.fill.zeros)
    Amain[pa.diag] = dmain

    Am1 = pa.mat(pa.size(A),pa.fill.zeros)
    Am1[pa.diag,-1] = dm1

    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A   ) - Amain)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A, 0) - Amain)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A, 1) - Ap1  )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diagmat(A,-1) - Am1  )), 0.0, abs_tol=0.0001) == True

def test_fn_diagmat_3():

    A = pa.mat([
        [ -0.78838,  0.69298,  0.41084,  0.90142 ],
        [  0.49345, -0.12020,  0.78987,  0.53124 ],
        [  0.73573,  0.52104, -0.22263,  0.40163 ]
    ])

    B = pa.mat("\
        0.171180   0.106848   0.490557  -0.079866;\
        0.073839  -0.428277  -0.049842   0.398193;\
        -0.030523   0.366160   0.260348  -0.412238;\
    ")

    Asub = A[:,0:2]
    At  = A.t()

    Bsub = B[:,0:2]
    Bt  = B.t()

    Asubdiagmat_times_Bsubdiagmat = pa.mat("\
        -0.13495488840   0.00000000000   0.00000000000;\
        0.00000000000   0.05147889540   0.00000000000;\
        0.00000000000   0.00000000000  -0.05796127524;\
    ")

    Bsub_times_Adiagmat = pa.mat("\
        -0.13495488840  -0.01284312960  -0.10921270491   0.00000000000;\
        -0.05821319082   0.05147889540   0.01109632446   0.00000000000;\
        0.02406372274  -0.04401243200  -0.05796127524   0.00000000000;\
    ")

    Adiagmat_times_Bt = pa.mat("\
        -0.134955  -0.058213   0.024064;\
        -0.012843   0.051479  -0.044012;\
        -0.109213   0.011096  -0.057961;\
    ")

    assert math.isclose(pa.accu(pa.abs((pa.diagmat(Asub) * pa.diagmat(Bsub)) - Asubdiagmat_times_Bsubdiagmat)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs((Bsub                    * pa.diagmat(A)) - Bsub_times_Adiagmat)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs((B[:, 0:2] * pa.diagmat(A)) - Bsub_times_Adiagmat)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs((pa.diagmat(A) * Bt    ) - Adiagmat_times_Bt  )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs((pa.diagmat(A) * B.t() ) - Adiagmat_times_Bt  )), 0.0, abs_tol=0.0001) == True