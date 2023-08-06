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

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    arma::subview_cube<typename T::elem_type> get_tube_span(const T &cube, const std::tuple<py::slice, py::slice> coords);

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_tube(const T &cube, const std::tuple<arma::uword, arma::uword> coords);

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_tube_size(const T &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords);

    template<typename T, typename U>
    void set_tube_span(T &cube, const std::tuple<py::slice, py::slice> coords, const U &item);

    template<typename T, typename U>
    void set_tube(T &cube, const std::tuple<arma::uword, arma::uword> coords, const U &item);

    template<typename T, typename U>
    void set_tube_size(T &cube, const std::tuple<arma::uword, arma::uword, arma::SizeMat> coords, const U &item);
}

