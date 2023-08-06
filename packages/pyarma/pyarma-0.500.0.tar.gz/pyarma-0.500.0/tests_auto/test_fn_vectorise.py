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

def test_fn_vectorise_1():

    A = pa.mat("\
     0.061198   0.201990;\
     0.437242   0.058956;\
    -0.492474  -0.031309;\
     0.336352   0.411541;\
    ")

    a = pa.mat([
        [0.061198],
        [0.437242],
        [-0.492474],
        [0.336352],
        [0.201990],
        [0.058956],
        [-0.031309],
        [0.411541],
    ])

    b = pa.mat([ 0.061198, 0.201990, 0.437242, 0.058956, -0.492474, -0.031309, 0.336352, 0.411541 ])

    assert math.isclose(pa.accu(pa.abs(a - pa.vectorise(A  ))) , 0.0) == True
    assert math.isclose(pa.accu(pa.abs(a - pa.vectorise(A,0))) , 0.0) == True
    assert math.isclose(pa.accu(pa.abs(b - pa.vectorise(A,1))) , 0.0) == True