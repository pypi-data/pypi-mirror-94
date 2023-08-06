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
#include <type_traits>
#include "functions/element_wise_all.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose element-wise functions
    template<typename T>
    typename std::enable_if<!(arma::is_cx<typename T::elem_type>::no)>::type
    expose_element_wise(py::module &m) { 
        expose_element_wise_all<T>(m);
    }

    template<typename T>
    typename std::enable_if<arma::is_cx<typename T::elem_type>::no>::type
    expose_element_wise(py::module &m) {
        expose_element_wise_all<T>(m);

        // exclusive to non-complex types
        m.def("trunc_exp", [](const T &object) { return arma::trunc_exp(object).eval(); })
        .def("trunc_log", [](const T &object) { return arma::trunc_log(object).eval(); })
        .def("expm1", [](const T &object) { return arma::expm1(object).eval(); })
        .def("log1p", [](const T &object) { return arma::log1p(object).eval(); })
        .def("erf", [](const T &object) { return arma::erf(object).eval(); })
        .def("erfc", [](const T &object) { return arma::erfc(object).eval(); })
        .def("lgamma", [](const T &object) { return arma::lgamma(object).eval(); })
        .def("tgamma", [](const T &object) { return arma::tgamma(object).eval(); });
    }

    template void expose_element_wise<arma::mat>(py::module &m);
    // template void expose_element_wise<arma::subview<double>>(py::module &m);
    // template void expose_element_wise<arma::diagview<double>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise<arma::Mat<float>>(py::module &m);
    // template void expose_element_wise<arma::subview<float>>(py::module &m);
    // template void expose_element_wise<arma::diagview<float>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise<arma::Mat<arma::cx_double>>(py::module &m);
    // template void expose_element_wise<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_element_wise<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);
 
    template void expose_element_wise<arma::Mat<arma::cx_float>>(py::module &m);
    // template void expose_element_wise<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_element_wise<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise<arma::Mat<arma::uword>>(py::module &m);
    // template void expose_element_wise<arma::subview<arma::uword>>(py::module &m);
    // template void expose_element_wise<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise<arma::Mat<arma::sword>>(py::module &m);
    // template void expose_element_wise<arma::subview<arma::sword>>(py::module &m);
    // template void expose_element_wise<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_element_wise<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise<arma::Cube<double>>(py::module &m);
    // template void expose_element_wise<arma::subview_cube<double>>(py::module &m);

    template void expose_element_wise<arma::Cube<float>>(py::module &m);
    // template void expose_element_wise<arma::subview_cube<float>>(py::module &m);

    template void expose_element_wise<arma::Cube<arma::cx_double>>(py::module &m);
    // template void expose_element_wise<arma::subview_cube<arma::cx_double>>(py::module &m);

    template void expose_element_wise<arma::Cube<arma::cx_float>>(py::module &m);
    // template void expose_element_wise<arma::subview_cube<arma::cx_float>>(py::module &m);

    template void expose_element_wise<arma::Cube<arma::uword>>(py::module &m);
    // template void expose_element_wise<arma::subview_cube<arma::uword>>(py::module &m);

    template void expose_element_wise<arma::Cube<arma::sword>>(py::module &m);
    // template void expose_element_wise<arma::subview_cube<arma::sword>>(py::module &m);
}