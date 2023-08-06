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
    // Expose dual-argument trigonometric functions
    template<typename T>
    void expose_dual(py::module &m) {
        // dual-argument trigonometric functions only available for real types
        m.def("atan2", [](const T &l, const T &r) { return atan2(l, r).eval(); })        
        .def("hypot", [](const T &l, const T &r) { return hypot(l, r).eval(); });
    }

    template void expose_dual<arma::mat>(py::module &m);

    template void expose_dual<arma::fmat>(py::module &m);

    template void expose_dual<arma::Cube<double>>(py::module &m);

    template void expose_dual<arma::Cube<float>>(py::module &m);
}