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
#include "indexing/subcube.hpp"

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    arma::subview_cube<typename T::elem_type> get_slice(const T &cube, const std::tuple<py::slice, py::slice, arma::uword> coord) {
        py::slice row_slice = std::get<0>(coord);
        py::slice col_slice = std::get<1>(coord);
        arma::uword slice = std::get<2>(coord);
        return get_subcube<T>(cube, std::make_tuple(row_slice, col_slice, py::slice(py::int_(slice), py::int_(slice), 0)));
    }

    template<typename T, typename U>
    // Same idea with tuple<int, py::slice> that takes one slice or one slice that's column-limited
    void set_slice(T &cube, std::tuple<py::slice, py::slice, arma::uword> coord, U item) {
        py::slice row_slice = std::get<0>(coord);
        py::slice col_slice = std::get<1>(coord);
        arma::uword slice = std::get<2>(coord);
        set_subcube<T, U>(cube, std::make_tuple(row_slice, col_slice, py::slice(py::int_(slice), py::int_(slice), 0)), item);
    }

    template arma::subview_cube<double> get_slice<arma::Cube<double>>(const arma::Cube<double> &cube, const std::tuple<py::slice, py::slice, arma::uword> coord);
    template void set_slice<arma::Cube<double>, arma::Cube<double>>(arma::Cube<double> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Cube<double> item);
    template void set_slice<arma::Cube<double>, arma::Mat<double>>(arma::Cube<double> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Mat<double> item);

    template arma::subview_cube<float> get_slice<arma::Cube<float>>(const arma::Cube<float> &cube, const std::tuple<py::slice, py::slice, arma::uword> coord);
    template void set_slice<arma::Cube<float>, arma::Cube<float>>(arma::Cube<float> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Cube<float> item);
    template void set_slice<arma::Cube<float>, arma::Mat<float>>(arma::Cube<float> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Mat<float> item);

    template arma::subview_cube<arma::cx_double> get_slice<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, const std::tuple<py::slice, py::slice, arma::uword> coord);
    template void set_slice<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Cube<arma::cx_double> item);
    template void set_slice<arma::Cube<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Cube<arma::cx_double> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Mat<arma::cx_double> item);

    template arma::subview_cube<arma::cx_float> get_slice<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, const std::tuple<py::slice, py::slice, arma::uword> coord);
    template void set_slice<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Cube<arma::cx_float> item);
    template void set_slice<arma::Cube<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Cube<arma::cx_float> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Mat<arma::cx_float> item);

    template arma::subview_cube<arma::uword> get_slice<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, const std::tuple<py::slice, py::slice, arma::uword> coord);
    template void set_slice<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(arma::Cube<arma::uword> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Cube<arma::uword> item);
    template void set_slice<arma::Cube<arma::uword>, arma::Mat<arma::uword>>(arma::Cube<arma::uword> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Mat<arma::uword> item);

    template arma::subview_cube<arma::sword> get_slice<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, const std::tuple<py::slice, py::slice, arma::uword> coord);
    template void set_slice<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(arma::Cube<arma::sword> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Cube<arma::sword> item);
    template void set_slice<arma::Cube<arma::sword>, arma::Mat<arma::sword>>(arma::Cube<arma::sword> &cube, std::tuple<py::slice, py::slice, arma::uword> coord, arma::Mat<arma::sword> item);
}
