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
    arma::subview_cube<typename T::elem_type> get_subcube(const T &cube, const std::tuple<py::slice, py::slice, py::slice> coords);

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_subcube_size(const T &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords);

    template<typename T, typename U>
    void set_subcube(T &cube, std::tuple<py::slice, py::slice, py::slice> coords, U item);

    template<typename T, typename U>
    void set_subcube_size(T &cube, const std::tuple<arma::uword, arma::uword, arma::uword, arma::SizeCube> coords, U item);
}

