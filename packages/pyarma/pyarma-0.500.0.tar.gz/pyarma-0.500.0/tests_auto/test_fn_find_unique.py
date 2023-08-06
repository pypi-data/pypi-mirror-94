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

def test_fn_find_unique_1():

    A = pa.mat([
        [  1,  3,  5,  6,  7 ],
        [  2,  4,  5,  7,  8 ],
        [  3,  5,  5,  6,  9 ],
    ])

    indices = pa.find_unique(A)

    indices2 = pa.umat([ 0, 1, 2, 4, 5, 9, 10, 13, 14 ])
    
    assert indices.n_elem == indices2.n_elem

    same = True

    for i in range(indices.n_elem):
        if indices[i] != indices2[i]:
            same = False
            break

    assert same == True

    unique_elem = pa.mat([ [1], [2], [3], [4], [5], [6], [7], [8], [9] ])

    assert math.isclose(pa.accu(pa.abs(A[indices] - unique_elem)), 0.0, abs_tol=0.0001) == True

def test_fn_find_unique_2():

    A = pa.cx_mat([
        [ complex(1,-1), complex(3, 2), complex(5, 2), complex(6, 1), complex(7,-1) ],
        [ complex(2, 1), complex(4, 4), complex(5, 2), complex(7,-1), complex(8, 1) ],
        [ complex(3, 2), complex(5, 1), complex(5, 3), complex(6, 1), complex(9,-9) ]
    ])

    indices = pa.find_unique(A)

    indices2 = pa.umat([ [0], [1], [2], [4], [5], [6], [8], [9], [10], [13], [14] ])

    assert indices.n_elem == indices2.n_elem

    same = True

    for i in range(indices.n_elem):
        if indices[i] != indices2[i]:
            same = False
            break

    assert same == True

    unique_elem = pa.cx_mat([
        [complex(1,-1)], 
        [complex(2, 1)], 
        [complex(3, 2)], 
        [complex(4, 4)],
        [complex(5, 1)],
        [complex(5, 2)],
        [complex(5, 3)],
        [complex(6, 1)],
        [complex(7,-1)],
        [complex(8, 1)],
        [complex(9,-9)]
    ])

    assert math.isclose(pa.accu(pa.abs(A[indices] - unique_elem)), 0.0, abs_tol=0.0001) == True