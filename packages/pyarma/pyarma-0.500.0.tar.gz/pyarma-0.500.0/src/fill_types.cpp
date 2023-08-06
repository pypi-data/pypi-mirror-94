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
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    class pyarma_fill {
    public:
        static const arma::fill::fill_class<arma::fill::fill_randu> randu;
        static const arma::fill::fill_class<arma::fill::fill_randn> randn;
        static const arma::fill::fill_class<arma::fill::fill_zeros> zeros;
        static const arma::fill::fill_class<arma::fill::fill_ones> ones;
        static const arma::fill::fill_class<arma::fill::fill_eye> eye;
        static const arma::fill::fill_class<arma::fill::fill_none> none;
    };

    const arma::fill::fill_class<arma::fill::fill_randu> pyarma_fill::randu;
    const arma::fill::fill_class<arma::fill::fill_randn> pyarma_fill::randn;
    const arma::fill::fill_class<arma::fill::fill_zeros> pyarma_fill::zeros;
    const arma::fill::fill_class<arma::fill::fill_ones> pyarma_fill::ones;
    const arma::fill::fill_class<arma::fill::fill_eye> pyarma_fill::eye;
    const arma::fill::fill_class<arma::fill::fill_none> pyarma_fill::none;

    // Expose fill_types
    arma_cold void expose_fill_types(py::module &m) {
        py::class_<arma::fill::fill_class<arma::fill::fill_randu>>(m, "__fill_randu");
        // m.attr("fill_randu") = py::cast(arma::fill::randu);

        py::class_<arma::fill::fill_class<arma::fill::fill_zeros>>(m, "__fill_zeros");
        // m.attr("fill_zeros") = py::cast(arma::fill::zeros);

        py::class_<arma::fill::fill_class<arma::fill::fill_ones>>(m, "__fill_ones");
        // m.attr("fill_ones") = py::cast(arma::fill::ones);
        
        py::class_<arma::fill::fill_class<arma::fill::fill_eye>>(m, "__fill_eye");
        // m.attr("fill_eye") = py::cast(arma::fill::eye);

        py::class_<arma::fill::fill_class<arma::fill::fill_randn>>(m, "__fill_randn");
        // m.attr("fill_randn") = py::cast(arma::fill::randn);

        py::class_<arma::fill::fill_class<arma::fill::fill_none>>(m, "__fill_none");
        // m.attr("fill_none") = py::cast(arma::fill::none);

        py::class_<pyarma_fill>(m, "fill")
            .def_readonly_static("randu", &pyarma_fill::randu)
            .def_readonly_static("randn", &pyarma_fill::randn)
            .def_readonly_static("zeros", &pyarma_fill::zeros)
            .def_readonly_static("ones", &pyarma_fill::ones)
            .def_readonly_static("eye", &pyarma_fill::eye)
            .def_readonly_static("none", &pyarma_fill::none);
    }
}