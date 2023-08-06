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
    // Broadcasting can only be done on the matrix
    template<typename T>
    arma::Mat<typename T::elem_type> schur_mat_r(arma::diagview<typename T::elem_type> &a, T &b) {
        arma::Mat<typename T::elem_type> output;
        if (a.n_cols == 1 && b.n_rows == a.n_rows) {
            output = a % b.each_col();
        } else if (a.n_rows == 1 && b.n_cols == a.n_cols) {
            output = a % b.each_row();
        } else {
            output = a % b;
        }
        return output;       
    }

    template arma::Mat<double> schur_mat_r<arma::Mat<double>>(arma::diagview<double> &a, arma::Mat<double> &b);
    // template arma::Mat<double> schur_mat_r<arma::subview<double>>(arma::diagview<double> &a, arma::subview<double> &b);
    template arma::Mat<float> schur_mat_r<arma::Mat<float>>(arma::diagview<float> &a, arma::Mat<float> &b);
    // template arma::Mat<float> schur_mat_r<arma::subview<float>>(arma::diagview<float> &a, arma::subview<float> &b);
    template arma::Mat<arma::cx_double> schur_mat_r<arma::Mat<arma::cx_double>>(arma::diagview<arma::cx_double> &a, arma::Mat<arma::cx_double> &b);
    // template arma::Mat<arma::cx_double> schur_mat_r<arma::subview<arma::cx_double>>(arma::diagview<arma::cx_double> &a, arma::subview<arma::cx_double> &b);
    template arma::Mat<arma::cx_float> schur_mat_r<arma::Mat<arma::cx_float>>(arma::diagview<arma::cx_float> &a, arma::Mat<arma::cx_float> &b);
    // template arma::Mat<arma::cx_float> schur_mat_r<arma::subview<arma::cx_float>>(arma::diagview<arma::cx_float> &a, arma::subview<arma::cx_float> &b);
    template arma::Mat<arma::uword> schur_mat_r<arma::Mat<arma::uword>>(arma::diagview<arma::uword> &a, arma::Mat<arma::uword> &b);
    // template arma::Mat<arma::uword> schur_mat_r<arma::subview<arma::uword>>(arma::diagview<arma::uword> &a, arma::subview<arma::uword> &b);
    template arma::Mat<arma::sword> schur_mat_r<arma::Mat<arma::sword>>(arma::diagview<arma::sword> &a, arma::Mat<arma::sword> &b);
    // template arma::Mat<arma::sword> schur_mat_r<arma::subview<arma::sword>>(arma::diagview<arma::sword> &a, arma::subview<arma::sword> &b);
}