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
    // Expose subtraction with broadcasting
    template<typename T, typename U>
    arma::Mat<typename T::elem_type> subtract_mat(T &a, U &b) {
        arma::Mat<typename T::elem_type> output;
        if (a.n_rows == 1 && a.n_cols == 1) {
            output = as_scalar(a) - b;
        } else if (b.n_rows == 1 && b.n_cols == 1) {
            output = a - as_scalar(b);
        } else if (b.n_cols == 1 && b.n_rows == a.n_rows) {
            output = a.each_col() - b;
        } else if (b.n_rows == 1 && b.n_cols == a.n_cols) {
            output = a.each_row() - b;
        } else if (a.n_cols == 1 && b.n_rows == a.n_rows) {
            output = a - b.each_col();
        } else if (a.n_rows == 1 && b.n_cols == a.n_cols) {
            output = a - b.each_row();
        } else {
            output = a - b;
        }
        return output;
    }

    template arma::Mat<double> subtract_mat<arma::Mat<double>, arma::Mat<double>>(arma::Mat<double> &a, arma::Mat<double> &b);
    template arma::Mat<float> subtract_mat<arma::Mat<float>, arma::Mat<float>>(arma::Mat<float> &a, arma::Mat<float> &b);
    template arma::Mat<arma::cx_double> subtract_mat<arma::Mat<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::Mat<arma::cx_double> &a, arma::Mat<arma::cx_double> &b);
    template arma::Mat<arma::cx_float> subtract_mat<arma::Mat<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::Mat<arma::cx_float> &a, arma::Mat<arma::cx_float> &b);
    template arma::Mat<arma::uword> subtract_mat<arma::Mat<arma::uword>, arma::Mat<arma::uword>>(arma::Mat<arma::uword> &a, arma::Mat<arma::uword> &b);
    template arma::Mat<arma::sword> subtract_mat<arma::Mat<arma::sword>, arma::Mat<arma::sword>>(arma::Mat<arma::sword> &a, arma::Mat<arma::sword> &b);

    template arma::Mat<double> subtract_mat<arma::subview<double>, arma::subview<double>>(arma::subview<double> &a, arma::subview<double> &b);
    template arma::Mat<double> subtract_mat<arma::subview<double>, arma::Mat<double>>(arma::subview<double> &a, arma::Mat<double> &b);
    template arma::Mat<float> subtract_mat<arma::subview<float>, arma::subview<float>>(arma::subview<float> &a, arma::subview<float> &b);
    template arma::Mat<float> subtract_mat<arma::subview<float>, arma::Mat<float>>(arma::subview<float> &a, arma::Mat<float> &b);
    template arma::Mat<arma::cx_double> subtract_mat<arma::subview<arma::cx_double>, arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &a, arma::subview<arma::cx_double> &b);
    template arma::Mat<arma::cx_double> subtract_mat<arma::subview<arma::cx_double>, arma::Mat<arma::cx_double>>(arma::subview<arma::cx_double> &a, arma::Mat<arma::cx_double> &b);
    template arma::Mat<arma::cx_float> subtract_mat<arma::subview<arma::cx_float>, arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &a, arma::subview<arma::cx_float> &b);
    template arma::Mat<arma::cx_float> subtract_mat<arma::subview<arma::cx_float>, arma::Mat<arma::cx_float>>(arma::subview<arma::cx_float> &a, arma::Mat<arma::cx_float> &b);
    template arma::Mat<arma::uword> subtract_mat<arma::subview<arma::uword>, arma::subview<arma::uword>>(arma::subview<arma::uword> &a, arma::subview<arma::uword> &b);
    template arma::Mat<arma::uword> subtract_mat<arma::subview<arma::uword>, arma::Mat<arma::uword>>(arma::subview<arma::uword> &a, arma::Mat<arma::uword> &b);
    template arma::Mat<arma::sword> subtract_mat<arma::subview<arma::sword>, arma::subview<arma::sword>>(arma::subview<arma::sword> &a, arma::subview<arma::sword> &b);
    template arma::Mat<arma::sword> subtract_mat<arma::subview<arma::sword>, arma::Mat<arma::sword>>(arma::subview<arma::sword> &a, arma::Mat<arma::sword> &b);
}