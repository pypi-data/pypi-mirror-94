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
    // Expose reversing (flipping) functions
    template<typename T>
    void expose_rev(py::module &m) {
        using Class = arma::Mat<T>;
        m.def("reverse", [](const Class &matrix, const arma::uword &dim) {
            return reverse(matrix, dim).eval();
        }, "matrix"_a, "dim"_a)
        .def("reverse", [](const Class &matrix) {
            Class output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = reverse(tmp);
                if (matrix.is_rowvec()) {
                    output = output.t();
                }
            } else {
                output = reverse(matrix, 0);
            }
            return output;
        })
        .def("fliplr", [](const Class &matrix) { return fliplr(matrix).eval(); })

        .def("flipud", [](const Class &matrix) { return flipud(matrix).eval(); });
    }

    template void expose_rev<double>(py::module &m);
    template void expose_rev<float>(py::module &m);
    template void expose_rev<arma::cx_double>(py::module &m);
    template void expose_rev<arma::cx_float>(py::module &m);
    template void expose_rev<arma::uword>(py::module &m);
    template void expose_rev<arma::sword>(py::module &m);
}