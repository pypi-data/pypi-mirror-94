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
// // #include "force_inst_cube.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include <type_traits>

namespace py = pybind11;

namespace pyarma {
    // Defines relational operators (==, !=, <, >, <=, >=, &&, ||)
    template<typename T, typename U>
    typename std::enable_if<(arma::is_cx_float<typename T::elem_type>::yes ||
    arma::is_cx_double<typename T::elem_type>::yes)>::type cube_expose_comparisons(py::class_<arma::BaseCube<typename T::elem_type, T>> &py_class) { 
        using Type = typename T::elem_type;
        py_class.def("__eq__", [](const T &l, const U &r) { return (l == r).eval(); }, py::is_operator())
                .def("__eq__", [](const T &l, const Type &r) { return (l == r).eval(); }, py::is_operator())
                .def("__ne__", [](const T &l, const U &r) { return (l != r).eval(); }, py::is_operator())
                .def("__ne__", [](const T &l, const Type &r) { return (l != r).eval(); }, py::is_operator());
    }

    template<typename T, typename U>
    typename std::enable_if<!(arma::is_cx_float<typename T::elem_type>::yes ||
    arma::is_cx_double<typename T::elem_type>::yes)>::type cube_expose_comparisons(py::class_<arma::BaseCube<typename T::elem_type, T>> &py_class) {
        using Type = typename T::elem_type;
        py_class.def("__eq__", [](const T &l, const U &r) { return (l == r).eval(); }, py::is_operator())
                .def("__eq__", [](const T &l, const Type &r) { return (l == r).eval(); }, py::is_operator())
                .def("__ne__", [](const T &l, const U &r) { return (l != r).eval(); }, py::is_operator())
                .def("__ne__", [](const T &l, const Type &r) { return (l != r).eval(); }, py::is_operator())
                .def("__ge__", [](const T &l, const U &r) { return (l >= r).eval(); }, py::is_operator())
                .def("__ge__", [](const T &l, const Type &r) { return (l >= r).eval(); }, py::is_operator())
                .def("__le__", [](const T &l, const U &r) { return (l <= r).eval(); }, py::is_operator())
                .def("__le__", [](const T &l, const Type &r) { return (l <= r).eval(); }, py::is_operator())
                .def("__lt__", [](const T &l, const U &r) { return (l < r).eval(); }, py::is_operator())
                .def("__lt__", [](const T &l, const Type &r) { return (l < r).eval(); }, py::is_operator())
                .def("__gt__", [](const T &l, const U &r) { return (l > r).eval(); }, py::is_operator())
                .def("__gt__", [](const T &l, const Type &r) { return (l > r).eval(); }, py::is_operator())
                .def("__and__", [](const T &l, const U &r) { return (l && r).eval(); }, py::is_operator())
                .def("__or__", [](const T &l, const U &r) { return (l || r).eval(); }, py::is_operator());
    }

    template void cube_expose_comparisons<arma::Cube<double>, arma::Cube<double>>(py::class_<arma::BaseCube<double, arma::Cube<double>>> &py_class);
    template void cube_expose_comparisons<arma::subview_cube<double>, arma::Cube<double>>(py::class_<arma::BaseCube<double, arma::subview_cube<double>>> &py_class);
    // template void cube_expose_comparisons<arma::subview_cube<double>, arma::subview_cube<double>>(py::class_<arma::BaseCube<double, arma::subview_cube<double>>> &py_class);

    template void cube_expose_comparisons<arma::Cube<float>, arma::Cube<float>>(py::class_<arma::BaseCube<float, arma::Cube<float>>> &py_class);
    template void cube_expose_comparisons<arma::subview_cube<float>, arma::Cube<float>>(py::class_<arma::BaseCube<float, arma::subview_cube<float>>> &py_class);
    // template void cube_expose_comparisons<arma::subview_cube<float>, arma::subview_cube<float>>(py::class_<arma::BaseCube<float, arma::subview_cube<float>>> &py_class);

    template void cube_expose_comparisons<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(py::class_<arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> &py_class);
    template void cube_expose_comparisons<arma::subview_cube<arma::cx_double>, arma::Cube<arma::cx_double>>(py::class_<arma::BaseCube<arma::cx_double, arma::subview_cube<arma::cx_double>>> &py_class);
    // template void cube_expose_comparisons<arma::subview_cube<arma::cx_double>, arma::subview_cube<arma::cx_double>>(py::class_<arma::BaseCube<arma::cx_double, arma::subview_cube<arma::cx_double>>> &py_class);

    template void cube_expose_comparisons<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(py::class_<arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> &py_class);
    template void cube_expose_comparisons<arma::subview_cube<arma::cx_float>, arma::Cube<arma::cx_float>>(py::class_<arma::BaseCube<arma::cx_float, arma::subview_cube<arma::cx_float>>> &py_class);
    // template void cube_expose_comparisons<arma::subview_cube<arma::cx_float>, arma::subview_cube<arma::cx_float>>(py::class_<arma::BaseCube<arma::cx_float, arma::subview_cube<arma::cx_float>>> &py_class);

    template void cube_expose_comparisons<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(py::class_<arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> &py_class);
    template void cube_expose_comparisons<arma::subview_cube<arma::uword>, arma::Cube<arma::uword>>(py::class_<arma::BaseCube<arma::uword, arma::subview_cube<arma::uword>>> &py_class);
    // template void cube_expose_comparisons<arma::subview_cube<arma::uword>, arma::subview_cube<arma::uword>>(py::class_<arma::BaseCube<arma::uword, arma::subview_cube<arma::uword>>> &py_class);

    template void cube_expose_comparisons<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(py::class_<arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> &py_class);
    template void cube_expose_comparisons<arma::subview_cube<arma::sword>, arma::Cube<arma::sword>>(py::class_<arma::BaseCube<arma::sword, arma::subview_cube<arma::sword>>> &py_class);
    // template void cube_expose_comparisons<arma::subview_cube<arma::sword>, arma::subview_cube<arma::sword>>(py::class_<arma::BaseCube<arma::sword, arma::subview_cube<arma::sword>>> &py_class);
}