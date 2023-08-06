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
    // Expose dist_mode options used by GMM
    arma_cold void expose_dist_mode(py::module &m) {
        // Expose dist_mode
        py::class_<arma::gmm_dist_mode>(m, "__dist_mode");

        py::class_<arma::gmm_dist_eucl, arma::gmm_dist_mode>(m, "__eucl_dist");
        py::class_<arma::gmm_dist_prob, arma::gmm_dist_mode>(m, "__prob_dist");
        py::class_<arma::gmm_dist_maha, arma::gmm_dist_mode>(m, "__maha_dist");

        // Expose as attributes, so dist_mode() is unnecessary
        m.attr("eucl_dist") = py::cast(arma::eucl_dist);
        m.attr("prob_dist") = py::cast(arma::prob_dist);
        m.attr("maha_dist") = py::cast(arma::maha_dist);
    }
}