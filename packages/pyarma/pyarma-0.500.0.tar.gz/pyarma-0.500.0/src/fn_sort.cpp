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
    // Expose sorting functions
    template<typename T>
    void expose_sort(py::module &m) {
        using Class = arma::Mat<T>;
        m.def("sort", [](const Class &matrix, const arma::uword &dim) {
            return sort(matrix, "ascend", dim).eval();
        }, "matrix"_a, "dim"_a)
        .def("sort", [](const Class &matrix, std::string sort_direction, const arma::uword &dim) {
            return sort(matrix, sort_direction.c_str(), dim).eval();
        }, "matrix"_a, "sort_direction"_a, "dim"_a)
        .def("sort", [](const Class &matrix, std::string sort_direction = "ascend") {
            Class output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = sort(tmp, sort_direction.c_str());
                if (matrix.is_rowvec()) {
                    output = output.t();
                }
            } else {
                output = arma::sort(matrix, sort_direction.c_str(), 0);
            }
            return output;
        }, "matrix"_a, "sort_direction"_a = "ascend")
        
        .def("sort_index", [](const Class &matrix, std::string sort_direction = "ascend") {
            return sort_index(matrix, sort_direction.c_str()).eval();
        }, "matrix"_a, "sort_direction"_a = "ascend")
        .def("stable_sort_index", [](const Class &matrix, std::string sort_direction = "ascend") {
            return stable_sort_index(matrix, sort_direction.c_str()).eval();
        }, "matrix"_a, "sort_direction"_a = "ascend");
    }

    template void expose_sort<double>(py::module &m);
    template void expose_sort<float>(py::module &m);
    template void expose_sort<arma::cx_double>(py::module &m);
    template void expose_sort<arma::cx_float>(py::module &m);
    template void expose_sort<arma::uword>(py::module &m);
    template void expose_sort<arma::sword>(py::module &m);
}