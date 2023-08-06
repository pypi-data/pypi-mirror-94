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

#define ARMA_DONT_PRINT_ERRORS
#include "pybind11/pybind11.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose direct element-wise multiplication
    template<typename T, typename U>
    arma::Mat<typename T::elem_type> schur(T &a, U &b) {
        return a % b;
    }

    template arma::Mat<double> schur<arma::diagview<double>, arma::diagview<double>>(arma::diagview<double> &a, arma::diagview<double> &b);
    template arma::Mat<float> schur<arma::diagview<float>, arma::diagview<float>>(arma::diagview<float> &a, arma::diagview<float> &b);
    template arma::Mat<arma::cx_double> schur<arma::diagview<arma::cx_double>, arma::diagview<arma::cx_double>>(arma::diagview<arma::cx_double> &a, arma::diagview<arma::cx_double> &b);
    template arma::Mat<arma::cx_float> schur<arma::diagview<arma::cx_float>, arma::diagview<arma::cx_float>>(arma::diagview<arma::cx_float> &a, arma::diagview<arma::cx_float> &b);
    template arma::Mat<arma::uword> schur<arma::diagview<arma::uword>, arma::diagview<arma::uword>>(arma::diagview<arma::uword> &a, arma::diagview<arma::uword> &b);
    template arma::Mat<arma::sword> schur<arma::diagview<arma::sword>, arma::diagview<arma::sword>>(arma::diagview<arma::sword> &a, arma::diagview<arma::sword> &b);
}