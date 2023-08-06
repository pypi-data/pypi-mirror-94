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
    // Expose hyperbolic trigonometric functions
    template<typename T>
    void expose_trigh(py::module &m) {
        m.def("cosh", [](const T &object) { return arma::cosh(object).eval(); })
        .def("sinh", [](const T &object) { return arma::sinh(object).eval(); })
        .def("tanh", [](const T &object) { return arma::tanh(object).eval(); });
    }

    template void expose_trigh<arma::mat>(py::module &m);

    template void expose_trigh<arma::fmat>(py::module &m);

    template void expose_trigh<arma::cx_mat>(py::module &m);

    template void expose_trigh<arma::cx_fmat>(py::module &m);

    template void expose_trigh<arma::umat>(py::module &m);

    template void expose_trigh<arma::imat>(py::module &m);

    template void expose_trigh<arma::Cube<double>>(py::module &m);

    template void expose_trigh<arma::Cube<float>>(py::module &m);

    template void expose_trigh<arma::Cube<arma::cx_double>>(py::module &m);

    template void expose_trigh<arma::Cube<arma::cx_float>>(py::module &m);

    template void expose_trigh<arma::Cube<arma::uword>>(py::module &m);

    template void expose_trigh<arma::Cube<arma::sword>>(py::module &m);
}