# Copyright 2015 Conrad Sanderson (http://conradsanderson.id.au)
# Copyright 2015 National ICT Australia (NICTA)
#
# Copyright 2020-2021 Jason Rumengan
# Copyright 2020-2021 Data61/CSIRO
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

from pyarma import *
import pytest
import builtins
import math

def initMatrix(n_rows, n_cols):
  m = mat(n_rows, n_cols)

  for ii in range(n_rows):
    for jj in range(n_cols):
      i = int(ii)
      j = int(jj)
      
      m[ii, jj] = 5 * (i % 17) + (i + j) % 13 - 7 * ((j + 2) % 5) + float(i)/float(m.n_rows)

  return m

def checkEigenvectors(coeff):
  # sign of the eigenvectors can be flipped
  assert math.isclose(builtins.abs(coeff[0,0]), 2.2366412109e-01) == True
  assert math.isclose(builtins.abs(coeff[0,1]), 3.1197826828e-01) == True
  assert math.isclose(builtins.abs(coeff[0,2]), 5.1847537613e-02) == True
  assert math.isclose(builtins.abs(coeff[1,0]), 2.2419616512e-01) == True
  assert math.isclose(builtins.abs(coeff[1,1]), 2.7564301912e-01) == True
  assert math.isclose(builtins.abs(coeff[1,2]), 1.0953921221e-01) == True
  assert math.isclose(builtins.abs(coeff[2,0]), 2.2427613980e-01) == True
  assert math.isclose(builtins.abs(coeff[2,1]), 1.6088934501e-01) == True
  assert math.isclose(builtins.abs(coeff[2,2]), 2.3660988967e-01) == True

def checkScore(score):
  assert math.isclose(score[0,0], -1.8538115696e+02) == True
  assert math.isclose(score[0,1], 4.6671842099e+00) == True
  assert math.isclose(score[0,2], 1.1026881736e+01) == True
  assert math.isclose(score[1,0], -1.6144314244e+02) == True
  assert math.isclose(score[1,1], 8.0636602200e+00) == True
  assert math.isclose(score[1,2], 8.5129014856e+00) == True
  assert math.isclose(score[2,0], -1.3750123749e+02) == True
  assert math.isclose(score[2,1], 1.0312494525e+01) == True
  assert math.isclose(score[2,2], 4.5214633042e+00) == True

def checkEigenvalues(latent):
  assert math.isclose(latent[0,0], 1.1989436021e+04) == True
  assert math.isclose(latent[1,0], 9.2136913098e+01) == True
  assert math.isclose(latent[2,0], 7.8335565832e+01) == True
  assert math.isclose(latent[3,0], 2.4204644513e+01) == True
  assert math.isclose(latent[4,0], 2.1302619671e+01) == True
  assert math.isclose(latent[5,0], 1.1615198930e+01) == True
  assert math.isclose(latent[6,0], 1.1040034957e+01) == True
  assert math.isclose(latent[7,0], 7.7918177707e+00) == True
  assert math.isclose(latent[8,0], 7.2862524567e+00) == True
  assert math.isclose(latent[9,0], 6.5039856845e+00) == True


def checkHotteling(tsquared):
  assert math.isclose(tsquared[0,0], 7.1983631370e+02) == True
  assert math.isclose(tsquared[1,0], 6.5616053343e+02) == True
  assert math.isclose(tsquared[2,0], 5.6308987454e+02) == True
  assert math.isclose(tsquared[3,0], 3.6908398978e+02) == True
  assert math.isclose(tsquared[4,0], 2.4632493795e+02) == True
  assert math.isclose(tsquared[5,0], 1.3213013367e+02) == True
  assert math.isclose(tsquared[6,0], 5.7414718234e+01) == True
  assert math.isclose(tsquared[7,0], 1.5157746233e+01) == True
  assert math.isclose(tsquared[8,0], 1.7316032365e+01) == True
  assert math.isclose(tsquared[9,0], 2.9290529527e+01) == True
  assert math.isclose(tsquared[20,0], 2.6159738840e+02) == True

class Test_Princomp:
  def test_fn_princomp_1(self):
    m = initMatrix(1000, 20)
    coeff, score, latent, tsquared = princomp(m)
    checkEigenvectors(coeff)

  def test_fn_princomp_2(self):
    m = initMatrix(1000, 20)
    coeff = mat()
    princomp(coeff, m)
    checkEigenvectors(coeff)

  def test_fn_princomp_3(self):
    m = initMatrix(1000, 20)
    coeff = mat()
    score = mat()
    princomp(coeff, score, m)
    checkScore(score)
    checkEigenvectors(coeff)

  def test_fn_princomp_4(self):
    m = initMatrix(1000, 20)
    coeff = mat()
    score = mat()
    latent = mat()
    princomp(coeff, score, latent, m)
    checkEigenvectors(coeff)
    checkScore(score)
    checkEigenvalues(latent)

  def test_fn_princomp_5(self):
    m = initMatrix(1000, 20)
    coeff = mat()
    score = mat()
    latent = mat()
    tsquared = mat()
    princomp(coeff, score, latent, tsquared, m)
    checkEigenvectors(coeff)
    checkScore(score)
    checkEigenvalues(latent)
    # checkHotteling(tsquared)

  # def test_fn_princomp_6(self):
  #   m = initMatrix(5, 20)
  #   coeff, score, latent, tsquared = princomp(m)
  #   assert math.isclose(builtins.abs(coeff[0,0]), 2.4288979933e-01) == True
  #   assert math.isclose(builtins.abs(coeff[0,1]), 3.9409505019e-16) == True
  #   assert math.isclose(builtins.abs(coeff[0,2]), 1.2516285718e-02) == True
  #   assert math.isclose(builtins.abs(coeff[1,0]), 2.4288979933e-01) == True
  #   assert math.isclose(builtins.abs(coeff[1,1]), 2.9190770799e-16) == True
  #   assert math.isclose(builtins.abs(coeff[1,2]), 1.2516285718e-02) == True
  #   assert math.isclose(builtins.abs(coeff[2,0]), 2.4288979933e-01) == True
  #   assert math.isclose(builtins.abs(coeff[2,1]), 3.4719806003e-17) == True
  #   assert math.isclose(builtins.abs(coeff[2,2]), 1.2516285718e-02) == True
  #   assert math.isclose(builtins.abs(coeff(19,19)), 9.5528446175e-01).epsilon(0.01) == True
