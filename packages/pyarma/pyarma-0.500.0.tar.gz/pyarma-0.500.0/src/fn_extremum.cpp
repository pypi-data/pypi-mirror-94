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
    // Expose extremum functions ((index)_min/max)
    template<typename T>
    void expose_extremum(py::module &m) {
        // standalone (index_)min/max
        m.def("min", [](const arma::Mat<T> &matrix) {
            arma::Mat<T> output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                arma::Mat<T> tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = min(tmp);
            } else {
                output = min(matrix, 0);
            }
            return output;
        }, "matrix"_a)
        .def("min", [](const arma::Mat<T> &matrix, const arma::uword &dim) {
            return arma::min(matrix, dim).eval();
        }, "matrix"_a, "dim"_a) 
        .def("min", [](const arma::Mat<T> &a, const arma::Mat<T> &b) {
            return arma::min(a, b).eval();
        })

        .def("max", [](const arma::Mat<T> &matrix) {
            arma::Mat<T> output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                arma::Mat<T> tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = max(tmp);
            } else {
                output = max(matrix, 0);
            }
            return output;
        }, "matrix"_a)
        .def("max", [](const arma::Mat<T> &matrix, const arma::uword &dim) {
            return arma::max(matrix, dim).eval();
        }, "matrix"_a, "dim"_a)
        .def("max", [](const arma::Mat<T> &a, const arma::Mat<T> &b) {
            return arma::max(a, b).eval();
        })

        .def("index_min", [](const arma::Mat<T> &matrix) {
            arma::umat output;

            if (matrix.is_vec()) {
                arma::Mat<T> tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = index_min(tmp);
            } else {
                output = index_min(matrix, 0);
            }
            return output;
        }, "matrix"_a)
        .def("index_min", [](const arma::Mat<T> &matrix, const arma::uword &dim) {
            return arma::index_min(matrix, dim).eval();
        })

        .def("index_max", [](const arma::Mat<T> &matrix) {
            arma::umat output;

            if (matrix.is_vec()) {
                arma::Mat<T> tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = index_max(tmp);
            } else {
                output = index_max(matrix, 0);
            }
            return output;
        }, "matrix"_a)
        .def("index_max", [](const arma::Mat<T> &matrix, arma::uword &dim) {
            return arma::index_max(matrix, dim).eval();
        });
    }

    template void expose_extremum<double>(py::module &m);
    template void expose_extremum<float>(py::module &m);
    template void expose_extremum<arma::cx_double>(py::module &m);
    template void expose_extremum<arma::cx_float>(py::module &m);
    template void expose_extremum<arma::uword>(py::module &m);
    template void expose_extremum<arma::sword>(py::module &m);
}