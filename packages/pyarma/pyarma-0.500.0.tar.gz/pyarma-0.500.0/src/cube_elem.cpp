// Copyright 2020-2021 Jason Rumengan, Terry Yue Zhuo
// Copyright 2020-2021 Data61/CSIRO
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ------------------------------------------------------------------------

#define ARMA_DONT_PRINT_ERRORS
#include "pybind11/pybind11.h"
#include "armadillo"

namespace pyarma {
    template<typename T>
    arma::subview_elem1<typename T::elem_type, arma::umat> cube_get_elem(const T &cube, const arma::Mat<arma::uword> &indices) {
        return cube.elem(indices);
    }

    template<typename T>
    void cube_set_elem(T &cube, arma::Mat<arma::uword> &indices, arma::Mat<typename T::elem_type> item) {
        cube.elem(indices) = item;
    }

    template arma::subview_elem1<double, arma::umat> cube_get_elem<arma::Cube<double>>(const arma::Cube<double> &cube, const arma::umat &indices);
    template arma::subview_elem1<float, arma::umat> cube_get_elem<arma::Cube<float>>(const arma::Cube<float> &cube, const arma::umat &indices);
    template arma::subview_elem1<arma::cx_double, arma::umat> cube_get_elem<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const arma::umat &indices);
    template arma::subview_elem1<arma::cx_float, arma::umat> cube_get_elem<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, const arma::umat &indices);
    template arma::subview_elem1<arma::uword, arma::umat> cube_get_elem<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, const arma::umat &indices);
    template arma::subview_elem1<arma::sword, arma::umat> cube_get_elem<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, const arma::umat &indices);

    template void cube_set_elem<arma::Cube<double>>(arma::Cube<double> &cube, arma::umat &indices, arma::Mat<double> item);
    template void cube_set_elem<arma::Cube<float>>(arma::Cube<float> &cube, arma::umat &indices, arma::Mat<float> item);
    template void cube_set_elem<arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, arma::umat &indices, arma::Mat<arma::cx_double> item);
    template void cube_set_elem<arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, arma::umat &indices, arma::Mat<arma::cx_float> item);
    template void cube_set_elem<arma::Cube<arma::uword>>(arma::Cube<arma::uword> &cube, arma::umat &indices, arma::Mat<arma::uword> item);
    template void cube_set_elem<arma::Cube<arma::sword>>(arma::Cube<arma::sword> &cube, arma::umat &indices, arma::Mat<arma::sword> item);
}
