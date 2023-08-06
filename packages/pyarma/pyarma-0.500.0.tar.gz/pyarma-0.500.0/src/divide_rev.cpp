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

#define ARMA_DONT_PRINT_ERRORS
#include "pybind11/pybind11.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose reverse type-promotion division
    template<typename T, typename U>
    arma::Mat<typename U::elem_type> divide_r(T &a, U &b) {
        return a / b;
    }

    template arma::cx_mat divide_r<arma::mat, arma::cx_mat>(arma::mat &a, arma::cx_mat &b);
    template arma::cx_mat divide_r<arma::fmat, arma::cx_mat>(arma::fmat &a, arma::cx_mat &b);
    template arma::cx_fmat divide_r<arma::fmat, arma::cx_fmat>(arma::fmat &a, arma::cx_fmat &b);
    template arma::mat divide_r<arma::fmat, arma::mat>(arma::fmat &a, arma::mat &b);
    template arma::mat divide_r<arma::umat, arma::mat>(arma::umat &a, arma::mat &b);
    template arma::fmat divide_r<arma::umat, arma::fmat>(arma::umat &a, arma::fmat &b);
    template arma::mat divide_r<arma::imat, arma::mat>(arma::imat &a, arma::mat &b);
    template arma::fmat divide_r<arma::imat, arma::fmat>(arma::imat &a, arma::fmat &b);
}