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

def test_find_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

    A[2,2] = 0.0

    indices_nonzero = pa.mat([[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29]])

    indices_zero = pa.mat([12])

    indices_greaterthan_00 = pa.mat([[0], [1], [3], [4], [5], [6], [8], [10], [13], [17], [21], [22], [25], [26], [28], [29]])

    indices_lessthan_00 = pa.mat([[2], [7], [9], [11], [14], [15], [16], [18], [19], [20], [23], [24], [27]])

    indices_greaterthan_04 = pa.mat([[1], [8], [13], [17]])

    indices_lessthan_neg04 = pa.mat([[2], [9], [14], [15], [27]])