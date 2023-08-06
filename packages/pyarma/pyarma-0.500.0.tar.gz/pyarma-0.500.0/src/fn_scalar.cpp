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
#include "pybind11/complex.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose as_scalar
    template<typename T>
    void expose_scalar(py::module &m) {
        using Class = arma::Mat<T>;

        m.def("as_scalar", [](const Class &matrix) { return as_scalar(matrix); });
    }

    template void expose_scalar<double>(py::module &m);
    template void expose_scalar<float>(py::module &m);
    template void expose_scalar<arma::cx_double>(py::module &m);
    template void expose_scalar<arma::cx_float>(py::module &m);
    template void expose_scalar<arma::uword>(py::module &m);
    template void expose_scalar<arma::sword>(py::module &m);
}