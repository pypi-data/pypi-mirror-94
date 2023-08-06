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
using namespace pybind11::literals;

namespace pyarma {
    // Defines convolutions
    template<typename Class>
    void expose_conv(py::module &m);

    // Defines inverse fast Fourier transforms for complex types
    template<typename Class>
    typename std::enable_if<!(arma::is_arma_type<Class>::value && 
    (arma::is_cx_float<typename Class::elem_type>::yes ||
     arma::is_cx_double<typename Class::elem_type>::yes))>::type expose_ifft(py::module &);

    template<typename Class>
    typename std::enable_if<arma::is_arma_type<Class>::value && 
    (arma::is_cx_float<typename Class::elem_type>::yes ||
     arma::is_cx_double<typename Class::elem_type>::yes)>::type
    expose_ifft(py::module &m);
        
    // Defines interpolation for floating-point types
    template<typename Class>
    typename std::enable_if<!(arma::is_real<typename Class::elem_type>::value)>::type
    expose_interp(py::module &);

    template<typename Class>
    typename std::enable_if<arma::is_real<typename Class::elem_type>::value>::type
    expose_interp(py::module &m);
}