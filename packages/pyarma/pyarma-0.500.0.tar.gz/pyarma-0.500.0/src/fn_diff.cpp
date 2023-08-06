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
    // Expose diff
    template<typename T>
    void expose_diff(py::module &m) {
        using Class = arma::Mat<T>;
        using PodType = typename arma::get_pod_type<T>::result;

        m.def("diff", [](const Class &matrix, arma::uword k = 1) {
            Class output;
            if (matrix.is_rowvec()) {
                output = diff(matrix, k, 1);
            } else {
                output = diff(matrix, k, 0);
            }
            return output;
        }, "matrix"_a, "k"_a = 1)
        .def("diff", [](const Class &matrix, arma::uword k, const arma::uword &dim) {
            return diff(matrix, k, dim).eval();
        }, "matrix"_a, "k"_a, "dim"_a)
        .def("diff", [](const Class &matrix, const arma::uword &dim) {
            return diff(matrix, 1, dim).eval();
        }, "matrix"_a, "dim"_a);
    }

    template void expose_diff<double>(py::module &m);
    template void expose_diff<float>(py::module &m);
    template void expose_diff<arma::cx_double>(py::module &m);
    template void expose_diff<arma::cx_float>(py::module &m);
    template void expose_diff<arma::uword>(py::module &m);
    template void expose_diff<arma::sword>(py::module &m);
}