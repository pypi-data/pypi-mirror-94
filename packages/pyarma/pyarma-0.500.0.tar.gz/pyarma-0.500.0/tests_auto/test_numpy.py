# Copyright 2020-2021 Jason Rumengan
# Copyright 2020-2021 Data61/CSIRO
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

import pytest
import numpy as np
from pyarma import *
import math

class Test_NumPy:
    # TODO: add error case where NP array size is incorrect
    # Normal case: convert PyArmadillo matrix to NumPy array
    def test_numpy_1(self):
        a = mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
        ")
        b = np.array(a)
        assert math.isclose(a[0], b[0,0], abs_tol=0.0001) == True
        assert math.isclose(a[1], b[1,0], abs_tol=0.0001) == True
        assert math.isclose(a[2], b[2,0], abs_tol=0.0001) == True
        assert math.isclose(a[3], b[3,0], abs_tol=0.0001) == True
        assert math.isclose(a[4], b[4,0], abs_tol=0.0001) == True
        assert math.isclose(a[5], b[0,1], abs_tol=0.0001) == True
        assert math.isclose(a[6], b[1,1], abs_tol=0.0001) == True
        assert math.isclose(a[7], b[2,1], abs_tol=0.0001) == True
        assert math.isclose(a[8], b[3,1], abs_tol=0.0001) == True
        assert math.isclose(a[9], b[4,1], abs_tol=0.0001) == True
        assert math.isclose(a[10], b[0,2], abs_tol=0.0001) == True
        assert math.isclose(a[11], b[1,2], abs_tol=0.0001) == True
        assert math.isclose(a[12], b[2,2], abs_tol=0.0001) == True
        assert math.isclose(a[13], b[3,2], abs_tol=0.0001) == True
        assert math.isclose(a[14], b[4,2], abs_tol=0.0001) == True
        assert math.isclose(a[15], b[0,3], abs_tol=0.0001) == True
        assert math.isclose(a[16], b[1,3], abs_tol=0.0001) == True
        assert math.isclose(a[17], b[2,3], abs_tol=0.0001) == True
        assert math.isclose(a[18], b[3,3], abs_tol=0.0001) == True
        assert math.isclose(a[19], b[4,3], abs_tol=0.0001) == True
        assert math.isclose(a[20], b[0,4], abs_tol=0.0001) == True
        assert math.isclose(a[21], b[1,4], abs_tol=0.0001) == True
        assert math.isclose(a[22], b[2,4], abs_tol=0.0001) == True
        assert math.isclose(a[23], b[3,4], abs_tol=0.0001) == True
        assert math.isclose(a[24], b[4,4], abs_tol=0.0001) == True

    # Normal case: convert NumPy array to PyArmadillo matrix
    def test_numpy_2(self):
        b = np.array([
        [0.061198,   0.201990,   0.019678,  -0.493936,  -0.126745],
        [0.437242,   0.058956,  -0.149362,  -0.045465,   0.296153],
        [-0.492474,  -0.031309,   0.314156,   0.419733,   0.068317],
        [0.336352,   0.411541,   0.458476,  -0.393139,  -0.135040],
        [0.239585,  -0.428913,  -0.406953,  -0.291020,  -0.353768]
        ])
        a = mat(b)
        assert math.isclose(a[0], b[0,0], abs_tol=0.0001) == True
        assert math.isclose(a[1], b[1,0], abs_tol=0.0001) == True
        assert math.isclose(a[2], b[2,0], abs_tol=0.0001) == True
        assert math.isclose(a[3], b[3,0], abs_tol=0.0001) == True
        assert math.isclose(a[4], b[4,0], abs_tol=0.0001) == True
        assert math.isclose(a[5], b[0,1], abs_tol=0.0001) == True
        assert math.isclose(a[6], b[1,1], abs_tol=0.0001) == True
        assert math.isclose(a[7], b[2,1], abs_tol=0.0001) == True
        assert math.isclose(a[8], b[3,1], abs_tol=0.0001) == True
        assert math.isclose(a[9], b[4,1], abs_tol=0.0001) == True
        assert math.isclose(a[10], b[0,2], abs_tol=0.0001) == True
        assert math.isclose(a[11], b[1,2], abs_tol=0.0001) == True
        assert math.isclose(a[12], b[2,2], abs_tol=0.0001) == True
        assert math.isclose(a[13], b[3,2], abs_tol=0.0001) == True
        assert math.isclose(a[14], b[4,2], abs_tol=0.0001) == True
        assert math.isclose(a[15], b[0,3], abs_tol=0.0001) == True
        assert math.isclose(a[16], b[1,3], abs_tol=0.0001) == True
        assert math.isclose(a[17], b[2,3], abs_tol=0.0001) == True
        assert math.isclose(a[18], b[3,3], abs_tol=0.0001) == True
        assert math.isclose(a[19], b[4,3], abs_tol=0.0001) == True
        assert math.isclose(a[20], b[0,4], abs_tol=0.0001) == True
        assert math.isclose(a[21], b[1,4], abs_tol=0.0001) == True
        assert math.isclose(a[22], b[2,4], abs_tol=0.0001) == True
        assert math.isclose(a[23], b[3,4], abs_tol=0.0001) == True
        assert math.isclose(a[24], b[4,4], abs_tol=0.0001) == True

    # Error case: converting an integer NumPy array to a double PyArmadillo matrix
    def test_numpy_3(self):
        b = np.array([
        [61198,   201990,   19678,  -493936,  -126745],
        [437242,  58956,  -149362,  -45465,   296153],
        [-492474,  31309,   314156,   419733,   68317],
        [336352,   411541,   458476,  -393139,  -135040],
        [239585,  -428913,  -406953,  -291020,  -353768]
        ])
        with pytest.raises(RuntimeError):
            a = mat(b)

    # Error case: converting a double NumPy array to an integer PyArmadillo matrix
    def test_numpy_4(self):
        b = np.array([
        [0.061198,   0.201990,   0.019678,  -0.493936,  -0.126745],
        [0.437242,   0.058956,  -0.149362,  -0.045465,   0.296153],
        [-0.492474,  -0.031309,   0.314156,   0.419733,   0.068317],
        [0.336352,   0.411541,   0.458476,  -0.393139,  -0.135040],
        [0.239585,  -0.428913,  -0.406953,  -0.291020,  -0.353768]
        ])
        with pytest.raises(RuntimeError):
            a = umat(b)
    