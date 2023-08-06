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
    arma::subview_cube<typename T::elem_type> cube_get_col(const T &cube, const std::tuple<py::slice, arma::uword, py::slice> coords) {
        py::slice row_slice = std::get<0>(coords);
        py::slice slice_slice = std::get<2>(coords);
        arma::uword col = std::get<1>(coords);
        return get_subcube<T>(cube, std::make_tuple(row_slice, py::slice(py::int_(col), py::int_(col), 0), slice_slice));
    }

    template<typename T, typename U>
    void cube_set_col(T &cube, std::tuple<py::slice, arma::uword, py::slice> coords, U item) {
        py::slice row_slice = std::get<0>(coords);
        py::slice slice_slice = std::get<2>(coords);
        arma::uword col = std::get<1>(coords);
        set_subcube<T, U>(cube, std::make_tuple(row_slice, py::slice(py::int_(col), py::int_(col), 0), slice_slice), item);
    }

    template arma::subview_cube<double> cube_get_col<arma::cube>(const arma::cube &cube, const std::tuple<py::slice, arma::uword, py::slice> coords);
    template arma::subview_cube<float> cube_get_col<arma::fcube>(const arma::fcube &cube, const std::tuple<py::slice, arma::uword, py::slice> coords);
    template arma::subview_cube<arma::cx_double> cube_get_col<arma::cx_cube>(const arma::cx_cube &cube, const std::tuple<py::slice, arma::uword, py::slice> coords);
    template arma::subview_cube<arma::cx_float> cube_get_col<arma::cx_fcube>(const arma::cx_fcube &cube, const std::tuple<py::slice, arma::uword, py::slice> coords);
    template arma::subview_cube<arma::uword> cube_get_col<arma::ucube>(const arma::ucube &cube, const std::tuple<py::slice, arma::uword, py::slice> coords);
    template arma::subview_cube<arma::sword> cube_get_col<arma::icube>(const arma::icube &cube, const std::tuple<py::slice, arma::uword, py::slice> coords);

    template void cube_set_col<arma::cube>(arma::cube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::cube item);
    template void cube_set_col<arma::fcube>(arma::fcube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::fcube item);
    template void cube_set_col<arma::cx_cube>(arma::cx_cube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::cx_cube item);
    template void cube_set_col<arma::cx_fcube>(arma::cx_fcube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::cx_fcube item);
    template void cube_set_col<arma::ucube>(arma::ucube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::ucube item);
    template void cube_set_col<arma::icube>(arma::icube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::icube item);

    template void cube_set_col<arma::cube>(arma::cube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::mat item);
    template void cube_set_col<arma::fcube>(arma::fcube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::fmat item);
    template void cube_set_col<arma::cx_cube>(arma::cx_cube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::cx_mat item);
    template void cube_set_col<arma::cx_fcube>(arma::cx_fcube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::cx_fmat item);
    template void cube_set_col<arma::ucube>(arma::ucube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::umat item);
    template void cube_set_col<arma::icube>(arma::icube &cube, std::tuple<py::slice, arma::uword, py::slice> coords, arma::imat item);
}
