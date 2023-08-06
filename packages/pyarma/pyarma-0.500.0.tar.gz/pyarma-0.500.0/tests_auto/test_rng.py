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
from pyarma import *
import math

class Test_RNG:
    # Test set_seed
    def test_rng_1(self):
        pyarma_rng.set_seed(123)
        a = mat(5, 5, fill.randu)
        pyarma_rng.set_seed(123)
        b = mat(5, 5, fill.randu)
        assert math.isclose(a[0], b[0], abs_tol=0.0001) == True
        assert math.isclose(a[1], b[1], abs_tol=0.0001) == True
        assert math.isclose(a[2], b[2], abs_tol=0.0001) == True
        assert math.isclose(a[3], b[3], abs_tol=0.0001) == True
        assert math.isclose(a[4], b[4], abs_tol=0.0001) == True
        assert math.isclose(a[5], b[5], abs_tol=0.0001) == True
        assert math.isclose(a[6], b[6], abs_tol=0.0001) == True
        assert math.isclose(a[7], b[7], abs_tol=0.0001) == True
        assert math.isclose(a[8], b[8], abs_tol=0.0001) == True
        assert math.isclose(a[9], b[9], abs_tol=0.0001) == True
        assert math.isclose(a[10], b[10], abs_tol=0.0001) == True
        assert math.isclose(a[11], b[11], abs_tol=0.0001) == True
        assert math.isclose(a[12], b[12], abs_tol=0.0001) == True
        assert math.isclose(a[13], b[13], abs_tol=0.0001) == True
        assert math.isclose(a[14], b[14], abs_tol=0.0001) == True
        assert math.isclose(a[15], b[15], abs_tol=0.0001) == True
        assert math.isclose(a[16], b[16], abs_tol=0.0001) == True
        assert math.isclose(a[17], b[17], abs_tol=0.0001) == True
        assert math.isclose(a[18], b[18], abs_tol=0.0001) == True
        assert math.isclose(a[19], b[19], abs_tol=0.0001) == True
        assert math.isclose(a[20], b[20], abs_tol=0.0001) == True
        assert math.isclose(a[21], b[21], abs_tol=0.0001) == True
        assert math.isclose(a[22], b[22], abs_tol=0.0001) == True
        assert math.isclose(a[23], b[23], abs_tol=0.0001) == True
        assert math.isclose(a[24], b[24], abs_tol=0.0001) == True

    # Test set_seed edge case (zero)
    def test_rng_2(self):
        pyarma_rng.set_seed(0)
        a = mat(5, 5, fill.randu)
        pyarma_rng.set_seed(0)
        b = mat(5, 5, fill.randu)
        assert math.isclose(a[0], b[0], abs_tol=0.0001) == True
        assert math.isclose(a[1], b[1], abs_tol=0.0001) == True
        assert math.isclose(a[2], b[2], abs_tol=0.0001) == True
        assert math.isclose(a[3], b[3], abs_tol=0.0001) == True
        assert math.isclose(a[4], b[4], abs_tol=0.0001) == True
        assert math.isclose(a[5], b[5], abs_tol=0.0001) == True
        assert math.isclose(a[6], b[6], abs_tol=0.0001) == True
        assert math.isclose(a[7], b[7], abs_tol=0.0001) == True
        assert math.isclose(a[8], b[8], abs_tol=0.0001) == True
        assert math.isclose(a[9], b[9], abs_tol=0.0001) == True
        assert math.isclose(a[10], b[10], abs_tol=0.0001) == True
        assert math.isclose(a[11], b[11], abs_tol=0.0001) == True
        assert math.isclose(a[12], b[12], abs_tol=0.0001) == True
        assert math.isclose(a[13], b[13], abs_tol=0.0001) == True
        assert math.isclose(a[14], b[14], abs_tol=0.0001) == True
        assert math.isclose(a[15], b[15], abs_tol=0.0001) == True
        assert math.isclose(a[16], b[16], abs_tol=0.0001) == True
        assert math.isclose(a[17], b[17], abs_tol=0.0001) == True
        assert math.isclose(a[18], b[18], abs_tol=0.0001) == True
        assert math.isclose(a[19], b[19], abs_tol=0.0001) == True
        assert math.isclose(a[20], b[20], abs_tol=0.0001) == True
        assert math.isclose(a[21], b[21], abs_tol=0.0001) == True
        assert math.isclose(a[22], b[22], abs_tol=0.0001) == True
        assert math.isclose(a[23], b[23], abs_tol=0.0001) == True
        assert math.isclose(a[24], b[24], abs_tol=0.0001) == True

    # Test set_seed edge case (large seed)
    def test_rng_3(self):
        pyarma_rng.set_seed(12345678987654321234)
        a = mat(5, 5, fill.randu)
        pyarma_rng.set_seed(12345678987654321234)
        b = mat(5, 5, fill.randu)
        assert math.isclose(a[0], b[0], abs_tol=0.0001) == True
        assert math.isclose(a[1], b[1], abs_tol=0.0001) == True
        assert math.isclose(a[2], b[2], abs_tol=0.0001) == True
        assert math.isclose(a[3], b[3], abs_tol=0.0001) == True
        assert math.isclose(a[4], b[4], abs_tol=0.0001) == True
        assert math.isclose(a[5], b[5], abs_tol=0.0001) == True
        assert math.isclose(a[6], b[6], abs_tol=0.0001) == True
        assert math.isclose(a[7], b[7], abs_tol=0.0001) == True
        assert math.isclose(a[8], b[8], abs_tol=0.0001) == True
        assert math.isclose(a[9], b[9], abs_tol=0.0001) == True
        assert math.isclose(a[10], b[10], abs_tol=0.0001) == True
        assert math.isclose(a[11], b[11], abs_tol=0.0001) == True
        assert math.isclose(a[12], b[12], abs_tol=0.0001) == True
        assert math.isclose(a[13], b[13], abs_tol=0.0001) == True
        assert math.isclose(a[14], b[14], abs_tol=0.0001) == True
        assert math.isclose(a[15], b[15], abs_tol=0.0001) == True
        assert math.isclose(a[16], b[16], abs_tol=0.0001) == True
        assert math.isclose(a[17], b[17], abs_tol=0.0001) == True
        assert math.isclose(a[18], b[18], abs_tol=0.0001) == True
        assert math.isclose(a[19], b[19], abs_tol=0.0001) == True
        assert math.isclose(a[20], b[20], abs_tol=0.0001) == True
        assert math.isclose(a[21], b[21], abs_tol=0.0001) == True
        assert math.isclose(a[22], b[22], abs_tol=0.0001) == True
        assert math.isclose(a[23], b[23], abs_tol=0.0001) == True
        assert math.isclose(a[24], b[24], abs_tol=0.0001) == True

    # Test set_seed error case (overly large seed)
    def test_rng_4(self):
        with pytest.raises(TypeError):
            pyarma_rng.set_seed(123456789876543212345)

    # Test set_seed error case (string)
    def test_rng_5(self):
        with pytest.raises(TypeError):
            pyarma_rng.set_seed('123456789')

    # Test set_seed error case (negative)
    def test_rng_6(self):
        with pytest.raises(TypeError):
            pyarma_rng.set_seed(-1)

    # Test set_seed error case (float)
    def test_rng_7(self):
        with pytest.raises(TypeError):
            pyarma_rng.set_seed(1.0)

    # Test set_seed error case (inf)
    def test_rng_8(self):
        with pytest.raises(TypeError):
            pyarma_rng.set_seed(math.inf)

    # Test set_seed error case (nan)
    def test_rng_9(self):
        with pytest.raises(TypeError):
            pyarma_rng.set_seed(math.nan)

    # Test set_seed error case (no argument)
    def test_rng_9(self):
        with pytest.raises(TypeError):
            pyarma_rng.set_seed()

    # With random seeds, there's no deteministic way to know whether the test will fail or succeed
    # # Test set_seed_random case
    # def test_rng_10(self):
    #     pyarma_rng.set_seed_random()
    #     a = mat(5, 5, fill.randu)
    #     pyarma_rng.set_seed_random()
    #     b = mat(5, 5, fill.randu)
    #     assert math.isclose(a[0], b[0], abs_tol=0.0001) == False
    #     assert math.isclose(a[1], b[1], abs_tol=0.0001) == False
    #     assert math.isclose(a[2], b[2], abs_tol=0.0001) == False
    #     assert math.isclose(a[3], b[3], abs_tol=0.0001) == False
    #     assert math.isclose(a[4], b[4], abs_tol=0.0001) == False
    #     assert math.isclose(a[5], b[5], abs_tol=0.0001) == False
    #     assert math.isclose(a[6], b[6], abs_tol=0.0001) == False
    #     assert math.isclose(a[7], b[7], abs_tol=0.0001) == False
    #     assert math.isclose(a[8], b[8], abs_tol=0.0001) == False
    #     assert math.isclose(a[9], b[9], abs_tol=0.0001) == False
    #     assert math.isclose(a[10], b[10], abs_tol=0.0001) == False
    #     assert math.isclose(a[11], b[11], abs_tol=0.0001) == False
    #     assert math.isclose(a[12], b[12], abs_tol=0.0001) == False
    #     assert math.isclose(a[13], b[13], abs_tol=0.0001) == False
    #     assert math.isclose(a[14], b[14], abs_tol=0.0001) == False
    #     assert math.isclose(a[15], b[15], abs_tol=0.0001) == False
    #     assert math.isclose(a[16], b[16], abs_tol=0.0001) == False
    #     assert math.isclose(a[17], b[17], abs_tol=0.0001) == False
    #     assert math.isclose(a[18], b[18], abs_tol=0.0001) == False
    #     assert math.isclose(a[19], b[19], abs_tol=0.0001) == False
    #     assert math.isclose(a[20], b[20], abs_tol=0.0001) == False
    #     assert math.isclose(a[21], b[21], abs_tol=0.0001) == False
    #     assert math.isclose(a[22], b[22], abs_tol=0.0001) == False
    #     assert math.isclose(a[23], b[23], abs_tol=0.0001) == False
    #     assert math.isclose(a[24], b[24], abs_tol=0.0001) == False
    