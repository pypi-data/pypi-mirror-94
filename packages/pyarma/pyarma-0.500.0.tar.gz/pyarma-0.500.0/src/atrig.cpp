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

namespace pyarma {
    // Expose arc trigonometric functions
    template<typename T>
    void expose_atrig(py::module &m) {
        m.def("acos", [](const T &object) { return arma::acos(object).eval(); })
        .def("asin", [](const T &object) { return arma::asin(object).eval(); })
        .def("atan", [](const T &object) { return arma::atan(object).eval(); });
    }

    template void expose_atrig<arma::mat>(py::module &m);

    template void expose_atrig<arma::fmat>(py::module &m);

    template void expose_atrig<arma::cx_mat>(py::module &m);

    template void expose_atrig<arma::cx_fmat>(py::module &m);

    template void expose_atrig<arma::umat>(py::module &m);

    template void expose_atrig<arma::imat>(py::module &m);

    template void expose_atrig<arma::Cube<double>>(py::module &m);

    template void expose_atrig<arma::Cube<float>>(py::module &m);

    template void expose_atrig<arma::Cube<arma::cx_double>>(py::module &m);

    template void expose_atrig<arma::Cube<arma::cx_float>>(py::module &m);

    template void expose_atrig<arma::Cube<arma::uword>>(py::module &m);

    template void expose_atrig<arma::Cube<arma::sword>>(py::module &m);
}