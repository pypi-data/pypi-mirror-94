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

#include "pybind11/pybind11.h"
#include "pybind11/iostream.h"
#include "armadillo"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose powmat functions
    template<typename T>
    void expose_powmat(py::module &m) {
        using Class = arma::Mat<T>;
        using CxType = typename std::conditional<arma::is_cx<T>::value, T, std::complex<T>>::type;

        m.def("powmat", [](const Class &matrix, int n) { 
            Class temp;
            powmat(temp, matrix, n);
            return temp;
        }, "matrix"_a, "n"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("powmat", [](const Class &matrix, double n) { 
            arma::Mat<CxType> temp;
            powmat(temp, matrix, n);
            return temp; 
        }, "matrix"_a, "n"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("powmat", [](Class &result, const Class &matrix, int n) {
            return powmat(result, matrix, n);
        }, "result"_a, "matrix"_a, "n"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("powmat", [](arma::Mat<CxType> &result, const Class &matrix, double n) {
            return powmat(result, matrix, n);
        }, "result"_a, "matrix"_a, "n"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>());
    }

    template void expose_powmat<double>(py::module &m);
    template void expose_powmat<float>(py::module &m);
    template void expose_powmat<arma::cx_double>(py::module &m);
    template void expose_powmat<arma::cx_float>(py::module &m);
}