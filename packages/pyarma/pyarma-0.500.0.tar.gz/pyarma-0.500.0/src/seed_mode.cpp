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
    // Expose seed_mode options used by kmeans and GMM
    arma_cold void expose_seed_mode(py::module &m) {
        // Expose seed_mode
        py::class_<arma::gmm_seed_mode>(m, "__seed_mode");

        py::class_<arma::gmm_seed_keep_existing, arma::gmm_seed_mode>(m, "__keep_existing");
        py::class_<arma::gmm_seed_static_subset, arma::gmm_seed_mode>(m, "__static_subset");
        py::class_<arma::gmm_seed_random_subset, arma::gmm_seed_mode>(m, "__random_subset");
        py::class_<arma::gmm_seed_static_spread, arma::gmm_seed_mode>(m, "__static_spread");
        py::class_<arma::gmm_seed_random_spread, arma::gmm_seed_mode>(m, "__random_spread");

        // Expose as attributes, so seed_mode() is unnecessary
        m.attr("keep_existing") = py::cast(arma::keep_existing);
        m.attr("static_subset") = py::cast(arma::static_subset);
        m.attr("random_subset") = py::cast(arma::random_subset);
        m.attr("static_spread") = py::cast(arma::static_spread);
        m.attr("random_spread") = py::cast(arma::random_spread);
    }
}