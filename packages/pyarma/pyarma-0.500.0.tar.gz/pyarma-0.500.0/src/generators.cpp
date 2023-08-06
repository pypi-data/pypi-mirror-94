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
#include <limits>

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose vector generators
    void expose_generators(py::module &m) {
        m.def("linspace", [](double start, double end, arma::uword N = 100) {
            return arma::Mat<double>(arma::linspace(start, end, N));
        }, "start"_a, "end"_a, "N"_a)
        
        .def("logspace", [](double A, double B, arma::uword N = 100) {
            return arma::Mat<double>(arma::logspace(A, B, N));
        }, "A"_a, "B"_a, "N"_a)

        .def("regspace", [](double start, double delta, double end) {
            return arma::Mat<double>(arma::regspace(start, delta, end));
        })
        .def("regspace", [](double start, double end) {
            return arma::Mat<double>(arma::regspace(start, end));
        })
        
        .def("randperm", [](arma::uword N, arma::uword M) {
            return arma::Mat<arma::uword>(arma::randperm(N, M));
        })
        .def("randperm", [](arma::uword N) {
            return arma::Mat<arma::uword>(arma::randperm(N));
        })
        
        .def("randg", [](arma::distr_param distr_param = arma::distr_param(1, 1)) { 
            return arma::randg<double>(distr_param); 
        }, "distr_param"_a = arma::distr_param(1, 1))
        .def("randg", [](arma::uword n_elem, arma::distr_param distr_param = arma::distr_param(1, 1)) { 
            return arma::mat(arma::randg<arma::vec>(n_elem, distr_param)); 
        }, "n_elem"_a, "distr_param"_a = arma::distr_param(1, 1))
        .def("randg", [](arma::uword n_rows, arma::uword n_cols, arma::distr_param distr_param = arma::distr_param(1, 1)) { 
            return arma::randg<arma::mat>(n_rows, n_cols, distr_param); 
        }, "n_rows"_a, "n_cols"_a, "distr_param"_a = arma::distr_param(1, 1))
        .def("randg", [](arma::uword n_rows, arma::uword n_cols, arma::uword n_slices, arma::distr_param distr_param = arma::distr_param(1, 1)) { 
            return arma::randg<arma::cube>(n_rows, n_cols, n_slices, distr_param); 
        }, "n_rows"_a, "n_cols"_a, "n_slices"_a, "distr_param"_a = arma::distr_param(1, 1))
        .def("randg", [](arma::SizeMat size, arma::distr_param distr_param = arma::distr_param(1, 1)) { 
            return arma::randg<arma::mat>(size, distr_param); 
        }, "size"_a, "distr_param"_a = arma::distr_param(1, 1))
        .def("randg", [](arma::SizeCube size, arma::distr_param distr_param = arma::distr_param(1, 1)) { 
            return arma::randg<arma::cube>(size, distr_param); 
        }, "size"_a, "distr_param"_a = arma::distr_param(1, 1))
        
        .def("randi", [](arma::distr_param distr_param = arma::distr_param(0, std::numeric_limits<int>::max())) { 
            return arma::randi<int>(distr_param); 
        }, "distr_param"_a = arma::distr_param(0, std::numeric_limits<int>::max()))
        .def("randi", [](arma::uword n_elem, arma::distr_param distr_param = arma::distr_param(0, std::numeric_limits<int>::max())) { 
            return arma::imat(arma::randi<arma::ivec>(n_elem, distr_param)); 
        }, "n_elem"_a, "distr_param"_a = arma::distr_param(0, std::numeric_limits<int>::max()))
        .def("randi", [](arma::uword n_rows, arma::uword n_cols, arma::distr_param distr_param = arma::distr_param(0, std::numeric_limits<int>::max())) { 
            return arma::randi<arma::imat>(n_rows, n_cols, distr_param); 
        }, "n_rows"_a, "n_cols"_a, "distr_param"_a = arma::distr_param(0, std::numeric_limits<int>::max()))
        .def("randi", [](arma::uword n_rows, arma::uword n_cols, arma::uword n_slices, arma::distr_param distr_param = arma::distr_param(0, std::numeric_limits<int>::max())) { 
            return arma::randi<arma::icube>(n_rows, n_cols, n_slices, distr_param); 
        }, "n_rows"_a, "n_cols"_a, "n_slices"_a, "distr_param"_a = arma::distr_param(0, std::numeric_limits<int>::max()))
        .def("randi", [](arma::SizeMat size, arma::distr_param distr_param = arma::distr_param(0, std::numeric_limits<int>::max())) { 
            return arma::randi<arma::imat>(size, distr_param); 
        }, "size"_a, "distr_param"_a = arma::distr_param(0, std::numeric_limits<int>::max()))
        .def("randi", [](arma::SizeCube size, arma::distr_param distr_param = arma::distr_param(0, std::numeric_limits<int>::max())) { 
            return arma::randi<arma::icube>(size, distr_param); 
        }, "size"_a, "distr_param"_a = arma::distr_param(0, std::numeric_limits<int>::max()))
        
        .def("randu", []() { return arma::randu(); })
        .def("randu", [](arma::uword n_elem) { return arma::randu<arma::mat>(n_elem).eval(); })
        .def("randu", [](arma::uword n_rows, arma::uword n_cols) { return arma::randu<arma::mat>(n_rows, n_cols).eval(); })
        .def("randu", [](arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { return arma::randu<arma::cube>(n_rows, n_cols, n_slices).eval(); })
        .def("randu", [](arma::SizeMat &size) { return arma::randu<arma::mat>(size).eval(); })
        .def("randu", [](arma::SizeCube &size) { return arma::randu<arma::cube>(size).eval(); })
        
        .def("randn", []() { return arma::randn(); })
        .def("randn", [](arma::uword n_elem) { return arma::randn<arma::mat>(n_elem).eval(); })
        .def("randn", [](arma::uword n_rows, arma::uword n_cols) { return arma::randn<arma::mat>(n_rows, n_cols).eval(); })
        .def("randn", [](arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { return arma::randn<arma::cube>(n_rows, n_cols, n_slices).eval(); })
        .def("randn", [](arma::SizeMat &size) { return arma::randn<arma::mat>(size).eval(); })
        .def("randn", [](arma::SizeCube &size) { return arma::randn<arma::cube>(size).eval(); })
        
        .def("ones", [](arma::uword n_elem) { return arma::ones<arma::mat>(n_elem).eval(); })
        .def("ones", [](arma::uword n_rows, arma::uword n_cols) { return arma::ones<arma::mat>(n_rows, n_cols).eval(); })
        .def("ones", [](arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { return arma::ones<arma::cube>(n_rows, n_cols, n_slices).eval(); })
        .def("ones", [](arma::SizeMat &size) { return arma::ones<arma::mat>(size).eval(); })
        .def("ones", [](arma::SizeCube &size) { return arma::ones<arma::cube>(size).eval(); })
        
        .def("zeros", [](arma::uword n_elem) { return arma::zeros<arma::mat>(n_elem).eval(); })
        .def("zeros", [](arma::uword n_rows, arma::uword n_cols) { return arma::zeros<arma::mat>(n_rows, n_cols).eval(); })
        .def("zeros", [](arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { return arma::zeros<arma::cube>(n_rows, n_cols, n_slices).eval(); })
        .def("zeros", [](arma::SizeMat &size) { return arma::zeros<arma::mat>(size).eval(); })
        .def("zeros", [](arma::SizeCube &size) { return arma::zeros<arma::cube>(size).eval(); })
        
        .def("eye", [](arma::uword n_rows, arma::uword n_cols) { return arma::eye<arma::mat>(n_rows, n_cols).eval(); })
        .def("eye", [](arma::SizeMat &size) { return arma::eye<arma::mat>(size).eval(); });
    }
}