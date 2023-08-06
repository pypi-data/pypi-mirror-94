// Copyright 2020-2021 Jason Rumengan, Terry Yue Zhuo
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

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    typename T::elem_type get_element(const T &matrix, const std::tuple<arma::uword, arma::uword> coords);

    template<typename T>
    void set_element(T &matrix, std::tuple<arma::uword, arma::uword> coords, typename T::elem_type item);

    // Get/set elements by specifying (column-wise) element index
    template<typename T>
    typename T::elem_type get_element_single(const T &matrix, const arma::uword coord);
    
    template<typename T>
    void set_element_single(T &matrix, arma::uword coord, typename T::elem_type item);
}