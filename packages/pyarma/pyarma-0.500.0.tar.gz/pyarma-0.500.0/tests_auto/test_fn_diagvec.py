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

def test_fn_diagvec_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
    ")

    A_main1 = pa.diagvec(A)
    A_main2 = pa.diagvec(A,0)

    A_p1 = pa.diagvec(A, 1)
    A_m1 = pa.diagvec(A,-1)

    a = pa.mat([
        [0.061198],
        [0.058956],
        [0.314156],
        [-0.393139],
        [-0.353768]
    ])

    b = pa.mat([
        [0.20199],
        [-0.14936],
        [0.41973],
        [-0.13504]
    ])

    c = pa.mat([
        [0.437242],
        [-0.031309],
        [0.458476],
        [-0.291020]
    ])

    assert math.isclose(pa.accu(pa.abs(A_main1 - a)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A_main2 - a)), 0.0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(A_p1 - b)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A_m1 - c)), 0.0, abs_tol=0.0001) == True