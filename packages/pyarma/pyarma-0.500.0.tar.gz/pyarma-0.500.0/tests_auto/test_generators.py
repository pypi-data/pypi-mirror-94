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

import pyarma as pa
import pytest

class TestLinspace:
    def test_linspace_1(self):
        assert pa.linspace(0, 5, 6).t() == pa.mat([0, 1, 2, 3, 4, 5])
    def test_linspace_2(self):
        assert pa.linspace(0, 1, 1) == pa.mat([1])
    def test_linspace_3(self):
        with pytest.raises(TypeError):
            pa.linspace(1, 2, -3)
    def test_linspace_4(self):
        with pytest.raises(TypeError):
            pa.linspace(1)
    def test_linspace_5(self):
        with pytest.raises(TypeError):
            pa.linspace("1", "2", "3")
    def test_linspace_6(self):
        with pytest.raises(TypeError):
            pa.linspace(1, 2, 3, 4)

class TestLogspace:
    def test_logspace_1(self):
        assert pa.logspace(0, 5, 6).t() == pa.mat([1, 10, 100, 1000, 10000, 100000])
    def test_logspace_2(self):
        assert pa.logspace(0, 1, 1) == pa.mat([10])
    def test_logspace_3(self):
        with pytest.raises(TypeError):
            pa.logspace(1, 2, -3)
    def test_logspace_4(self):
        with pytest.raises(TypeError):
            pa.logspace(1)
    def test_logspace_5(self):
        with pytest.raises(TypeError):
            pa.logspace("1", "2", "3")
    def test_logspace_6(self):
        with pytest.raises(TypeError):
            pa.logspace(1, 2, 3, 4)

class TestRegspace:
    def test_regspace_1(self):
        assert pa.regspace(2, 2, 10).t() == pa.mat([2, 4, 6, 8, 10])
    def test_regspace_2(self):
        assert pa.regspace(0, -1, -10).t() == pa.mat([0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10])
    def test_regspace_3(self):
        assert pa.regspace(0, 9).t() == pa.mat([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_regspace_4(self):
        with pytest.raises(TypeError):
            pa.regspace(1)
    def test_regspace_5(self):
        with pytest.raises(TypeError):
            pa.regspace(1, 2, 3, 4)
    def test_regspace_6(self):
        with pytest.raises(TypeError):
            pa.regspace("1", "2")

class TestRandperm:
    def test_randperm_1(self):
        with pytest.raises(TypeError):
            pa.randperm(-3)
    def test_randperm_2(self):
        with pytest.raises(TypeError):
            pa.randperm(-3, -4)
    def test_randperm_3(self):
        with pytest.raises(TypeError):
            pa.randperm(3, 4, 5)
    def test_randperm_3(self):
        with pytest.raises(TypeError):
            pa.randperm("3", "4", "5")

class TestRandi:
    def test_randi_1(self):
        assert pa.randi() >= 0
    def test_randi_2(self):
        assert 0 <= pa.randi(pa.distr_param(0,9)) <= 9
    def test_randi_3(self):
        with pytest.raises(TypeError):
            pa.randi(pa.distr_param("1", "2"))
    def test_randi_4(self):
        with pytest.raises(RuntimeError):
            pa.randi(pa.distr_param(-1, -10))
    def test_randi_5(self):
        assert -10 <= pa.randi(pa.distr_param(-10, -1)) <= -1
    def test_randi_6(self):
        assert pa.find((pa.randi(3) >= 0)).n_elem == 3
    def test_randi_7(self):
        assert pa.find(0 <= pa.randi(3, pa.distr_param(0,9))).n_elem == pa.find(pa.randi(3, pa.distr_param(0,9)) <= 9).n_elem
    def test_randi_8(self):
        with pytest.raises(TypeError):
            pa.randi(3, pa.distr_param("1", "2"))
    def test_randi_9(self):
        with pytest.raises(RuntimeError):
            pa.randi(3, pa.distr_param(-1, -10))
    def test_randi_10(self):
        assert pa.find(-10 <= pa.randi(3, pa.distr_param(-10, -1))).n_elem == pa.find(pa.randi(3, pa.distr_param(-10, -1)) <= -1).n_elem
    def test_randi_11(self):
        assert pa.find((pa.randi(3, 3) >= 0)).n_elem == 9
    def test_randi_12(self):
        assert pa.find(0 <= pa.randi(3, 3, pa.distr_param(0,9))).n_elem == pa.find(pa.randi(3, 3, pa.distr_param(0,9)) <= 9).n_elem
    def test_randi_13(self):
        with pytest.raises(TypeError):
            pa.randi(3, 3, pa.distr_param("1", "2"))
    def test_randi_14(self):
        with pytest.raises(RuntimeError):
            pa.randi(3, 3, pa.distr_param(-1, -10))
    def test_randi_15(self):
        assert pa.find(-10 <= pa.randi(3, 3, pa.distr_param(-10, -1))).n_elem == pa.find(pa.randi(3, 3, pa.distr_param(-10, -1)) <= -1).n_elem
    def test_randi_16(self):
        assert pa.find((pa.randi(3, 3, 3) >= 0)).n_elem == 27
    def test_randi_17(self):
        assert pa.find(0 <= pa.randi(3, 3, 3, pa.distr_param(0,9))).n_elem == pa.find(pa.randi(3, 3, 3, pa.distr_param(0,9)) <= 9).n_elem
    def test_randi_18(self):
        with pytest.raises(TypeError):
            pa.randi(3, 3, 3, pa.distr_param("1", "2"))
    def test_randi_19(self):
        with pytest.raises(RuntimeError):
            pa.randi(3, 3, 3, pa.distr_param(-1, -10))
    def test_randi_20(self):
        assert pa.find(-10 <= pa.randi(3, 3, 3, pa.distr_param(-10, -1))).n_elem == pa.find(pa.randi(3, 3, 3, pa.distr_param(-10, -1)) <= -1).n_elem
    def test_randi_21(self):
        assert pa.find((pa.randi(pa.size(pa.mat(3, 3, pa.fill.none))) >= 0)).n_elem == 9
    def test_randi_22(self):
        assert pa.find(0 <= pa.randi(pa.size(pa.mat(3, 3, pa.fill.none)), pa.distr_param(0,9))).n_elem == pa.find(pa.randi(pa.size(pa.mat(3, 3, pa.fill.none)), pa.distr_param(0,9)) <= 9).n_elem
    def test_randi_23(self):
        with pytest.raises(TypeError):
            pa.randi(pa.size(pa.mat(3, 3, pa.fill.none)), pa.distr_param("1", "2"))
    def test_randi_24(self):
        with pytest.raises(RuntimeError):
            pa.randi(pa.size(pa.mat(3, 3, pa.fill.none)), pa.distr_param(-1, -10))
    def test_randi_25(self):
        assert pa.find(-10 <= pa.randi(pa.size(pa.mat(3, 3, pa.fill.none)), pa.distr_param(-10, -1))).n_elem == pa.find(pa.randi(pa.size(pa.mat(3, 3, pa.fill.none)), pa.distr_param(-10, -1)) <= -1).n_elem
    def test_randi_26(self):
        assert pa.find((pa.randi(pa.size(pa.cube(3, 3, 3, pa.fill.none))) >= 0)).n_elem == 27
    def test_randi_27(self):
        assert pa.find(0 <= pa.randi(pa.size(pa.cube(3, 3, 3, pa.fill.none)), pa.distr_param(0,9))).n_elem == pa.find(pa.randi(pa.size(pa.cube(3, 3, 3, pa.fill.none)), pa.distr_param(0,9)) <= 9).n_elem
    def test_randi_28(self):
        with pytest.raises(TypeError):
            pa.randi(pa.size(pa.cube(3, 3, 3, pa.fill.none)), pa.distr_param("1", "2"))
    def test_randi_29(self):
        with pytest.raises(RuntimeError):
            pa.randi(pa.size(pa.cube(3, 3, 3, pa.fill.none)), pa.distr_param(-1, -10))
    def test_randi_30(self):
        assert pa.find(-10 <= pa.randi(pa.size(pa.cube(3, 3, 3, pa.fill.none)), pa.distr_param(-10, -1))).n_elem == pa.find(pa.randi(pa.size(pa.cube(3, 3, 3, pa.fill.none)), pa.distr_param(-10, -1)) <= -1).n_elem
