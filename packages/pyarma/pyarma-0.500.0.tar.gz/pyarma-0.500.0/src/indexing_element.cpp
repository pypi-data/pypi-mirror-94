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

#include "force_inst_sub.hpp"
#include "force_inst_diag.hpp"
#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "indexing/element.hpp"

namespace py = pybind11;

namespace pyarma {
    // Exposes getters and setters for single elements
    template<typename T, typename Derived>
    void expose_element_get_set(py::class_<Derived, arma::Base<T, Derived>> &py_class) {
        py_class.def("__getitem__", &get_element<Derived>)
                .def("__getitem__", &get_element_single<Derived>)
                .def("__setitem__", &set_element<Derived>)
                .def("__setitem__", &set_element_single<Derived>);
    }

    template void expose_element_get_set<double, arma::mat>(py::class_<arma::mat, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_element_get_set<double, arma::subview<double>>(py::class_<arma::subview<double>, arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_element_get_set<double, arma::diagview<double>>(py::class_<arma::diagview<double>, arma::Base<double, arma::diagview<double>>> &py_class);

    template void expose_element_get_set<float, arma::Mat<float>>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_element_get_set<float, arma::subview<float>>(py::class_<arma::subview<float>, arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_element_get_set<float, arma::diagview<float>>(py::class_<arma::diagview<float>, arma::Base<float, arma::diagview<float>>> &py_class);

    template void expose_element_get_set<arma::cx_double, arma::Mat<arma::cx_double>>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_element_get_set<arma::cx_double, arma::subview<arma::cx_double>>(py::class_<arma::subview<arma::cx_double>, arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    template void expose_element_get_set<arma::cx_double, arma::diagview<arma::cx_double>>(py::class_<arma::diagview<arma::cx_double>, arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
 
    template void expose_element_get_set<arma::cx_float, arma::Mat<arma::cx_float>>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_element_get_set<arma::cx_float, arma::subview<arma::cx_float>>(py::class_<arma::subview<arma::cx_float>, arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    template void expose_element_get_set<arma::cx_float, arma::diagview<arma::cx_float>>(py::class_<arma::diagview<arma::cx_float>, arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);

    template void expose_element_get_set<arma::uword, arma::Mat<arma::uword>>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_element_get_set<arma::uword, arma::subview<arma::uword>>(py::class_<arma::subview<arma::uword>, arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_element_get_set<arma::uword, arma::diagview<arma::uword>>(py::class_<arma::diagview<arma::uword>, arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);

    template void expose_element_get_set<arma::sword, arma::Mat<arma::sword>>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    template void expose_element_get_set<arma::sword, arma::subview<arma::sword>>(py::class_<arma::subview<arma::sword>, arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    template void expose_element_get_set<arma::sword, arma::diagview<arma::sword>>(py::class_<arma::diagview<arma::sword>, arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
}