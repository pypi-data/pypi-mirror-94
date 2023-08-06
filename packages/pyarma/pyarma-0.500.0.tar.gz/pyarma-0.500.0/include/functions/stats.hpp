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

#pragma once
#include "pybind11/pybind11.h"
#include "armadillo"
#include <type_traits>

namespace py = pybind11;

namespace pyarma {
    // Expose histograms, which can only be used with non-complex types (including integral types)
    template<typename T>
    typename std::enable_if<(arma::is_cx_float<typename T::elem_type>::yes ||
                             arma::is_cx_double<typename T::elem_type>::yes)>::type
    expose_hist(py::module &);

    template<typename T>
    typename std::enable_if<!(arma::is_cx_float<typename T::elem_type>::yes ||
                             arma::is_cx_double<typename T::elem_type>::yes)>::type
    expose_hist(py::module &m);

    template<typename T>
    typename std::enable_if<!(arma::is_real<typename T::elem_type>::value)>::type 
    expose_stats_real(py::module &);

    template<typename T>
    typename std::enable_if<arma::is_real<typename T::elem_type>::value>::type 
    expose_stats_real(py::module &m);

    /* Expose stats functions
       (only available for real types) */
    template<typename T>
    typename std::enable_if<!(arma::is_supported_blas_type<typename T::elem_type>::value)>::type 
    expose_stats(py::module &);

    template<typename T>
    typename std::enable_if<(arma::is_supported_blas_type<typename T::elem_type>::value && !(arma::is_arma_cube_type<T>::value))>::type 
    expose_stats(py::module &m);

    template<typename T>
    typename std::enable_if<(arma::is_supported_blas_type<typename T::elem_type>::value && arma::is_arma_cube_type<T>::value)>::type 
    expose_stats(py::module &m);
}
