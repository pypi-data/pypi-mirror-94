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
    // Expose trimat functions
    template<typename T>
    void expose_trimat(py::module &m) {
        using Class = arma::Mat<T>;

        m.def("trimatu", [](const Class &matrix, arma::sword k = 0) {
            return trimatu(matrix, k).eval();
        }, "matrix"_a, "k"_a = 0)
        .def("trimatl", [](const Class &matrix, arma::sword k = 0) {
            return trimatl(matrix, k).eval();
        }, "matrix"_a, "k"_a = 0)

        .def("trimatu_ind", [](const arma::SizeMat &size, arma::sword k = 0) { 
            return arma::umat(trimatu_ind(size, k));
        }, "size"_a, "k"_a = 0)
        .def("trimatl_ind", [](const arma::SizeMat &size, arma::sword k = 0) {
            return arma::umat(trimatl_ind(size, k));
        }, "size"_a, "k"_a = 0);
    }

    template void expose_trimat<double>(py::module &m);
    template void expose_trimat<float>(py::module &m);
    template void expose_trimat<arma::cx_double>(py::module &m);
    template void expose_trimat<arma::cx_float>(py::module &m);
    template void expose_trimat<arma::uword>(py::module &m);
    template void expose_trimat<arma::sword>(py::module &m);
}