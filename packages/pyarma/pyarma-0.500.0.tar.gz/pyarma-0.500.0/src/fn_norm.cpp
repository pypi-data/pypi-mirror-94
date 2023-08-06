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
    // Expose norm functions
    template<typename T>
    void expose_norm(py::module &m) {
        using Class = arma::Mat<T>;
        m.def("normalise", [](const Class &matrix, arma::uword p = 2) { 
            arma::Mat<T> output;

            if (matrix.is_rowvec()) {
                output = normalise(matrix, p, 1);
            } else {
                output = normalise(matrix, p, 0);
            }
            return output; 
        }, "matrix"_a, "p"_a = 2)
        .def("normalise", [](const Class &matrix, const arma::uword &p, const arma::uword &dim) { 
            return normalise(matrix, p, dim).eval(); 
        }, "matrix"_a, "p"_a, "dim"_a)
        .def("normalise", [](const Class &matrix, const arma::uword &dim) { 
            return normalise(matrix, 2, dim).eval(); 
        }, "matrix"_a, "dim"_a)
        .def("norm", [](const Class &matrix, arma::uword p = 2) { 
            return norm(matrix, p); 
        }, "matrix"_a, "p"_a = 2)
        .def("norm", [](const Class &matrix, const std::string &p) { return norm(matrix, p.c_str()); })
        
        .def("norm_dot", [](const Class &a, const Class &b) { return norm_dot(a, b); });
    }

    template void expose_norm<double>(py::module &m);
    template void expose_norm<float>(py::module &m);
    template void expose_norm<arma::cx_double>(py::module &m);
    template void expose_norm<arma::cx_float>(py::module &m);
}