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
using namespace pybind11::literals;

namespace pyarma {
    // Expose additive functions
    template<typename T>
    void expose_additive(py::module &m) {
        using Class = arma::Mat<T>;
        m.def("sum", [](const Class &matrix) { 
            Class output;

            if (matrix.n_elem == 0) {
                output.set_size(1,1);
                output[0] = T(0);
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output.set_size(1,1);
                output[0] = arma::accu(tmp);
            } else {
                output = arma::sum(matrix, 0);
            }
            return output;
        }, "matrix"_a)
        .def("sum", [](const Class &matrix, const arma::uword &dim) { 
            return arma::sum(matrix, dim).eval(); 
        }, "matrix"_a, "dim"_a)
        .def("accu", [](const Class &matrix) { return arma::accu(matrix); })
        .def("cumsum", [](const Class &matrix) {
            Class output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = cumsum(tmp);
                if (matrix.is_rowvec()) {
                    output = output.t();
                }
            } else {
                output = arma::cumsum(matrix, 0);
            }
            return output;
        })
        .def("cumsum", [](const Class &matrix, const arma::uword &dim) { return cumsum(matrix, dim).eval(); })

        .def("cumprod", [](const Class &matrix) {
            Class output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = cumprod(tmp);
                if (matrix.is_rowvec()) {
                    output = output.t();
                }
            } else {
                output = arma::cumprod(matrix, 0);
            }
            return output;
        })
        .def("cumprod", [](const Class &matrix, const arma::uword &dim) { return cumprod(matrix, dim).eval(); });
    }

    template void expose_additive<double>(py::module &m);
    template void expose_additive<float>(py::module &m);
    template void expose_additive<arma::cx_double>(py::module &m);
    template void expose_additive<arma::cx_float>(py::module &m);
    template void expose_additive<arma::uword>(py::module &m);
    template void expose_additive<arma::sword>(py::module &m);
}