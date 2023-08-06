// Copyright 2020-2021 Terry Yue Zhuo
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
    // TODO: convert to subview_slices
    template<typename T>
    arma::Cube<typename T::elem_type> get_slices(const T &cube, const std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices) {
        py::slice row_slice = std::get<0>(indices);
        py::slice col_slice = std::get<1>(indices);
        arma::Mat<arma::uword> slice_indices = std::get<2>(indices);
        py::object st_row = row_slice.attr("start"), sp_row = row_slice.attr("stop");
        py::object st_col = col_slice.attr("start"), sp_col = col_slice.attr("stop");
        bool is_start_row_none = st_row.is(py::none()), is_stop_row_none = sp_row.is(py::none());
        bool is_start_col_none = st_col.is(py::none()), is_stop_col_none = sp_col.is(py::none());
        if (is_start_row_none && is_stop_row_none &&
            is_start_col_none && is_stop_col_none) {
            return cube.slices(slice_indices).eval();
        } else {
            throw py::value_error("Invalid starting symbol. Only ':' is permitted.");
        }
    }

    template<typename T>
    void set_slices(T &cube, std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices, T item) {
        py::slice row_slice = std::get<0>(indices);
        py::slice col_slice = std::get<1>(indices);
        arma::Mat<arma::uword> slice_indices = std::get<2>(indices);
        py::object st_row = row_slice.attr("start"), sp_row = row_slice.attr("stop");
        py::object st_col = col_slice.attr("start"), sp_col = col_slice.attr("stop");
        bool is_start_row_none = st_row.is(py::none()), is_stop_row_none = sp_row.is(py::none());
        bool is_start_col_none = st_col.is(py::none()), is_stop_col_none = sp_col.is(py::none());
        if (is_start_row_none && is_stop_row_none &&
            is_start_col_none && is_stop_col_none) {
            cube.slices(slice_indices) = item;
        } else {
            throw py::value_error("Invalid starting symbol. Only ':' is permitted.");
        }
    }

    template arma::Cube<double> get_slices<arma::Cube<double>>(const arma::Cube<double> &cube, const std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices);
    template arma::Cube<float> get_slices<arma::Cube<float>>(const arma::Cube<float> &cube, const std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices);
    template arma::Cube<arma::cx_double> get_slices<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices);
    template arma::Cube<arma::cx_float> get_slices<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &matrix, const std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices);
    template arma::Cube<arma::uword> get_slices<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &matrix, const std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices);
    template arma::Cube<arma::sword> get_slices<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &matrix, const std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices);

    template void set_slices<arma::Cube<double>>(arma::Cube<double> &matrix, std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices, arma::Cube<double> item);
    template void set_slices<arma::Cube<float>>(arma::Cube<float> &matrix, std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices, arma::Cube<float> item);
    template void set_slices<arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &matrix, std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices, arma::Cube<arma::cx_double> item);
    template void set_slices<arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &matrix, std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices, arma::Cube<arma::cx_float> item);
    template void set_slices<arma::Cube<arma::uword>>(arma::Cube<arma::uword> &matrix, std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices, arma::Cube<arma::uword> item);
    template void set_slices<arma::Cube<arma::sword>>(arma::Cube<arma::sword> &matrix, std::tuple<py::slice, py::slice, arma::Mat<arma::uword>> indices, arma::Cube<arma::sword> item);
}
