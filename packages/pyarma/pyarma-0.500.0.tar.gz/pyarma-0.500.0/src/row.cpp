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

#include "pybind11/pybind11.h"
#include "armadillo"
#include "indexing/submatrix.hpp"

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    arma::subview<typename T::elem_type> get_row(const T &matrix, const std::tuple<arma::uword, py::slice> coords) {
        arma::uword row = std::get<0>(coords);
        py::slice col_slice = std::get<1>(coords);
        return get_submatrix<T>(matrix, std::make_tuple(py::slice(py::int_(row), py::int_(row), 0), col_slice));
    }

    template<typename T>
    void set_row(T &matrix, std::tuple<arma::uword, py::slice> coords, arma::Mat<typename T::elem_type> item) {
        py::slice col_slice = std::get<1>(coords);
        arma::uword row = std::get<0>(coords);
        set_submatrix<T>(matrix, std::make_tuple(py::slice(py::int_(row), py::int_(row), 0), col_slice), item);
    }

    template arma::subview<double> get_row<arma::mat>(const arma::mat &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<float> get_row<arma::fmat>(const arma::fmat &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::cx_double> get_row<arma::cx_mat>(const arma::cx_mat &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::cx_float> get_row<arma::cx_fmat>(const arma::cx_fmat &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::uword> get_row<arma::umat>(const arma::umat &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::sword> get_row<arma::imat>(const arma::imat &matrix, const std::tuple<arma::uword, py::slice> coords);

    template arma::subview<double> get_row<arma::subview<double>>(const arma::subview<double> &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<float> get_row<arma::subview<float>>(const arma::subview<float> &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::cx_double> get_row<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::cx_float> get_row<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::uword> get_row<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, const std::tuple<arma::uword, py::slice> coords);
    template arma::subview<arma::sword> get_row<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, const std::tuple<arma::uword, py::slice> coords);

    template void set_row<arma::mat>(arma::mat &matrix, std::tuple<arma::uword, py::slice> coords, arma::mat item);
    template void set_row<arma::fmat>(arma::fmat &matrix, std::tuple<arma::uword, py::slice> coords, arma::fmat item);
    template void set_row<arma::cx_mat>(arma::cx_mat &matrix, std::tuple<arma::uword, py::slice> coords, arma::cx_mat item);
    template void set_row<arma::cx_fmat>(arma::cx_fmat &matrix, std::tuple<arma::uword, py::slice> coords, arma::cx_fmat item);
    template void set_row<arma::umat>(arma::umat &matrix, std::tuple<arma::uword, py::slice> coords, arma::umat item);
    template void set_row<arma::imat>(arma::imat &matrix, std::tuple<arma::uword, py::slice> coords, arma::imat item);

    template void set_row<arma::subview<double>>(arma::subview<double> &matrix, std::tuple<arma::uword, py::slice> coords, arma::Mat<double> item);
    template void set_row<arma::subview<float>>(arma::subview<float> &matrix, std::tuple<arma::uword, py::slice> coords, arma::Mat<float> item);
    template void set_row<arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &matrix, std::tuple<arma::uword, py::slice> coords, arma::Mat<arma::cx_double> item);
    template void set_row<arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &matrix, std::tuple<arma::uword, py::slice> coords, arma::Mat<arma::cx_float> item);
    template void set_row<arma::subview<arma::uword>>(arma::subview<arma::uword> &matrix, std::tuple<arma::uword, py::slice> coords, arma::Mat<arma::uword> item);
    template void set_row<arma::subview<arma::sword>>(arma::subview<arma::sword> &matrix, std::tuple<arma::uword, py::slice> coords, arma::Mat<arma::sword> item);
}
