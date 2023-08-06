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

namespace pyarma {
    template<typename T>
    arma::subview_elem2<T, arma::umat, arma::umat> get_submat(const arma::Mat<T> &matrix, const std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> &indices);

    template<typename T>
    void set_submat(arma::Mat<T> &matrix, std::tuple<arma::Mat<arma::uword> &, arma::Mat<arma::uword> &> indices, arma::Mat<T> item);
}