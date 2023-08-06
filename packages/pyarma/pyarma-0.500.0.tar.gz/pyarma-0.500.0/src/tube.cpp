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
    arma::subview_cube<typename T::elem_type> get_tube_span(const T &cube, const std::tuple<py::slice, py::slice> coords) {
        py::slice row_slice = std::get<0>(coords);
        py::slice col_slice = std::get<1>(coords);
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> indices = get_indices<T>(cube, row_slice, col_slice);
        return cube.tube(arma::span(std::get<0>(indices), std::get<1>(indices)), arma::span(std::get<2>(indices), std::get<3>(indices)));
    }

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_tube(const T &cube, const std::tuple<arma::uword, arma::uword> coords) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        return cube.tube(row, col);
    }

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_tube_size(const T &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        arma::SizeMat size = std::get<2>(coords);
        return cube.tube(row, col, size);
    }

    template<typename T, typename U>
    void set_tube_span(T &cube, const std::tuple<py::slice, py::slice> coords, const U &item) {
        py::slice row_slice = std::get<0>(coords);
        py::slice col_slice = std::get<1>(coords);
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> indices = get_indices<T>(cube, row_slice, col_slice);
        cube.tube(arma::span(std::get<0>(indices), std::get<1>(indices)), arma::span(std::get<2>(indices), std::get<3>(indices))) = item;
    }

    template<typename T, typename U>
    void set_tube(T &cube, const std::tuple<arma::uword, arma::uword> coords, const U &item) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        cube.tube(row, col) = item;
    }

    template<typename T, typename U>
    void set_tube_size(T &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const U &item) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        arma::SizeMat size = std::get<2>(coords);
        cube.tube(row, col, size) = item;
    }

    template arma::subview_cube<double> get_tube_span<arma::Cube<double>>(const arma::Cube<double> &cube, const std::tuple<py::slice, py::slice> coords);
    template arma::subview_cube<double> get_tube<arma::Cube<double>>(const arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword> coords);
    template arma::subview_cube<double> get_tube_size<arma::Cube<double>>(const arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords);

    template void set_tube_span<arma::Cube<double>, arma::Cube<double>>(arma::Cube<double> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Cube<double> &item);
    template void set_tube<arma::Cube<double>, arma::Cube<double>>(arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Cube<double> &item);
    template void set_tube_size<arma::Cube<double>, arma::Cube<double>>(arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Cube<double> &item);
    
    template void set_tube_span<arma::Cube<double>, arma::Mat<double>>(arma::Cube<double> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Mat<double> &item);
    template void set_tube<arma::Cube<double>, arma::Mat<double>>(arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Mat<double> &item);
    template void set_tube_size<arma::Cube<double>, arma::Mat<double>>(arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Mat<double> &item);

    template arma::subview_cube<float> get_tube_span<arma::Cube<float>>(const arma::Cube<float> &cube, const std::tuple<py::slice, py::slice> coords);
    template arma::subview_cube<float> get_tube<arma::Cube<float>>(const arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword> coords);
    template arma::subview_cube<float> get_tube_size<arma::Cube<float>>(const arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords);

    template void set_tube_span<arma::Cube<float>, arma::Cube<float>>(arma::Cube<float> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Cube<float> &item);
    template void set_tube<arma::Cube<float>, arma::Cube<float>>(arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Cube<float> &item);
    template void set_tube_size<arma::Cube<float>, arma::Cube<float>>(arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Cube<float> &item);

    template void set_tube_span<arma::Cube<float>, arma::Mat<float>>(arma::Cube<float> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Mat<float> &item);
    template void set_tube<arma::Cube<float>, arma::Mat<float>>(arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Mat<float> &item);
    template void set_tube_size<arma::Cube<float>, arma::Mat<float>>(arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Mat<float> &item);

    template arma::subview_cube<arma::cx_double> get_tube_span<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const std::tuple<py::slice, py::slice> coords);
    template arma::subview_cube<arma::cx_double> get_tube<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword> coords);
    template arma::subview_cube<arma::cx_double> get_tube_size<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords);

    template void set_tube_span<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Cube<arma::cx_double> &item);
    template void set_tube<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Cube<arma::cx_double> &item);
    template void set_tube_size<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Cube<arma::cx_double> &item);

    template void set_tube_span<arma::Cube<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Mat<arma::cx_double> &item);
    template void set_tube<arma::Cube<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Mat<arma::cx_double> &item);
    template void set_tube_size<arma::Cube<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Mat<arma::cx_double> &item);

    template arma::subview_cube<arma::cx_float> get_tube_span<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, const std::tuple<py::slice, py::slice> coords);
    template arma::subview_cube<arma::cx_float> get_tube<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword> coords);
    template arma::subview_cube<arma::cx_float> get_tube_size<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords);

    template void set_tube_span<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Cube<arma::cx_float> &item);
    template void set_tube<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Cube<arma::cx_float> &item);
    template void set_tube_size<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Cube<arma::cx_float> &item);

    template void set_tube_span<arma::Cube<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Mat<arma::cx_float> &item);
    template void set_tube<arma::Cube<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Mat<arma::cx_float> &item);
    template void set_tube_size<arma::Cube<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Mat<arma::cx_float> &item);

    template arma::subview_cube<arma::uword> get_tube_span<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, const std::tuple<py::slice, py::slice> coords);
    template arma::subview_cube<arma::uword> get_tube<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword> coords);
    template arma::subview_cube<arma::uword> get_tube_size<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords);

    template void set_tube_span<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Cube<arma::uword> &item);
    template void set_tube<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Cube<arma::uword> &item);
    template void set_tube_size<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Cube<arma::uword> &item);

    template void set_tube_span<arma::Cube<arma::uword>, arma::Mat<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Mat<arma::uword> &item);
    template void set_tube<arma::Cube<arma::uword>, arma::Mat<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Mat<arma::uword> &item);
    template void set_tube_size<arma::Cube<arma::uword>, arma::Mat<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Mat<arma::uword> &item);

    template arma::subview_cube<arma::sword> get_tube_span<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, const std::tuple<py::slice, py::slice> coords);
    template arma::subview_cube<arma::sword> get_tube<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword> coords);
    template arma::subview_cube<arma::sword> get_tube_size<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords);

    template void set_tube_span<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Cube<arma::sword> &item);
    template void set_tube<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Cube<arma::sword> &item);
    template void set_tube_size<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Cube<arma::sword> &item);

    template void set_tube_span<arma::Cube<arma::sword>, arma::Mat<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<py::slice, py::slice> coords, const arma::Mat<arma::sword> &item);
    template void set_tube<arma::Cube<arma::sword>, arma::Mat<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword> coords, const arma::Mat<arma::sword> &item);
    template void set_tube_size<arma::Cube<arma::sword>, arma::Mat<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const arma::Mat<arma::sword> &item);
}

