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

namespace pyarma {
    // Expose dot products
    template<typename T>
    void expose_dot(py::module &m) {
        using Class = arma::Mat<T>;
        using PodType = typename arma::get_pod_type<T>::result;

        m.def("dot", [](const Class &a, const Class &b) { return dot(a, b); })
        .def("cdot", [](const Class &a, const Class &b) { return cdot(a, b); });
    }

    template void expose_dot<double>(py::module &m);
    template void expose_dot<float>(py::module &m);
    template void expose_dot<arma::cx_double>(py::module &m);
    template void expose_dot<arma::cx_float>(py::module &m);
    template void expose_dot<arma::uword>(py::module &m);
    template void expose_dot<arma::sword>(py::module &m);
}