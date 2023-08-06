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
    // Expose transposition functions
    template<typename T>
    void expose_trans(py::module &m) {
        using Class = arma::Mat<T>;
        m.def("trans", [](const Class &matrix) { return arma::trans(matrix).eval(); })
        .def("strans", [](const Class &matrix) { return arma::strans(matrix).eval(); })
        .def("inplace_trans", [](Class &matrix) {
            inplace_trans(matrix);
        }, "matrix"_a)

        .def("inplace_strans", [](Class &matrix) {
            inplace_strans(matrix);
        }, "matrix"_a);
    }

    template void expose_trans<double>(py::module &m);
    template void expose_trans<float>(py::module &m);
    template void expose_trans<arma::cx_double>(py::module &m);
    template void expose_trans<arma::cx_float>(py::module &m);
    template void expose_trans<arma::uword>(py::module &m);
    template void expose_trans<arma::sword>(py::module &m);
}