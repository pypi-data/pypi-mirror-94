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

def test_fn_conv_1():

    a =  pa.linspace(1,5,6)
    b = 2*pa.linspace(1,6,7)

    c = pa.conv(a,b)
    d = pa.mat([
        [2.00000000000000],
        [7.26666666666667],
        [17.13333333333333],
        [32.93333333333334],
        [56.00000000000000],
        [87.66666666666667],
        [117.66666666666666],
        [134.00000000000003],
        [137.73333333333335],
        [127.53333333333336],
        [102.06666666666668],
        [60.00000000000000]
    ])

    assert math.isclose(pa.accu(pa.abs(c - d)), 0.0, abs_tol=0.0001) == True