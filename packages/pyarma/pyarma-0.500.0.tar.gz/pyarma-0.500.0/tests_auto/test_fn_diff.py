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

def test_fn_diff_1():
# TODO: FIX 
    a = pa.square(pa.linspace(1,5,6))
    b = pa.square(pa.mat([[1,5,5]]))

    a_diff_1 = pa.mat([[2.2400], [3.5200], [4.8000], [6.0800], [7.3600]])
    a_diff_2 = pa.mat([[1.2800], [1.2800], [1.2800], [1.2800]])
    a_diff_9 = pa.mat([[]])

    b_diff_1 = pa.mat([[3, 5, 7, 9]])
    b_diff_2 = pa.mat([[2, 2, 2]])
    b_diff_9 = pa.mat([[]])

    assert math.isclose(pa.accu(pa.abs(pa.diff(a,0) - a       )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(a  ) - a_diff_1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(a,1) - a_diff_1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(a,2) - a_diff_2)), 0.0, abs_tol=0.0001) == True
    # assert math.isclose(pa.accu(pa.abs(pa.diff(a,9) - a_diff_9)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(pa.diff(b,0) - b       )), 0.0, abs_tol=0.0001) == True
    # assert math.isclose(pa.accu(pa.abs(pa.diff(b  ) - b_diff_1)), 0.0, abs_tol=0.0001) == True
    # assert math.isclose(pa.accu(pa.abs(pa.diff(b,1) - b_diff_1)), 0.0, abs_tol=0.0001) == True
    # assert math.isclose(pa.accu(pa.abs(pa.diff(b,2) - b_diff_2)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(b,9) - b_diff_9)), 0.0, abs_tol=0.0001) == True

def test_fn_diff_2():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
    ")

    A_diff1_0 = pa.mat("\
        0.376044  -0.143034  -0.169040   0.448471   0.422898;\
        -0.929716  -0.090265   0.463518   0.465198  -0.227836;\
        0.828826   0.442850   0.144320  -0.812872  -0.203357;\
        -0.096767  -0.840454  -0.865429   0.102119  -0.218728;\
    ")

    A_diff2_0 = pa.mat("\
        -1.305760   0.052769   0.632558   0.016727  -0.650734;\
        1.758542   0.533115  -0.319198  -1.278070   0.024479;\
        -0.925593  -1.283304  -1.009749   0.914991  -0.015371;\
    ")

    A_diff3_0 = pa.mat("\
        3.064302   0.480346  -0.951756  -1.294797   0.675213;\
        -2.684135  -1.816419  -0.690551   2.193061  -0.039850;\
    ")

    A_diff1_1 = pa.mat("\
        0.140792  -0.182312  -0.513614   0.367191;\
        -0.378286  -0.208318   0.103897   0.341618;\
        0.461165   0.345465   0.105577  -0.351416;\
        0.075189   0.046935  -0.851615   0.258099;\
        -0.668498   0.021960   0.115933  -0.062748;\
    ")

    A_diff2_1 = pa.mat("\
        -0.323104  -0.331302   0.880805;\
        0.169968   0.312215   0.237721;\
        -0.115700  -0.239888  -0.456993;\
        -0.028254  -0.898550   1.109714;\
        0.690458   0.093973  -0.178681;\
    ")

    A_diff3_1 = pa.mat("\
        -0.0081980   1.2121070;\
        0.1422470  -0.0744940;\
        -0.1241880  -0.2171050;\
        -0.8702960   2.0082640;\
        -0.5964850  -0.2726540;\
    ")

    assert math.isclose(pa.accu(pa.abs(pa.diff(A,0) - A        )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A  ) - A_diff1_0)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,1) - A_diff1_0)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,2) - A_diff2_0)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,3) - A_diff3_0)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(pa.diff(A,0,0) - A        )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,1,0) - A_diff1_0)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,2,0) - A_diff2_0)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,3,0) - A_diff3_0)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(pa.diff(A,0,1) - A        )), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,1,1) - A_diff1_1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,2,1) - A_diff2_1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.diff(A,3,1) - A_diff3_1)), 0.0, abs_tol=0.0001) == True