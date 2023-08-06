// Copyright 2020-2021 Jason Rumengan
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
    arma::subview_elem2<T, arma::umat, arma::umat> get_submat(const arma::Mat<T> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices) {
        const arma::Mat<arma::uword> &row_indices = std::get<0>(indices);
        const arma::Mat<arma::uword> &col_indices = std::get<1>(indices);
        return matrix.submat(row_indices, col_indices);
    }

    template<typename T>
    void set_submat(arma::Mat<T> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<T> item) {
        matrix.submat(std::get<0>(indices), std::get<1>(indices)) = item;
    }

    template arma::subview_elem2<double, arma::umat, arma::umat> get_submat<double>(const arma::Mat<double> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<float, arma::umat, arma::umat> get_submat<float>(const arma::Mat<float> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> get_submat<arma::cx_double>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> get_submat<arma::cx_float>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::uword, arma::umat, arma::umat> get_submat<arma::uword>(const arma::Mat<arma::uword> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::sword, arma::umat, arma::umat> get_submat<arma::sword>(const arma::Mat<arma::sword> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices);

    template void set_submat<double>(arma::Mat<double> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<double> item);
    template void set_submat<float>(arma::Mat<float> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<float> item);
    template void set_submat<arma::cx_double>(arma::Mat<arma::cx_double> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<arma::cx_double> item);
    template void set_submat<arma::cx_float>(arma::Mat<arma::cx_float> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<arma::cx_float> item);
    template void set_submat<arma::uword>(arma::Mat<arma::uword> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<arma::uword> item);
    template void set_submat<arma::sword>(arma::Mat<arma::sword> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<arma::sword> item);
}