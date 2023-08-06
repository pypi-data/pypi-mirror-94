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
    // Expose expmat functions
    template<typename T>
    void expose_expmat(py::module &m) {
        using Class = arma::Mat<T>;
        m.def("expmat", [](const Class &matrix) { 
            Class temp;
            expmat(temp, matrix);
            return temp;
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("expmat", [](Class &result, const Class &matrix) { 
            return expmat(result, matrix); 
        }, "result"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("expmat_sym", [](const Class &matrix) { 
            Class temp;
            expmat_sym(temp, matrix);
            return temp;
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("expmat_sym", [](Class &result, const Class &matrix) {
            return expmat(result, matrix); 
        }, "result"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>());
    }

    template void expose_expmat<double>(py::module &m);
    template void expose_expmat<float>(py::module &m);
    template void expose_expmat<arma::cx_double>(py::module &m);
    template void expose_expmat<arma::cx_float>(py::module &m);
}