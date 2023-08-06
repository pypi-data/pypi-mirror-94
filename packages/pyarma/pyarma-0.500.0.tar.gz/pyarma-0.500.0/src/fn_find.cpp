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
    // Expose find functions
    template<typename T>
    void expose_find(py::module &m) {
        using Class = arma::Mat<T>;
        m.def("find", [](const Class &matrix, arma::uword k = 0, std::string s = "first") { return find(matrix, k, s.c_str()).eval(); }, "matrix"_a, "k"_a = 0, "s"_a = "first")

        .def("find_finite", [](const Class &matrix) { return find_finite(matrix).eval(); })

        .def("find_nonfinite", [](const Class &matrix) { return find_nonfinite(matrix).eval(); })

        .def("find_unique", [](const Class &matrix, bool ascending_indices = true) {
            return find_unique(matrix, ascending_indices).eval();
        }, "matrix"_a, "ascending_indices"_a = true);
    }

    template void expose_find<double>(py::module &m);
    template void expose_find<float>(py::module &m);
    template void expose_find<arma::cx_double>(py::module &m);
    template void expose_find<arma::cx_float>(py::module &m);
    template void expose_find<arma::uword>(py::module &m);
    template void expose_find<arma::sword>(py::module &m);
}