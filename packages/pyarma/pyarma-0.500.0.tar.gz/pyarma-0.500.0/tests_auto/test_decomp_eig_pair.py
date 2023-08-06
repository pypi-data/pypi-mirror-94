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

import math
import pytest
import pyarma as pa

def test_decomp_eig_pair_1():

    A1 = pa.mat("\
        0.840375529753905  -0.600326562133734  -2.138355269439939   0.124049800003193   2.908008030729362;\
        -0.888032082329010   0.489965321173948  -0.839588747336614   1.436696622718939   0.825218894228491;\
        0.100092833139322   0.739363123604474   1.354594328004644  -1.960899999365033   1.378971977916614;\
        -0.544528929990548   1.711887782981555  -1.072155288384252  -0.197698225974150  -1.058180257987362;\
        0.303520794649354  -0.194123535758265   0.960953869740567  -1.207845485259799  -0.468615581100624;\
    ")

    A1_cx = pa.cx_mat("\
        0.840375529753905  -0.600326562133734  -2.138355269439939   0.124049800003193   2.908008030729362;\
        -0.888032082329010   0.489965321173948  -0.839588747336614   1.436696622718939   0.825218894228491;\
        0.100092833139322   0.739363123604474   1.354594328004644  -1.960899999365033   1.378971977916614;\
        -0.544528929990548   1.711887782981555  -1.072155288384252  -0.197698225974150  -1.058180257987362;\
        0.303520794649354  -0.194123535758265   0.960953869740567  -1.207845485259799  -0.468615581100624;\
    ")

    A2 = pa.mat("\
       -0.272469409250187  -0.353849997774433   0.033479882244451   0.022889792751630  -0.979206305167302;\
        1.098424617888623  -0.823586525156853  -1.333677943428106  -0.261995434966092  -1.156401655664002;\
        -0.277871932787639  -1.577057022799202   1.127492278341590  -1.750212368446790  -0.533557109315987;\
        0.701541458163284   0.507974650905946   0.350179410603312  -0.285650971595330  -2.002635735883060;\
        -2.051816299911149   0.281984063670556  -0.299066030332982  -0.831366511567624   0.964229422631627;\
    ")

    A2_cx = pa.cx_mat("\
       -0.272469409250187  -0.353849997774433   0.033479882244451   0.022889792751630  -0.979206305167302;\
        1.098424617888623  -0.823586525156853  -1.333677943428106  -0.261995434966092  -1.156401655664002;\
        -0.277871932787639  -1.577057022799202   1.127492278341590  -1.750212368446790  -0.533557109315987;\
        0.701541458163284   0.507974650905946   0.350179410603312  -0.285650971595330  -2.002635735883060;\
        -2.051816299911149   0.281984063670556  -0.299066030332982  -0.831366511567624   0.964229422631627;\
    ")

    eigvals1 = pa.cx_mat([
        [complex(-2.467066249890401, +0.000000000000000)],
        [complex( 1.483137782196390, +0.595028644066690)],
        [complex( 1.483137782196390, -0.595028644066690)],
        [complex(-0.646831879916377, +0.000000000000000)],
        [complex( 0.099992295916005, +0.000000000000000)]
    ])

    eigvals2 = pa.eig_pair(A1, A2)[0]

    eigvals3 = pa.cx_mat()
    status = pa.eig_pair(eigvals3, A1, A2)

    eigvals4 = pa.cx_mat()
    eigvecs4 = pa.cx_mat()
    pa.eig_pair(eigvals4, eigvecs4, A1, A2)

    eigvals5 = pa.cx_mat()
    leigvecs5 = pa.cx_mat()
    reigvecs5 = pa.cx_mat()
    pa.eig_pair(eigvals5, leigvecs5, reigvecs5, A1, A2)

    B = A2_cx * eigvecs4 * pa.diagmat(eigvals4) * pa.inv(eigvecs4)

    Cl = pa.inv(pa.trans(leigvecs5)) * pa.diagmat(eigvals5) * pa.trans(leigvecs5) * A2_cx
    Cr = A2_cx * reigvecs5 * pa.diagmat(eigvals5) * pa.inv(reigvecs5)

    assert status == True
    assert math.isclose(pa.accu(pa.abs(eigvals2 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals3 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals4 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals5 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A1_cx - B)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A1_cx - Cl)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A1_cx - Cr)), 0.0, abs_tol=0.0001) == True

def test_decomp_eig_pair_2():

    A1 = pa.cx_mat([
        [ complex( 0.520060101455458, +0.451679418928238), complex(-0.133217479507735, -1.361694470870754), complex(-0.293753597735416, +1.039090653504956), complex( 0.307535159238252, -0.195221197898754), complex(-1.332004421315247, +0.826062790211595) ],
        [ complex(-0.020027851642538, -0.130284653145721), complex(-0.714530163787158, +0.455029556444334), complex(-0.847926243637934, -1.117638683265208), complex(-1.257118359352053, -0.217606350143192), complex(-2.329867155805076, +1.526976686733373) ],
        [ complex(-0.034771086028483, +0.183689095861942), complex( 1.351385768426657, -0.848709379933659), complex(-1.120128301243728, +1.260658709120896), complex(-0.865468030554804, -0.303107621351741), complex(-1.449097292838739, +0.466914435684700) ],
        [ complex(-0.798163584564142, -0.476153016619074), complex(-0.224771056052584, -0.334886938964048), complex( 2.525999692118309, +0.660143141046978), complex(-0.176534114231451, +0.023045624425105), complex( 0.333510833065806, -0.209713338388737) ],
        [ complex( 1.018685282128575, +0.862021611556922), complex(-0.589029030720801, +0.552783345944550), complex( 1.655497592887346, -0.067865553542687), complex( 0.791416061628634, +0.051290355848775), complex( 0.391353604432901, +0.625190357087626) ]
    ])

    A2 = pa.cx_mat([
        [ complex( 0.183227263001437, -0.444627816446985), complex( 0.515246335524849, +0.391894209432449), complex(-0.532011376808821, -0.320575506600239), complex(-1.174212331456816, -1.066701398984750), complex(-1.064213412889327, -1.565056014150725) ],
        [ complex(-1.029767543566621, -0.155941035724769), complex( 0.261406324055383, -1.250678906826407), complex( 1.682103594663179, +0.012469041361618), complex(-0.192239517539275, +0.933728162671238), complex( 1.603457298120044, -0.084539479817724) ],
        [ complex( 0.949221831131023, +0.276068253931536), complex(-0.941485770955434, -0.947960922331432), complex(-0.875729346160017, -3.029177341404146), complex(-0.274070229932602, +0.350321001356112), complex( 1.234679146890778, +1.603946350602880) ],
        [ complex( 0.307061919146703, -0.261163645776479), complex(-0.162337672803828, -0.741106093940411), complex(-0.483815050110121, -0.457014640871583), complex( 1.530072514424096, -0.029005763708726), complex(-0.229626450963180, +0.098347774640108) ],
        [ complex( 0.135174942099456, +0.443421912904091), complex(-0.146054634331526, -0.507817550278174), complex(-0.712004549027422, +1.242448406390738), complex(-0.249024742513714, +0.182452167505983), complex(-1.506159703979719, +0.041373613489615) ]
    ])

    eigvals1 = pa.cx_mat([
        [complex(-0.567948485992280, -1.314594536444777)],
        [complex( 1.051873153748018, -0.162676262480913)],
        [complex( 0.610087089288344, +0.562148335263468)],
        [complex(-0.890023643973463, -0.352930772605452)],
        [complex(-0.365476750045154, +0.305826583179225)]
    ])

    eigvals2 = pa.eig_pair(A1, A2)[0]

    eigvals3 = pa.cx_mat()
    status = pa.eig_pair(eigvals3, A1, A2)

    eigvals4 = pa.cx_mat()
    eigvecs4 = pa.cx_mat()
    pa.eig_pair(eigvals4, eigvecs4, A1, A2)

    eigvals5 = pa.cx_mat()
    leigvecs5 = pa.cx_mat()
    reigvecs5 = pa.cx_mat()
    pa.eig_pair(eigvals5, leigvecs5, reigvecs5, A1, A2)

    B = A2 * eigvecs4 * pa.diagmat(eigvals4) * pa.inv(eigvecs4)

    Cl = pa.inv(pa.trans(leigvecs5)) * pa.diagmat(eigvals5) * pa.trans(leigvecs5) * A2
    Cr = A2 * reigvecs5 * pa.diagmat(eigvals5) * pa.inv(reigvecs5)

    assert status == True
    assert math.isclose(pa.accu(pa.abs(eigvals2 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals3 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals4 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(eigvals5 - eigvals1)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A1 - B)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A1 - Cl)), 0.0, abs_tol=0.0001) == True
    assert math.isclose(pa.accu(pa.abs(A1 - Cr)), 0.0, abs_tol=0.0001) == True