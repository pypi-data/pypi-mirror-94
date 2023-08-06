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

namespace py = pybind11;

namespace pyarma {
    // Exposes a matrix along with its standalone functions and methods
    template<typename T>
    py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> declare_matrix(py::module &m, const std::string typestr);
    
    // Expose a matrix while adding functions and methods exclusive to certain types
    template<typename T>
    void expose_matrix(py::module &m, const std::string typestr);

    template<>
    void expose_matrix<double>(py::module &m, const std::string typestr);

    template<>
    void expose_matrix<float>(py::module &m, const std::string typestr);

    template<>
    void expose_matrix<arma::cx_double>(py::module &m, const std::string typestr);

    template<>
    void expose_matrix<arma::cx_float>(py::module &m, const std::string typestr);

    template<>
    void expose_matrix<arma::uword>(py::module &m, const std::string typestr);

    template<>
    void expose_matrix<arma::sword>(py::module &m, const std::string typestr);
}