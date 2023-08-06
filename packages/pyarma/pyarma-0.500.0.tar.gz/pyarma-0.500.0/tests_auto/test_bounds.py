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

import pytest
import pyarma as pa

def test_mat_bounds():

    n_rows = 5
    n_cols = 6

    A = pa.mat(n_rows, n_cols, pa.fill.zeros)

    try:
        A[n_rows-1,n_cols-1] = 0
    except:
        pytest.fail("Unexpected Error during value assignment!")

    with pytest.raises(RuntimeError):
        A[n_rows,n_cols] = 0