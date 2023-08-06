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
    arma::subview<typename T::elem_type> get_col(const T &matrix, const std::tuple<py::slice, arma::uword> coords) {
        py::slice row_slice = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        return get_submatrix<T>(matrix, std::make_tuple(row_slice, py::slice(py::int_(col), py::int_(col), 0)));
    }

    template<typename T>
    void set_col(T &matrix, const std::tuple<py::slice, arma::uword> coords, arma::Mat<typename T::elem_type> item) {
        py::slice row_slice = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        set_submatrix<T>(matrix, std::make_tuple(row_slice, py::slice(py::int_(col), py::int_(col), 0)), item);
    }

    template arma::subview<double> get_col<arma::mat>(const arma::mat &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<float> get_col<arma::fmat>(const arma::fmat &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::cx_double> get_col<arma::cx_mat>(const arma::cx_mat &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::cx_float> get_col<arma::cx_fmat>(const arma::cx_fmat &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::uword> get_col<arma::umat>(const arma::umat &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::sword> get_col<arma::imat>(const arma::imat &matrix, const std::tuple<py::slice, arma::uword> coords);

    template arma::subview<double> get_col<arma::subview<double>>(const arma::subview<double> &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<float> get_col<arma::subview<float>>(const arma::subview<float> &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::cx_double> get_col<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::cx_float> get_col<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::uword> get_col<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, const std::tuple<py::slice, arma::uword> coords);
    template arma::subview<arma::sword> get_col<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, const std::tuple<py::slice, arma::uword> coords);

    template void set_col<arma::mat>(arma::mat &matrix, std::tuple<py::slice, arma::uword> coords, arma::mat item);
    template void set_col<arma::fmat>(arma::fmat &matrix, std::tuple<py::slice, arma::uword> coords, arma::fmat item);
    template void set_col<arma::cx_mat>(arma::cx_mat &matrix, std::tuple<py::slice, arma::uword> coords, arma::cx_mat item);
    template void set_col<arma::cx_fmat>(arma::cx_fmat &matrix, std::tuple<py::slice, arma::uword> coords, arma::cx_fmat item);
    template void set_col<arma::umat>(arma::umat &matrix, std::tuple<py::slice, arma::uword> coords, arma::umat item);
    template void set_col<arma::imat>(arma::imat &matrix, std::tuple<py::slice, arma::uword> coords, arma::imat item);

    template void set_col<arma::subview<double>>(arma::subview<double> &matrix, std::tuple<py::slice, arma::uword> coords, arma::Mat<double> item);
    template void set_col<arma::subview<float>>(arma::subview<float> &matrix, std::tuple<py::slice, arma::uword> coords, arma::Mat<float> item);
    template void set_col<arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &matrix, std::tuple<py::slice, arma::uword> coords, arma::Mat<arma::cx_double> item);
    template void set_col<arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &matrix, std::tuple<py::slice, arma::uword> coords, arma::Mat<arma::cx_float> item);
    template void set_col<arma::subview<arma::uword>>(arma::subview<arma::uword> &matrix, std::tuple<py::slice, arma::uword> coords, arma::Mat<arma::uword> item);
    template void set_col<arma::subview<arma::sword>>(arma::subview<arma::sword> &matrix, std::tuple<py::slice, arma::uword> coords, arma::Mat<arma::sword> item);
}
