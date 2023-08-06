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
#include "indexing/cube_indices.hpp"

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    arma::subview_cube<typename T::elem_type> get_subcube(const T &cube, const std::tuple<py::slice, py::slice, py::slice> coords) {
        py::slice row_slice = std::get<0>(coords);
        py::slice col_slice = std::get<1>(coords);
        py::slice slice_slice = std::get<2>(coords);
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> indices = cube_get_indices<T>(cube, row_slice, col_slice, slice_slice);
        return cube.subcube(arma::span(std::get<0>(indices), std::get<1>(indices)), arma::span(std::get<2>(indices), std::get<3>(indices)), arma::span(std::get<4>(indices), std::get<5>(indices)));
    }

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_subcube_size(const T &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        arma::uword slice = std::get<2>(coords);
        arma::SizeCube size = std::get<3>(coords);
        return cube(row, col, slice, size);
    }

    template<typename T, typename U>
    void set_subcube(T &cube, std::tuple<py::slice, py::slice, py::slice> coords, U item) {
        py::slice row_slice = std::get<0>(coords);
        py::slice col_slice = std::get<1>(coords);
        py::slice slice_slice = std::get<2>(coords);
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> indices = cube_get_indices<T>(cube, row_slice, col_slice, slice_slice);
        cube.subcube(arma::span(std::get<0>(indices), std::get<1>(indices)), arma::span(std::get<2>(indices), std::get<3>(indices)), arma::span(std::get<4>(indices), std::get<5>(indices))) = item;
    }

    template<typename T, typename U>
    void set_subcube_size(T &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, U item) {
        arma::uword row = std::get<0>(coords);
        arma::uword col = std::get<1>(coords);
        arma::uword slice = std::get<2>(coords);
        arma::SizeCube size = std::get<3>(coords);
        cube(row, col, slice, size) = item;
    }

    template arma::subview_cube<double> get_subcube<arma::Cube<double>>(const arma::Cube<double> &cube, const std::tuple<py::slice, py::slice, py::slice> coords);
    template arma::subview_cube<double> get_subcube_size<arma::Cube<double>>(const arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords);
    template void set_subcube<arma::Cube<double>, arma::Cube<double>>(arma::Cube<double> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Cube<double> item);
    template void set_subcube_size<arma::Cube<double>, arma::Cube<double>>(arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Cube<double> item);
    template void set_subcube<arma::Cube<double>, arma::Mat<double>>(arma::Cube<double> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Mat<double> item);
    template void set_subcube_size<arma::Cube<double>, arma::Mat<double>>(arma::Cube<double> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Mat<double> item);

    template arma::subview_cube<float> get_subcube<arma::Cube<float>>(const arma::Cube<float> &cube, const std::tuple<py::slice, py::slice, py::slice> coords);
    template arma::subview_cube<float> get_subcube_size<arma::Cube<float>>(const arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords);
    template void set_subcube<arma::Cube<float>, arma::Cube<float>>(arma::Cube<float> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Cube<float> item);
    template void set_subcube_size<arma::Cube<float>, arma::Cube<float>>(arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Cube<float> item);
    template void set_subcube<arma::Cube<float>, arma::Mat<float>>(arma::Cube<float> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Mat<float> item);
    template void set_subcube_size<arma::Cube<float>, arma::Mat<float>>(arma::Cube<float> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Mat<float> item);

    template arma::subview_cube<arma::cx_double> get_subcube<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const std::tuple<py::slice, py::slice, py::slice> coords);
    template arma::subview_cube<arma::cx_double> get_subcube_size<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords);
    template void set_subcube<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Cube<arma::cx_double> item);
    template void set_subcube_size<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Cube<arma::cx_double> item);
    template void set_subcube<arma::Cube<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Mat<arma::cx_double> item);
    template void set_subcube_size<arma::Cube<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Mat<arma::cx_double> item);

    template arma::subview_cube<arma::cx_float> get_subcube<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, const std::tuple<py::slice, py::slice, py::slice> coords);
    template arma::subview_cube<arma::cx_float> get_subcube_size<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords);
    template void set_subcube<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Cube<arma::cx_float> item);
    template void set_subcube_size<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Cube<arma::cx_float> item);
    template void set_subcube<arma::Cube<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Mat<arma::cx_float> item);
    template void set_subcube_size<arma::Cube<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Mat<arma::cx_float> item);

    template arma::subview_cube<arma::uword> get_subcube<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, const std::tuple<py::slice, py::slice, py::slice> coords);
    template arma::subview_cube<arma::uword> get_subcube_size<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords);
    template void set_subcube<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(arma::Cube<arma::uword> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Cube<arma::uword> item);
    template void set_subcube_size<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Cube<arma::uword> item);
    template void set_subcube<arma::Cube<arma::uword>, arma::Mat<arma::uword>>(arma::Cube<arma::uword> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Mat<arma::uword> item);
    template void set_subcube_size<arma::Cube<arma::uword>, arma::Mat<arma::uword>>(arma::Cube<arma::uword> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Mat<arma::uword> item);

    template arma::subview_cube<arma::sword> get_subcube<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, const std::tuple<py::slice, py::slice, py::slice> coords);
    template arma::subview_cube<arma::sword> get_subcube_size<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords);
    template void set_subcube<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(arma::Cube<arma::sword> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Cube<arma::sword> item);
    template void set_subcube_size<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Cube<arma::sword> item);
    template void set_subcube<arma::Cube<arma::sword>, arma::Mat<arma::sword>>(arma::Cube<arma::sword> &cube, std::tuple<py::slice, py::slice, py::slice> coords, arma::Mat<arma::sword> item);
    template void set_subcube_size<arma::Cube<arma::sword>, arma::Mat<arma::sword>>(arma::Cube<arma::sword> &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, arma::Mat<arma::sword> item);
}

