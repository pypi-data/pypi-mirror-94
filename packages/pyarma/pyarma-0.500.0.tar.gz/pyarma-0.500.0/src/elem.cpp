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
    arma::subview_elem1<T, arma::umat> get_elem(const arma::Mat<T> &matrix, const arma::umat &indices) {
        return matrix.elem(indices);
    }

    template<typename T>
    void set_elem(arma::Mat<T> &matrix, arma::Mat<arma::uword> indices, arma::Mat<T> item) {
        matrix.elem(indices) = item;
    }

    template arma::subview_elem1<double, arma::umat> get_elem<double>(const arma::Mat<double> &matrix, const arma::umat &indices);
    template arma::subview_elem1<float, arma::umat> get_elem<float>(const arma::Mat<float> &matrix, const arma::umat &indices);
    template arma::subview_elem1<arma::cx_double, arma::umat> get_elem<arma::cx_double>(const arma::Mat<arma::cx_double> &matrix, const arma::umat &indices);
    template arma::subview_elem1<arma::cx_float, arma::umat> get_elem<arma::cx_float>(const arma::Mat<arma::cx_float> &matrix, const arma::umat &indices);
    template arma::subview_elem1<arma::uword, arma::umat> get_elem<arma::uword>(const arma::Mat<arma::uword> &matrix, const arma::umat &indices);
    template arma::subview_elem1<arma::sword, arma::umat> get_elem<arma::sword>(const arma::Mat<arma::sword> &matrix, const arma::umat &indices);

    template void set_elem<double>(arma::Mat<double> &matrix, arma::umat indices, arma::Mat<double> item);
    template void set_elem<float>(arma::Mat<float> &matrix, arma::umat indices, arma::Mat<float> item);
    template void set_elem<arma::cx_double>(arma::Mat<arma::cx_double> &matrix, arma::umat indices, arma::Mat<arma::cx_double> item);
    template void set_elem<arma::cx_float>(arma::Mat<arma::cx_float> &matrix, arma::umat indices, arma::Mat<arma::cx_float> item);
    template void set_elem<arma::uword>(arma::Mat<arma::uword> &matrix, arma::umat indices, arma::Mat<arma::uword> item);
    template void set_elem<arma::sword>(arma::Mat<arma::sword> &matrix, arma::umat indices, arma::Mat<arma::sword> item);
}
