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

// // #include "force_inst_cube.hpp"
#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "indexing/element_cube.hpp"

namespace py = pybind11;

namespace pyarma {
    // Exposes getters and setters for single elements of cubes
    template<typename T, typename Derived>
    void expose_cube_element_get_set(py::class_<Derived, arma::BaseCube<T, Derived>> &py_class) {
        py_class.def("__getitem__", &cube_get_element<Derived>)
                .def("__getitem__", &cube_get_element_single<Derived>)
                .def("__setitem__", &cube_set_element<Derived>)
                .def("__setitem__", &cube_set_element_single<Derived>);
    }

    template void expose_cube_element_get_set<double, arma::cube>(py::class_<arma::cube, arma::BaseCube<double, arma::Cube<double>>> &py_class);
    template void expose_cube_element_get_set<double, arma::subview_cube<double>>(py::class_<arma::subview_cube<double>, arma::BaseCube<double, arma::subview_cube<double>>> &py_class);

    template void expose_cube_element_get_set<float, arma::Cube<float>>(py::class_<arma::Cube<float>, arma::BaseCube<float, arma::Cube<float>>> &py_class);
    template void expose_cube_element_get_set<float, arma::subview_cube<float>>(py::class_<arma::subview_cube<float>, arma::BaseCube<float, arma::subview_cube<float>>> &py_class);

    template void expose_cube_element_get_set<arma::cx_double, arma::Cube<arma::cx_double>>(py::class_<arma::Cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> &py_class);
    template void expose_cube_element_get_set<arma::cx_double, arma::subview_cube<arma::cx_double>>(py::class_<arma::subview_cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::subview_cube<arma::cx_double>>> &py_class);
 
    template void expose_cube_element_get_set<arma::cx_float, arma::Cube<arma::cx_float>>(py::class_<arma::Cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> &py_class);
    template void expose_cube_element_get_set<arma::cx_float, arma::subview_cube<arma::cx_float>>(py::class_<arma::subview_cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::subview_cube<arma::cx_float>>> &py_class);

    template void expose_cube_element_get_set<arma::uword, arma::Cube<arma::uword>>(py::class_<arma::Cube<arma::uword>, arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> &py_class);
    template void expose_cube_element_get_set<arma::uword, arma::subview_cube<arma::uword>>(py::class_<arma::subview_cube<arma::uword>, arma::BaseCube<arma::uword, arma::subview_cube<arma::uword>>> &py_class);

    template void expose_cube_element_get_set<arma::sword, arma::Cube<arma::sword>>(py::class_<arma::Cube<arma::sword>, arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> &py_class);
    template void expose_cube_element_get_set<arma::sword, arma::subview_cube<arma::sword>>(py::class_<arma::subview_cube<arma::sword>, arma::BaseCube<arma::sword, arma::subview_cube<arma::sword>>> &py_class);
}