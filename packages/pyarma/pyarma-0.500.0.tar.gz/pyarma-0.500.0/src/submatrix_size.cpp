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
// // #include "force_inst_sub.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "indexing/indices.hpp"

namespace py = pybind11;

namespace pyarma {
    // Get/set submatrices using size(X)
    template<typename T>
    arma::subview<typename T::elem_type> get_submatrix_size(const T &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        arma::SizeMat size = std::get<2>(coords);
        return matrix(row, col, size);
    }

    template<typename T, typename U>
    void set_submatrix_size(T &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const U &item) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        arma::SizeMat size = std::get<2>(coords);
        matrix(row, col, size) = item;
    }

    template arma::subview<double> get_submatrix_size<arma::Mat<double>>(const arma::Mat<double> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords);
    // template void set_submatrix_size<arma::Mat<double>, double>(arma::Mat<double> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const double &item);
    template void set_submatrix_size<arma::Mat<double>, arma::Mat<double>>(arma::Mat<double> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::Mat<double> &item);

    template arma::subview<float> get_submatrix_size<arma::Mat<float>>(const arma::Mat<float> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords);
    // template void set_submatrix_size<arma::Mat<float>, float>(arma::Mat<float> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const float &item);
    template void set_submatrix_size<arma::Mat<float>, arma::Mat<float>>(arma::Mat<float> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::Mat<float> &item);

    template arma::subview<arma::cx_double> get_submatrix_size<arma::Mat<arma::cx_double>>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords);
    // template void set_submatrix_size<arma::Mat<arma::cx_double>, arma::cx_double>(arma::Mat<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::cx_double &item);
    template void set_submatrix_size<arma::Mat<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Mat<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::Mat<arma::cx_double> &item);

    template arma::subview<arma::cx_float> get_submatrix_size<arma::Mat<arma::cx_float>>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords);
    // template void set_submatrix_size<arma::Mat<arma::cx_float>, arma::cx_float>(arma::Mat<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::cx_float &item);
    template void set_submatrix_size<arma::Mat<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Mat<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::Mat<arma::cx_float> &item);

    template arma::subview<arma::uword> get_submatrix_size<arma::Mat<arma::uword>>(const arma::Mat<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords);
    // template void set_submatrix_size<arma::Mat<arma::uword>, arma::uword>(arma::Mat<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::uword &item);
    template void set_submatrix_size<arma::Mat<arma::uword>, arma::Mat<arma::uword>>(arma::Mat<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::Mat<arma::uword> &item);

    template arma::subview<arma::sword> get_submatrix_size<arma::Mat<arma::sword>>(const arma::Mat<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords);
    // template void set_submatrix_size<arma::Mat<arma::sword>, arma::sword>(arma::Mat<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::sword &item);
    template void set_submatrix_size<arma::Mat<arma::sword>, arma::Mat<arma::sword>>(arma::Mat<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword, arma::SizeMat> &coords, const arma::Mat<arma::sword> &item);
}