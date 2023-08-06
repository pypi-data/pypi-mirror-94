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

def test_fn_clamp_1():

    A  = pa.mat(5,6,pa.fill.randu)

    B = pa.clamp(A, 0.2, 0.8) 
    assert math.isclose(B.min(), 0.2, abs_tol=0.0001) == True
    assert math.isclose(B.max(), 0.8, abs_tol=0.0001) == True

    C = pa.clamp(A, A.min(), 0.8) 
    assert C.min() == A.min()
    assert math.isclose(C.max(), 0.8, abs_tol=0.0001) == True

    D = pa.clamp(A, 0.2, A.max())   
    assert math.isclose(D.min(), 0.2, abs_tol=0.0001) == True
    assert D.max() == A.max()

    with pytest.raises(RuntimeError):
        pa.clamp(A, A.max(), A.min())