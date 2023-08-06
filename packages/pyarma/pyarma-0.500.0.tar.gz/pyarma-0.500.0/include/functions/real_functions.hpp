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
    /* Defining functions and methods that only work on real types 
       (double, float, and their complex forms) */
    template<typename T>
    typename std::enable_if<!(arma::is_supported_blas_type<typename T::elem_type>::value)>::type
    expose_real_funcs(py::module &, py::class_<T, arma::Base<typename T::elem_type, T>> &);

    template<typename T>
    typename std::enable_if<arma::is_supported_blas_type<typename T::elem_type>::value>::type
    expose_real_funcs(py::module &m, py::class_<T, arma::Base<typename T::elem_type, T>> &py_class);
}