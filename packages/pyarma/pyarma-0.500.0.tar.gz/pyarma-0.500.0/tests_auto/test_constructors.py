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
import pyarma as pa
import math

class Test_Constructors:
    # TODO: Work on all scenarios
    # TODO: add Arma init tests
    # Scenarios: 
    # Normal: test all good values
    # Edge: test valid but large
    # Edge: test zeros
    # Bad: test bad value entries (i.e. strings, no argument, nan, massive values, negative)
    # Normal case: convert PyArmadillo matrix to NumPy array

    # Test string initialisation of matrices
    def test_constructors_1(self):
        a = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768;\
        ")
        assert math.isclose(a[0], 0.061198, abs_tol=0.0001) == True
        assert math.isclose(a[1], 0.437242, abs_tol=0.0001) == True
        assert math.isclose(a[2], -0.492474, abs_tol=0.0001) == True
        assert math.isclose(a[3], 0.336352, abs_tol=0.0001) == True
        assert math.isclose(a[4], 0.239585, abs_tol=0.0001) == True
        assert math.isclose(a[5], 0.201990, abs_tol=0.0001) == True
        assert math.isclose(a[6], 0.058956, abs_tol=0.0001) == True
        assert math.isclose(a[7], -0.031309, abs_tol=0.0001) == True
        assert math.isclose(a[8], 0.411541, abs_tol=0.0001) == True
        assert math.isclose(a[9], -0.428913, abs_tol=0.0001) == True
        assert math.isclose(a[10], 0.019678, abs_tol=0.0001) == True
        assert math.isclose(a[11], -0.149362, abs_tol=0.0001) == True
        assert math.isclose(a[12], 0.314156, abs_tol=0.0001) == True
        assert math.isclose(a[13], 0.458476, abs_tol=0.0001) == True
        assert math.isclose(a[14], -0.406953, abs_tol=0.0001) == True
        assert math.isclose(a[15], -0.493936, abs_tol=0.0001) == True
        assert math.isclose(a[16], -0.045465, abs_tol=0.0001) == True
        assert math.isclose(a[17], 0.419733, abs_tol=0.0001) == True
        assert math.isclose(a[18], -0.393139, abs_tol=0.0001) == True
        assert math.isclose(a[19], -0.291020, abs_tol=0.0001) == True
        assert math.isclose(a[20], -0.126745, abs_tol=0.0001) == True
        assert math.isclose(a[21], 0.296153, abs_tol=0.0001) == True
        assert math.isclose(a[22], 0.068317, abs_tol=0.0001) == True
        assert math.isclose(a[23], -0.135040, abs_tol=0.0001) == True
        assert math.isclose(a[24], -0.353768, abs_tol=0.0001) == True

    # Test element initialisation of matrices
    def test_constructors_2(self):
        a = pa.mat([
        [0.061198,   0.201990,   0.019678,  -0.493936,  -0.126745],
        [0.437242,   0.058956,  -0.149362,  -0.045465,   0.296153],
        [-0.492474,  -0.031309,   0.314156,   0.419733,   0.068317],
        [0.336352,   0.411541,   0.458476,  -0.393139,  -0.135040],
        [0.239585,  -0.428913,  -0.406953,  -0.291020,  -0.353768]
        ])
        assert math.isclose(a[0], 0.061198, abs_tol=0.0001) == True
        assert math.isclose(a[1], 0.437242, abs_tol=0.0001) == True
        assert math.isclose(a[2], -0.492474, abs_tol=0.0001) == True
        assert math.isclose(a[3], 0.336352, abs_tol=0.0001) == True
        assert math.isclose(a[4], 0.239585, abs_tol=0.0001) == True
        assert math.isclose(a[5], 0.201990, abs_tol=0.0001) == True
        assert math.isclose(a[6], 0.058956, abs_tol=0.0001) == True
        assert math.isclose(a[7], -0.031309, abs_tol=0.0001) == True
        assert math.isclose(a[8], 0.411541, abs_tol=0.0001) == True
        assert math.isclose(a[9], -0.428913, abs_tol=0.0001) == True
        assert math.isclose(a[10], 0.019678, abs_tol=0.0001) == True
        assert math.isclose(a[11], -0.149362, abs_tol=0.0001) == True
        assert math.isclose(a[12], 0.314156, abs_tol=0.0001) == True
        assert math.isclose(a[13], 0.458476, abs_tol=0.0001) == True
        assert math.isclose(a[14], -0.406953, abs_tol=0.0001) == True
        assert math.isclose(a[15], -0.493936, abs_tol=0.0001) == True
        assert math.isclose(a[16], -0.045465, abs_tol=0.0001) == True
        assert math.isclose(a[17], 0.419733, abs_tol=0.0001) == True
        assert math.isclose(a[18], -0.393139, abs_tol=0.0001) == True
        assert math.isclose(a[19], -0.291020, abs_tol=0.0001) == True
        assert math.isclose(a[20], -0.126745, abs_tol=0.0001) == True
        assert math.isclose(a[21], 0.296153, abs_tol=0.0001) == True
        assert math.isclose(a[22], 0.068317, abs_tol=0.0001) == True
        assert math.isclose(a[23], -0.135040, abs_tol=0.0001) == True
        assert math.isclose(a[24], -0.353768, abs_tol=0.0001) == True

    # Test element initialisation of row vectors
    def test_constructors_3(self):
        a = pa.mat([0.061198,   0.201990,   0.019678,  -0.493936,  -0.126745])
        assert a.is_rowvec() == True
        assert math.isclose(a[0], 0.061198, abs_tol=0.0001) == True
        assert math.isclose(a[1], 0.201990, abs_tol=0.0001) == True
        assert math.isclose(a[2], 0.019678, abs_tol=0.0001) == True
        assert math.isclose(a[3], -0.493936, abs_tol=0.0001) == True
        assert math.isclose(a[4], -0.126745, abs_tol=0.0001) == True

    # Test element initialisation of column vectors
    def test_constructors_4(self):
        a = pa.mat([[0.061198],   [0.201990],   [0.019678],  [-0.493936],  [-0.126745]])
        assert a.is_colvec() == True
        assert math.isclose(a[0], 0.061198, abs_tol=0.0001) == True
        assert math.isclose(a[1], 0.201990, abs_tol=0.0001) == True
        assert math.isclose(a[2], 0.019678, abs_tol=0.0001) == True
        assert math.isclose(a[3], -0.493936, abs_tol=0.0001) == True
        assert math.isclose(a[4], -0.126745, abs_tol=0.0001) == True

    # Test (rows, columns) initialisation
    def test_constructors_5(self):
        a = pa.mat(5, 5)
        assert math.isclose(a[0], 0, abs_tol=0.0001) == True
        assert math.isclose(a[1], 0, abs_tol=0.0001) == True
        assert math.isclose(a[2], 0, abs_tol=0.0001) == True
        assert math.isclose(a[3], 0, abs_tol=0.0001) == True
        assert math.isclose(a[4], 0, abs_tol=0.0001) == True
        assert math.isclose(a[5], 0, abs_tol=0.0001) == True
        assert math.isclose(a[6], 0, abs_tol=0.0001) == True
        assert math.isclose(a[7], 0, abs_tol=0.0001) == True
        assert math.isclose(a[8], 0, abs_tol=0.0001) == True
        assert math.isclose(a[9], 0, abs_tol=0.0001) == True
        assert math.isclose(a[10], 0, abs_tol=0.0001) == True
        assert math.isclose(a[11], 0, abs_tol=0.0001) == True
        assert math.isclose(a[12], 0, abs_tol=0.0001) == True
        assert math.isclose(a[13], 0, abs_tol=0.0001) == True
        assert math.isclose(a[14], 0, abs_tol=0.0001) == True
        assert math.isclose(a[15], 0, abs_tol=0.0001) == True
        assert math.isclose(a[16], 0, abs_tol=0.0001) == True
        assert math.isclose(a[17], 0, abs_tol=0.0001) == True
        assert math.isclose(a[18], 0, abs_tol=0.0001) == True
        assert math.isclose(a[19], 0, abs_tol=0.0001) == True
        assert math.isclose(a[20], 0, abs_tol=0.0001) == True
        assert math.isclose(a[21], 0, abs_tol=0.0001) == True
        assert math.isclose(a[22], 0, abs_tol=0.0001) == True
        assert math.isclose(a[23], 0, abs_tol=0.0001) == True
        assert math.isclose(a[24], 0, abs_tol=0.0001) == True

    # Test (rows, columns, fill.ones) initialisation
    def test_constructors_6(self):
        a = pa.mat(5, 5, pa.fill.ones)
        assert math.isclose(a[0], 1, abs_tol=0.0001) == True
        assert math.isclose(a[1], 1, abs_tol=0.0001) == True
        assert math.isclose(a[2], 1, abs_tol=0.0001) == True
        assert math.isclose(a[3], 1, abs_tol=0.0001) == True
        assert math.isclose(a[4], 1, abs_tol=0.0001) == True
        assert math.isclose(a[5], 1, abs_tol=0.0001) == True
        assert math.isclose(a[6], 1, abs_tol=0.0001) == True
        assert math.isclose(a[7], 1, abs_tol=0.0001) == True
        assert math.isclose(a[8], 1, abs_tol=0.0001) == True
        assert math.isclose(a[9], 1, abs_tol=0.0001) == True
        assert math.isclose(a[10], 1, abs_tol=0.0001) == True
        assert math.isclose(a[11], 1, abs_tol=0.0001) == True
        assert math.isclose(a[12], 1, abs_tol=0.0001) == True
        assert math.isclose(a[13], 1, abs_tol=0.0001) == True
        assert math.isclose(a[14], 1, abs_tol=0.0001) == True
        assert math.isclose(a[15], 1, abs_tol=0.0001) == True
        assert math.isclose(a[16], 1, abs_tol=0.0001) == True
        assert math.isclose(a[17], 1, abs_tol=0.0001) == True
        assert math.isclose(a[18], 1, abs_tol=0.0001) == True
        assert math.isclose(a[19], 1, abs_tol=0.0001) == True
        assert math.isclose(a[20], 1, abs_tol=0.0001) == True
        assert math.isclose(a[21], 1, abs_tol=0.0001) == True
        assert math.isclose(a[22], 1, abs_tol=0.0001) == True
        assert math.isclose(a[23], 1, abs_tol=0.0001) == True
        assert math.isclose(a[24], 1, abs_tol=0.0001) == True

    # Test (rows, columns, fill.zeros) initialisation
    def test_constructors_7(self):
        a = pa.mat(5, 5, pa.fill.zeros)
        assert math.isclose(a[0], 0, abs_tol=0.0001) == True
        assert math.isclose(a[1], 0, abs_tol=0.0001) == True
        assert math.isclose(a[2], 0, abs_tol=0.0001) == True
        assert math.isclose(a[3], 0, abs_tol=0.0001) == True
        assert math.isclose(a[4], 0, abs_tol=0.0001) == True
        assert math.isclose(a[5], 0, abs_tol=0.0001) == True
        assert math.isclose(a[6], 0, abs_tol=0.0001) == True
        assert math.isclose(a[7], 0, abs_tol=0.0001) == True
        assert math.isclose(a[8], 0, abs_tol=0.0001) == True
        assert math.isclose(a[9], 0, abs_tol=0.0001) == True
        assert math.isclose(a[10], 0, abs_tol=0.0001) == True
        assert math.isclose(a[11], 0, abs_tol=0.0001) == True
        assert math.isclose(a[12], 0, abs_tol=0.0001) == True
        assert math.isclose(a[13], 0, abs_tol=0.0001) == True
        assert math.isclose(a[14], 0, abs_tol=0.0001) == True
        assert math.isclose(a[15], 0, abs_tol=0.0001) == True
        assert math.isclose(a[16], 0, abs_tol=0.0001) == True
        assert math.isclose(a[17], 0, abs_tol=0.0001) == True
        assert math.isclose(a[18], 0, abs_tol=0.0001) == True
        assert math.isclose(a[19], 0, abs_tol=0.0001) == True
        assert math.isclose(a[20], 0, abs_tol=0.0001) == True
        assert math.isclose(a[21], 0, abs_tol=0.0001) == True
        assert math.isclose(a[22], 0, abs_tol=0.0001) == True
        assert math.isclose(a[23], 0, abs_tol=0.0001) == True
        assert math.isclose(a[24], 0, abs_tol=0.0001) == True

    # Test (rows, columns, fill.eye) initialisation
    def test_constructors_6(self):
        a = pa.mat(5, 5, pa.fill.eye)
        assert math.isclose(a[0], 1, abs_tol=0.0001) == True
        assert math.isclose(a[1], 0, abs_tol=0.0001) == True
        assert math.isclose(a[2], 0, abs_tol=0.0001) == True
        assert math.isclose(a[3], 0, abs_tol=0.0001) == True
        assert math.isclose(a[4], 0, abs_tol=0.0001) == True
        assert math.isclose(a[5], 0, abs_tol=0.0001) == True
        assert math.isclose(a[6], 1, abs_tol=0.0001) == True
        assert math.isclose(a[7], 0, abs_tol=0.0001) == True
        assert math.isclose(a[8], 0, abs_tol=0.0001) == True
        assert math.isclose(a[9], 0, abs_tol=0.0001) == True
        assert math.isclose(a[10], 0, abs_tol=0.0001) == True
        assert math.isclose(a[11], 0, abs_tol=0.0001) == True
        assert math.isclose(a[12], 1, abs_tol=0.0001) == True
        assert math.isclose(a[13], 0, abs_tol=0.0001) == True
        assert math.isclose(a[14], 0, abs_tol=0.0001) == True
        assert math.isclose(a[15], 0, abs_tol=0.0001) == True
        assert math.isclose(a[16], 0, abs_tol=0.0001) == True
        assert math.isclose(a[17], 0, abs_tol=0.0001) == True
        assert math.isclose(a[18], 1, abs_tol=0.0001) == True
        assert math.isclose(a[19], 0, abs_tol=0.0001) == True
        assert math.isclose(a[20], 0, abs_tol=0.0001) == True
        assert math.isclose(a[21], 0, abs_tol=0.0001) == True
        assert math.isclose(a[22], 0, abs_tol=0.0001) == True
        assert math.isclose(a[23], 0, abs_tol=0.0001) == True
        assert math.isclose(a[24], 1, abs_tol=0.0001) == True

    # Test (rows, columns, fill.randu) initialisation
    def test_constructors_7(self):
        a = pa.mat(5, 5, pa.fill.randu)
        assert isinstance(a[0], float)
        assert isinstance(a[1], float)
        assert isinstance(a[2], float)
        assert isinstance(a[3], float)
        assert isinstance(a[4], float)
        assert isinstance(a[5], float)
        assert isinstance(a[6], float)
        assert isinstance(a[7], float)
        assert isinstance(a[8], float)
        assert isinstance(a[9], float)
        assert isinstance(a[10], float)
        assert isinstance(a[11], float)
        assert isinstance(a[12], float)
        assert isinstance(a[13], float)
        assert isinstance(a[14], float)
        assert isinstance(a[15], float)
        assert isinstance(a[16], float)
        assert isinstance(a[17], float)
        assert isinstance(a[18], float)
        assert isinstance(a[19], float)
        assert isinstance(a[20], float)
        assert isinstance(a[21], float)
        assert isinstance(a[22], float)
        assert isinstance(a[23], float)
        assert isinstance(a[24], float)
    