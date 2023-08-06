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

def test_fn_flip_1():

    A = pa.mat("\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
    ")

    A_fliplr = pa.mat("\
        0.051408  -0.126745  -0.493936   0.019678   0.201990   0.061198;\
        0.035437   0.296153  -0.045465  -0.149362   0.058956   0.437242;\
        -0.454499   0.068317   0.419733   0.314156  -0.031309  -0.492474;\
        0.373833  -0.135040  -0.393139   0.458476   0.411541   0.336352;\
        0.258704  -0.353768  -0.291020  -0.406953  -0.428913   0.239585;\
    ")

    A_flipud = pa.mat("\
        0.239585  -0.428913  -0.406953  -0.291020  -0.353768   0.258704;\
        0.336352   0.411541   0.458476  -0.393139  -0.135040   0.373833;\
        -0.492474  -0.031309   0.314156   0.419733   0.068317  -0.454499;\
        0.437242   0.058956  -0.149362  -0.045465   0.296153   0.035437;\
        0.061198   0.201990   0.019678  -0.493936  -0.126745   0.051408;\
    ")

    two_times_A_fliplr = pa.mat("\
        0.102816  -0.253490  -0.987872   0.039356   0.403980   0.122396;\
        0.070874   0.592306  -0.090930  -0.298724   0.117912   0.874484;\
        -0.908998   0.136634   0.839466   0.628312  -0.062618  -0.984948;\
        0.747666  -0.270080  -0.786278   0.916952   0.823082   0.672704;\
        0.517408  -0.707536  -0.582040  -0.813906  -0.857826   0.479170;\
    ")

    two_times_A_flipud = pa.mat("\
        0.479170  -0.857826  -0.813906  -0.582040  -0.707536   0.517408;\
        0.672704   0.823082   0.916952  -0.786278  -0.270080   0.747666;\
        -0.984948  -0.062618   0.628312   0.839466   0.136634  -0.908998;\
        0.874484   0.117912  -0.298724  -0.090930   0.592306   0.070874;\
        0.122396   0.403980   0.039356  -0.987872  -0.253490   0.102816;\
    ")

    assert math.isclose(pa.accu(pa.abs(pa.fliplr(A) - A_fliplr)), 0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.flipud(A) - A_flipud)), 0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(-pa.fliplr(A) + A_fliplr)), 0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(-pa.flipud(A) + A_flipud)), 0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(pa.fliplr(-A) + A_fliplr)), 0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.flipud(-A) + A_flipud)), 0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(2*pa.fliplr(A) - two_times_A_fliplr)), 0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(2*pa.flipud(A) - two_times_A_flipud)), 0, abs_tol=0.0001) == True

    assert math.isclose(pa.accu(pa.abs(pa.fliplr(2*A) - two_times_A_fliplr)), 0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(pa.flipud(2*A) - two_times_A_flipud)), 0, abs_tol=0.0001) == True
