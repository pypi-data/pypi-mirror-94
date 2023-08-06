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
#include "indexing/indices.hpp"

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    arma::subview<typename T::elem_type> get_submatrix(const T &matrix, const std::tuple<py::slice, py::slice> coords) {
        py::slice row_slice = std::get<0>(coords);
        py::slice col_slice = std::get<1>(coords);
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> indices = get_indices<T>(matrix, row_slice, col_slice);
        return matrix(arma::span(std::get<0>(indices), std::get<1>(indices)), arma::span(std::get<2>(indices), std::get<3>(indices)));
    }

    template<typename T>
    void set_submatrix(T &matrix, std::tuple<py::slice, py::slice> coords, arma::Mat<typename T::elem_type> item) {
        py::slice row_slice = std::get<0>(coords);
        py::slice col_slice = std::get<1>(coords);
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> indices = get_indices<T>(matrix, row_slice, col_slice);
        matrix(arma::span(std::get<0>(indices), std::get<1>(indices)), arma::span(std::get<2>(indices), std::get<3>(indices))) = item;
    }

    template arma::subview<double> get_submatrix<arma::mat>(const arma::mat &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<float> get_submatrix<arma::fmat>(const arma::fmat &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::cx_double> get_submatrix<arma::cx_mat>(const arma::cx_mat &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::cx_float> get_submatrix<arma::cx_fmat>(const arma::cx_fmat &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::uword> get_submatrix<arma::umat>(const arma::umat &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::sword> get_submatrix<arma::imat>(const arma::imat &matrix, const std::tuple<py::slice, py::slice> coords);

    template arma::subview<double> get_submatrix<arma::subview<double>>(const arma::subview<double> &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<float> get_submatrix<arma::subview<float>>(const arma::subview<float> &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::cx_double> get_submatrix<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::cx_float> get_submatrix<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::uword> get_submatrix<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, const std::tuple<py::slice, py::slice> coords);
    template arma::subview<arma::sword> get_submatrix<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, const std::tuple<py::slice, py::slice> coords);

    template void set_submatrix<arma::mat>(arma::mat &matrix, std::tuple<py::slice, py::slice> coords, arma::mat item);
    template void set_submatrix<arma::fmat>(arma::fmat &matrix, std::tuple<py::slice, py::slice> coords, arma::fmat item);
    template void set_submatrix<arma::cx_mat>(arma::cx_mat &matrix, std::tuple<py::slice, py::slice> coords, arma::cx_mat item);
    template void set_submatrix<arma::cx_fmat>(arma::cx_fmat &matrix, std::tuple<py::slice, py::slice> coords, arma::cx_fmat item);
    template void set_submatrix<arma::umat>(arma::umat &matrix, std::tuple<py::slice, py::slice> coords, arma::umat item);
    template void set_submatrix<arma::imat>(arma::imat &matrix, std::tuple<py::slice, py::slice> coords, arma::imat item);

    template void set_submatrix<arma::subview<double>>(arma::subview<double> &matrix, std::tuple<py::slice, py::slice> coords, arma::Mat<double> item);
    template void set_submatrix<arma::subview<float>>(arma::subview<float> &matrix, std::tuple<py::slice, py::slice> coords, arma::Mat<float> item);
    template void set_submatrix<arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &matrix, std::tuple<py::slice, py::slice> coords, arma::Mat<arma::cx_double> item);
    template void set_submatrix<arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &matrix, std::tuple<py::slice, py::slice> coords, arma::Mat<arma::cx_float> item);
    template void set_submatrix<arma::subview<arma::uword>>(arma::subview<arma::uword> &matrix, std::tuple<py::slice, py::slice> coords, arma::Mat<arma::uword> item);
    template void set_submatrix<arma::subview<arma::sword>>(arma::subview<arma::sword> &matrix, std::tuple<py::slice, py::slice> coords, arma::Mat<arma::sword> item);
}