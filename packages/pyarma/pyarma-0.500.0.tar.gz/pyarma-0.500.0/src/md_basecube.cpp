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

#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "methods/md_save_cube.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose base cube methods
    template<typename T, typename Derived>
    void expose_base_cube_methods(py::class_<arma::BaseCube<T, Derived>> &py_class) {
        // defining BaseCube methods
        expose_save_cube<T, Derived>(py_class);

        py_class.def("is_finite", [](const Derived &cube) { return cube.is_finite(); })
            .def("has_inf", [](const Derived &cube) { return cube.has_inf(); })
            .def("has_nan", [](const Derived &cube) { return cube.has_nan(); })
            .def("is_zero", [](const Derived &cube, double tolerance) { return cube.is_zero(tolerance); }, "tolerance"_a = 0)
            .def("min", [](const Derived &cube) { return cube.min(); })
            .def("max", [](const Derived &cube) { return cube.max(); })
            .def("index_min", [](const Derived &cube) { return cube.index_min(); })
            .def("index_max", [](const Derived &cube) { return cube.index_max(); })
            .def("is_empty", [](const Derived &cube) { return cube.is_empty(); })
            .def("zeros", [](Derived &cube) { cube.zeros(); })
            .def("ones", [](Derived &cube) { cube.ones(); })
            .def("print", [](const Derived &cube, std::string header = "") {
                std::ostringstream stream;
                cube.print(stream, header);
                py::print(stream.str(), "end"_a="");
            }, "header"_a = "")
            .def("__repr__", [](const Derived &cube) {
                std::ostringstream stream;
                py::object type = py::type::of(py::cast(cube));
                py::str module = type.attr("__module__");
                py::str qualname = type.attr("__qualname__");
                stream << "<" << std::string(module) << "." << std::string(qualname) << " object at " << &cube << ">" << std::endl;
                cube.brief_print(stream);
                return stream.str();
            })
            .def("brief_print", [](const Derived &cube, std::string header = "") {
                std::ostringstream stream;
                cube.brief_print(stream, header);
                py::print(stream.str(), "end"_a="");
            }, "header"_a = "")
            .def("replace", [](Derived &cube, T old_value, T new_value) { cube.replace(old_value, new_value); })
            .def("fill", [](Derived &cube, T value) { cube.fill(value); })
            .def("eval", [](Derived &cube) { return cube.eval(); })

            .def("__neg__", [](const Derived &cube) { return (-cube).eval(); })

            // methods normally exclusive to Cube<T>
            .def("in_range", [](const arma::Cube<T> &cube, const arma::uword i) { return cube.in_range(i); })
            .def("in_range", [](const arma::Cube<T> &cube, const arma::uword row, const arma::uword col, const arma::uword slice) { return cube.in_range(row, col, slice); })
            .def("__len__", [](const arma::Cube<T> &cube) { return cube.size(); })
            .def_property_readonly("n_rows", [](const Derived &cube) { return cube.n_rows; })
            .def_property_readonly("n_cols", [](const Derived &cube) { return cube.n_cols; })
            .def_property_readonly("n_slices", [](const Derived &cube) { return cube.n_slices; })
            .def_property_readonly("n_elem", [](const Derived &cube) { return cube.n_elem; });
    }

    template void expose_base_cube_methods<double, arma::Cube<double>>(py::class_<arma::BaseCube<double, arma::Cube<double>>> &py_class);
    template void expose_base_cube_methods<double, arma::subview_cube<double>>(py::class_<arma::BaseCube<double, arma::subview_cube<double>>> &py_class);

    template void expose_base_cube_methods<float, arma::Cube<float>>(py::class_<arma::BaseCube<float, arma::Cube<float>>> &py_class);
    template void expose_base_cube_methods<float, arma::subview_cube<float>>(py::class_<arma::BaseCube<float, arma::subview_cube<float>>> &py_class);

    template void expose_base_cube_methods<arma::cx_double, arma::Cube<arma::cx_double>>(py::class_<arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> &py_class);
    template void expose_base_cube_methods<arma::cx_double, arma::subview_cube<arma::cx_double>>(py::class_<arma::BaseCube<arma::cx_double, arma::subview_cube<arma::cx_double>>> &py_class);

    template void expose_base_cube_methods<arma::cx_float, arma::Cube<arma::cx_float>>(py::class_<arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> &py_class);
    template void expose_base_cube_methods<arma::cx_float, arma::subview_cube<arma::cx_float>>(py::class_<arma::BaseCube<arma::cx_float, arma::subview_cube<arma::cx_float>>> &py_class);

    template void expose_base_cube_methods<arma::uword, arma::Cube<arma::uword>>(py::class_<arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> &py_class);
    template void expose_base_cube_methods<arma::uword, arma::subview_cube<arma::uword>>(py::class_<arma::BaseCube<arma::uword, arma::subview_cube<arma::uword>>> &py_class);

    template void expose_base_cube_methods<arma::sword, arma::Cube<arma::sword>>(py::class_<arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> &py_class);
    template void expose_base_cube_methods<arma::sword, arma::subview_cube<arma::sword>>(py::class_<arma::BaseCube<arma::sword, arma::subview_cube<arma::sword>>> &py_class);
}