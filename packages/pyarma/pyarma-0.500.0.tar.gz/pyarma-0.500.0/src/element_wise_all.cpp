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

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose element-wise functions
    template<typename T>
    void expose_element_wise_all(py::module &m) { 
        m.def("exp", [](const T &object) { return arma::exp(object).eval(); })
        .def("log", [](const T &object) { return arma::log(object).eval(); })
        .def("pow", [](const T &object, typename T::elem_type &p) { return arma::pow(object, p).eval(); })
        .def("pow", [](const T &object, typename T::pod_type &p) { return arma::pow(object, p).eval(); })
        .def("floor", [](const T &object) { return arma::floor(object).eval(); })
        .def("sign", [](const T &object) { return arma::sign(object).eval(); })
        .def("exp2", [](const T &object) { return arma::exp2(object).eval(); })
        .def("log2", [](const T &object) { return arma::log2(object).eval(); })
        .def("exp10", [](const T &object) { return arma::exp10(object).eval(); })
        .def("log10", [](const T &object) { return arma::log10(object).eval(); })
        .def("square", [](const T &object) { return arma::square(object).eval(); })
        .def("sqrt", [](const T &object) { return arma::sqrt(object).eval(); })
        .def("ceil", [](const T &object) { return arma::ceil(object).eval(); })
        .def("round", [](const T &object) { return arma::round(object).eval(); })
        .def("trunc", [](const T &object) { return arma::trunc(object).eval(); });
    }

    template void expose_element_wise_all<arma::mat>(py::module &m);
    // template void expose_element_wise_all<arma::subview<double>>(py::module &m);
    // template void expose_element_wise_all<arma::diagview<double>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise_all<arma::Mat<float>>(py::module &m);
    // template void expose_element_wise_all<arma::subview<float>>(py::module &m);
    // template void expose_element_wise_all<arma::diagview<float>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise_all<arma::Mat<arma::cx_double>>(py::module &m);
    // template void expose_element_wise_all<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_element_wise_all<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);
 
    template void expose_element_wise_all<arma::Mat<arma::cx_float>>(py::module &m);
    // template void expose_element_wise_all<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_element_wise_all<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise_all<arma::Mat<arma::uword>>(py::module &m);
    // template void expose_element_wise_all<arma::subview<arma::uword>>(py::module &m);
    // template void expose_element_wise_all<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise_all<arma::Mat<arma::sword>>(py::module &m);
    // template void expose_element_wise_all<arma::subview<arma::sword>>(py::module &m);
    // template void expose_element_wise_all<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);

    template void expose_element_wise_all<arma::Cube<double>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_cube<double>>(py::module &m);

    template void expose_element_wise_all<arma::Cube<float>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_cube<float>>(py::module &m);

    template void expose_element_wise_all<arma::Cube<arma::cx_double>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_cube<arma::cx_double>>(py::module &m);

    template void expose_element_wise_all<arma::Cube<arma::cx_float>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_cube<arma::cx_float>>(py::module &m);

    template void expose_element_wise_all<arma::Cube<arma::uword>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_cube<arma::uword>>(py::module &m);

    template void expose_element_wise_all<arma::Cube<arma::sword>>(py::module &m);
    // template void expose_element_wise_all<arma::subview_cube<arma::sword>>(py::module &m);
}