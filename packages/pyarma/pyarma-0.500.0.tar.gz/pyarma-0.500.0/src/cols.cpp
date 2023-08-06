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

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    arma::subview_elem2<T, arma::umat, arma::umat> get_cols(const arma::Mat<T> &matrix, const std::tuple<py::slice, arma::Mat<arma::uword> &> &indices) {
        py::slice row_slice = std::get<0>(indices);
        const arma::Mat<arma::uword> &col_indices = std::get<1>(indices);
        py::object st_row = row_slice.attr("start"), sp_row = row_slice.attr("stop");
        bool is_start_none = st_row.is(py::none()), is_stop_none = sp_row.is(py::none());
        if (is_start_none && is_stop_none) {
            return matrix.cols(col_indices);
        } else {
            throw py::value_error("Invalid starting symbol. Only ':' is permitted.");
        }
    }

    template<typename T>
    void set_cols(arma::Mat<T> &matrix, std::tuple<py::slice, arma::Mat<arma::uword> &> indices, arma::Mat<T> item) {
        py::slice row_slice = std::get<0>(indices);
        arma::Mat<arma::uword> col_indices = std::get<1>(indices);
        py::object st_row = row_slice.attr("start"), sp_row = row_slice.attr("stop");
        bool is_start_none = st_row.is(py::none()), is_stop_none = sp_row.is(py::none());
        if (is_start_none && is_stop_none) {
            matrix.cols(col_indices) = item;
        } else {
            throw py::value_error("Invalid starting symbol. Only ':' is permitted.");
        }
    }

    template arma::subview_elem2<double, arma::umat, arma::umat> get_cols<double>(const arma::Mat<double> &matrix, const std::tuple<py::slice, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<float, arma::umat, arma::umat> get_cols<float>(const arma::Mat<float> &matrix, const std::tuple<py::slice, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> get_cols<arma::cx_double>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<py::slice, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> get_cols<arma::cx_float>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<py::slice, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::uword, arma::umat, arma::umat> get_cols<arma::uword>(const arma::Mat<arma::uword> &matrix, const std::tuple<py::slice, arma::Mat<arma::uword> &> &indices);
    template arma::subview_elem2<arma::sword, arma::umat, arma::umat> get_cols<arma::sword>(const arma::Mat<arma::sword> &matrix, const std::tuple<py::slice, arma::Mat<arma::uword> &> &indices);

    template void set_cols<double>(arma::Mat<double> &matrix, std::tuple<py::slice, arma::Mat<arma::uword> &> indices, arma::Mat<double> item);
    template void set_cols<float>(arma::Mat<float> &matrix, std::tuple<py::slice, arma::Mat<arma::uword> &> indices, arma::Mat<float> item);
    template void set_cols<arma::cx_double>(arma::Mat<arma::cx_double> &matrix, std::tuple<py::slice, arma::Mat<arma::uword> &> indices, arma::Mat<arma::cx_double> item);
    template void set_cols<arma::cx_float>(arma::Mat<arma::cx_float> &matrix, std::tuple<py::slice, arma::Mat<arma::uword> &> indices, arma::Mat<arma::cx_float> item);
    template void set_cols<arma::uword>(arma::Mat<arma::uword> &matrix, std::tuple<py::slice, arma::Mat<arma::uword> &> indices, arma::Mat<arma::uword> item);
    template void set_cols<arma::sword>(arma::Mat<arma::sword> &matrix, std::tuple<py::slice, arma::Mat<arma::uword> &> indices, arma::Mat<arma::sword> item);
}