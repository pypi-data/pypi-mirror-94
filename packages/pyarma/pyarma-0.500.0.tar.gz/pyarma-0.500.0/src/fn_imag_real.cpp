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
    // Expose imag/real
    template<typename T>
    void expose_imag_real(py::module &m) {
        // Expose functions
        m.def("imag", [](const arma::Mat<T> &matrix) { return arma::imag(matrix).eval(); })
        .def("real", [](const arma::Mat<T> &matrix) { return arma::real(matrix).eval(); });
    }

    template void expose_imag_real<double>(py::module &m);
    // template void expose_imag_real<double, arma::subview<double>>(py::module &m);
    // template void expose_imag_real<double, arma::diagview<double>>(py::module &m);
    // template void expose_imag_real<double, arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_imag_real<double, arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_imag_real<float>(py::module &m);
    // template void expose_imag_real<float, arma::subview<float>>(py::module &m);
    // template void expose_imag_real<float, arma::diagview<float>>(py::module &m);
    // template void expose_imag_real<float, arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_imag_real<float, arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_imag_real<arma::cx_double>(py::module &m);
    // template void expose_imag_real<arma::cx_double, arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_imag_real<arma::cx_double, arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_imag_real<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_imag_real<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);
 
    template void expose_imag_real<arma::cx_float>(py::module &m);
    // template void expose_imag_real<arma::cx_float, arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_imag_real<arma::cx_float, arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_imag_real<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_imag_real<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_imag_real<arma::uword>(py::module &m);
    // template void expose_imag_real<arma::uword, arma::subview<arma::uword>>(py::module &m);
    // template void expose_imag_real<arma::uword, arma::diagview<arma::uword>>(py::module &m);
    // template void expose_imag_real<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_imag_real<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_imag_real<arma::sword>(py::module &m);
    // template void expose_imag_real<arma::sword, arma::subview<arma::sword>>(py::module &m);
    // template void expose_imag_real<arma::sword, arma::diagview<arma::sword>>(py::module &m);
    // template void expose_imag_real<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_imag_real<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);
}