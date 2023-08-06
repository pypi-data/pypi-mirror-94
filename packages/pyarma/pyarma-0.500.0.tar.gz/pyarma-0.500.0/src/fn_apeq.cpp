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

namespace pyarma {
    // Expose approx_equal
    template<typename T>
    void expose_apeq(py::module &m) {
        using Class = arma::Mat<T>;
        using PodType = typename arma::get_pod_type<T>::result;

        m.def("approx_equal", [](const Class &a, const Class &b, const std::string &method, const PodType &tol) {
            return approx_equal(a, b, method.c_str(), tol);
        })
        .def("approx_equal", [](const Class &a, const Class &b, const std::string &method, const PodType &abstol, const PodType &reltol) {
            return approx_equal(a, b, method.c_str(), abstol, reltol);
        });
    }

    template void expose_apeq<double>(py::module &m);
    template void expose_apeq<float>(py::module &m);
    template void expose_apeq<arma::cx_double>(py::module &m);
    template void expose_apeq<arma::cx_float>(py::module &m);
    template void expose_apeq<arma::uword>(py::module &m);
    template void expose_apeq<arma::sword>(py::module &m);
}