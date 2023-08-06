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
    // Expose direct element-wise multiplication
    template<typename T, typename U>
    arma::Mat<typename T::elem_type> schur(T &a, U &b);

    // Expose reverse type-promotion element-wise multiplication
    template<typename T, typename U>
    arma::Mat<typename U::elem_type> schur_r(T &a, U &b);

    // Expost element-wise multiplication with broadcasting
    template<typename T, typename U>
    arma::Mat<typename T::elem_type> schur_mat(T &a, U &b);

    // Broadcasting can only be done on the matrix
    template<typename T>
    arma::Mat<typename T::elem_type> schur_mat(T &a, arma::diagview<typename T::elem_type> &b);
    
    // Broadcasting can only be done on the matrix
    template<typename T>
    arma::Mat<typename T::elem_type> schur_mat_r(arma::diagview<typename T::elem_type> &a, T &b);

    template<typename T, typename U>
    arma::Cube<typename T::elem_type> cube_schur(T &a, U &b);
}