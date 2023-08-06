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
import pyarma as pa

class Test_Version:
    # Test major version
    def test_version_1(self):
        assert isinstance(pa.pyarma_version.major, int) == True

    # Test minor version
    def test_version_2(self):
        assert isinstance(pa.pyarma_version.major, int) == True

    # Test patch version
    def test_version_3(self):
        assert isinstance(pa.pyarma_version.patch, int) == True

    # Test string
    def test_version_4(self):
        assert isinstance(pa.pyarma_version.as_string(), str) == True
        version = pa.pyarma_version.as_string().split()[0].split('.')
        assert version[0] == str(pa.pyarma_version.major)
        assert version[1] == str(pa.pyarma_version.minor)
        assert version[2] == str(pa.pyarma_version.patch)
    