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
    // Expose direct division
    template<typename T, typename U>
    arma::Mat<typename T::elem_type> divide(T &a, U &b) {
        return a / b;
    }

    // template arma::Mat<double> divide<arma::diagview<double>, arma::diagview<double>>(arma::diagview<double> &a, arma::diagview<double> &b);
    template arma::Mat<double> divide<arma::diagview<double>, double>(arma::diagview<double> &a, double &b);
    // template arma::Mat<double> divide<arma::diagview<double>, arma::subview_elem1<double, arma::umat>>(arma::diagview<double> &a, arma::subview_elem1<double, arma::umat> &b);
    // template arma::Mat<double> divide<arma::diagview<double>, arma::subview_elem2<double, arma::umat, arma::umat>>(arma::diagview<double> &a, arma::subview_elem2<double, arma::umat, arma::umat> &b);
    // template arma::Mat<float> divide<arma::diagview<float>, arma::diagview<float>>(arma::diagview<float> &a, arma::diagview<float> &b);
    template arma::Mat<float> divide<arma::diagview<float>, float>(arma::diagview<float> &a, float &b);
    // template arma::Mat<float> divide<arma::diagview<float>, arma::subview_elem1<float, arma::umat>>(arma::diagview<float> &a, arma::subview_elem1<float, arma::umat> &b);
    // template arma::Mat<float> divide<arma::diagview<float>, arma::subview_elem2<float, arma::umat, arma::umat>>(arma::diagview<float> &a, arma::subview_elem2<float, arma::umat, arma::umat> &b);
    // template arma::Mat<arma::cx_double> divide<arma::diagview<arma::cx_double>, arma::diagview<arma::cx_double>>(arma::diagview<arma::cx_double> &a, arma::diagview<arma::cx_double> &b);
    template arma::Mat<arma::cx_double> divide<arma::diagview<arma::cx_double>, arma::cx_double>(arma::diagview<arma::cx_double> &a, arma::cx_double &b);
    // template arma::Mat<arma::cx_double> divide<arma::diagview<arma::cx_double>, arma::subview_elem1<arma::cx_double, arma::umat>>(arma::diagview<arma::cx_double> &a, arma::subview_elem1<arma::cx_double, arma::umat> &b);
    // template arma::Mat<arma::cx_double> divide<arma::diagview<arma::cx_double>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(arma::diagview<arma::cx_double> &a, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &b);
    // template arma::Mat<arma::cx_float> divide<arma::diagview<arma::cx_float>, arma::diagview<arma::cx_float>>(arma::diagview<arma::cx_float> &a, arma::diagview<arma::cx_float> &b);
    template arma::Mat<arma::cx_float> divide<arma::diagview<arma::cx_float>, arma::cx_float>(arma::diagview<arma::cx_float> &a, arma::cx_float &b);
    // template arma::Mat<arma::cx_float> divide<arma::diagview<arma::cx_float>, arma::subview_elem1<arma::cx_float, arma::umat>>(arma::diagview<arma::cx_float> &a, arma::subview_elem1<arma::cx_float, arma::umat> &b);
    // template arma::Mat<arma::cx_float> divide<arma::diagview<arma::cx_float>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(arma::diagview<arma::cx_float> &a, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &b);
    // template arma::Mat<arma::uword> divide<arma::diagview<arma::uword>, arma::diagview<arma::uword>>(arma::diagview<arma::uword> &a, arma::diagview<arma::uword> &b);
    template arma::Mat<arma::uword> divide<arma::diagview<arma::uword>, arma::uword>(arma::diagview<arma::uword> &a, arma::uword &b);
    // template arma::Mat<arma::uword> divide<arma::diagview<arma::uword>, arma::subview_elem1<arma::uword, arma::umat>>(arma::diagview<arma::uword> &a, arma::subview_elem1<arma::uword, arma::umat> &b);
    // template arma::Mat<arma::uword> divide<arma::diagview<arma::uword>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(arma::diagview<arma::uword> &a, arma::subview_elem2<arma::uword, arma::umat, arma::umat> &b);
    // template arma::Mat<arma::sword> divide<arma::diagview<arma::sword>, arma::diagview<arma::sword>>(arma::diagview<arma::sword> &a, arma::diagview<arma::sword> &b);
    template arma::Mat<arma::sword> divide<arma::diagview<arma::sword>, arma::sword>(arma::diagview<arma::sword> &a, arma::sword &b);
    // template arma::Mat<arma::sword> divide<arma::diagview<arma::sword>, arma::subview_elem1<arma::sword, arma::umat>>(arma::diagview<arma::sword> &a, arma::subview_elem1<arma::sword, arma::umat> &b);
    // template arma::Mat<arma::sword> divide<arma::diagview<arma::sword>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(arma::diagview<arma::sword> &a, arma::subview_elem2<arma::sword, arma::umat, arma::umat> &b);                      

    template arma::Mat<double> divide<arma::Mat<double>, double>(arma::Mat<double> &a, double &b);
    template arma::Mat<float> divide<arma::Mat<float>, float>(arma::Mat<float> &a, float &b);
    template arma::Mat<arma::cx_double> divide<arma::Mat<arma::cx_double>, arma::cx_double>(arma::Mat<arma::cx_double> &a, arma::cx_double &b);
    template arma::Mat<arma::cx_float> divide<arma::Mat<arma::cx_float>, arma::cx_float>(arma::Mat<arma::cx_float> &a, arma::cx_float &b);
    template arma::Mat<arma::uword> divide<arma::Mat<arma::uword>, arma::uword>(arma::Mat<arma::uword> &a, arma::uword &b);
    template arma::Mat<arma::sword> divide<arma::Mat<arma::sword>, arma::sword>(arma::Mat<arma::sword> &a, arma::sword &b);

    template arma::Mat<double> divide<arma::subview<double>, double>(arma::subview<double> &a, double &b);
    // template arma::Mat<double> divide<arma::subview<double>, arma::subview_elem1<double, arma::umat>>(arma::subview<double> &a, arma::subview_elem1<double, arma::umat> &b);
    // template arma::Mat<double> divide<arma::subview<double>, arma::subview_elem2<double, arma::umat, arma::umat>>(arma::subview<double> &a, arma::subview_elem2<double, arma::umat, arma::umat> &b);
    template arma::Mat<float> divide<arma::subview<float>, float>(arma::subview<float> &a, float &b);
    // template arma::Mat<float> divide<arma::subview<float>, arma::subview_elem1<float, arma::umat>>(arma::subview<float> &a, arma::subview_elem1<float, arma::umat> &b);
    // template arma::Mat<float> divide<arma::subview<float>, arma::subview_elem2<float, arma::umat, arma::umat>>(arma::subview<float> &a, arma::subview_elem2<float, arma::umat, arma::umat> &b);
    template arma::Mat<arma::cx_double> divide<arma::subview<arma::cx_double>, arma::cx_double>(arma::subview<arma::cx_double> &a, arma::cx_double &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview<arma::cx_double>, arma::subview_elem1<arma::cx_double, arma::umat>>(arma::subview<arma::cx_double> &a, arma::subview_elem1<arma::cx_double, arma::umat> &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview<arma::cx_double>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(arma::subview<arma::cx_double> &a, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &b);
    template arma::Mat<arma::cx_float> divide<arma::subview<arma::cx_float>, arma::cx_float>(arma::subview<arma::cx_float> &a, arma::cx_float &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview<arma::cx_float>, arma::subview_elem1<arma::cx_float, arma::umat>>(arma::subview<arma::cx_float> &a, arma::subview_elem1<arma::cx_float, arma::umat> &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview<arma::cx_float>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(arma::subview<arma::cx_float> &a, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &b);
    template arma::Mat<arma::uword> divide<arma::subview<arma::uword>, arma::uword>(arma::subview<arma::uword> &a, arma::uword &b);
    // template arma::Mat<arma::uword> divide<arma::subview<arma::uword>, arma::subview_elem1<arma::uword, arma::umat>>(arma::subview<arma::uword> &a, arma::subview_elem1<arma::uword, arma::umat> &b);
    // template arma::Mat<arma::uword> divide<arma::subview<arma::uword>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(arma::subview<arma::uword> &a, arma::subview_elem2<arma::uword, arma::umat, arma::umat> &b);
    template arma::Mat<arma::sword> divide<arma::subview<arma::sword>, arma::sword>(arma::subview<arma::sword> &a, arma::sword &b);
    // template arma::Mat<arma::sword> divide<arma::subview<arma::sword>, arma::subview_elem1<arma::sword, arma::umat>>(arma::subview<arma::sword> &a, arma::subview_elem1<arma::sword, arma::umat> &b);
    // template arma::Mat<arma::sword> divide<arma::subview<arma::sword>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(arma::subview<arma::sword> &a, arma::subview_elem2<arma::sword, arma::umat, arma::umat> &b);

    // template arma::Mat<double> divide<arma::subview_elem1<double, arma::umat>, arma::subview_elem1<double, arma::umat>>(arma::subview_elem1<double, arma::umat> &a, arma::subview_elem1<double, arma::umat> &b);
    template arma::Mat<double> divide<arma::subview_elem1<double, arma::umat>, arma::Mat<double>>(arma::subview_elem1<double, arma::umat> &a, arma::Mat<double> &b);
    // template arma::Mat<double> divide<arma::subview_elem1<double, arma::umat>, arma::subview<double>>(arma::subview_elem1<double, arma::umat> &a, arma::subview<double> &b);
    // template arma::Mat<double> divide<arma::subview_elem1<double, arma::umat>, arma::diagview<double>>(arma::subview_elem1<double, arma::umat> &a, arma::diagview<double> &b);
    // template arma::Mat<double> divide<arma::subview_elem1<double, arma::umat>, arma::subview_elem2<double, arma::umat, arma::umat>>(arma::subview_elem1<double, arma::umat> &a, arma::subview_elem2<double, arma::umat, arma::umat> &b);
    template arma::Mat<double> divide<arma::subview_elem1<double, arma::umat>, double>(arma::subview_elem1<double, arma::umat> &a, double &b);
    // template arma::Mat<float> divide<arma::subview_elem1<float, arma::umat>, arma::subview_elem1<float, arma::umat>>(arma::subview_elem1<float, arma::umat> &a, arma::subview_elem1<float, arma::umat> &b);
    template arma::Mat<float> divide<arma::subview_elem1<float, arma::umat>, arma::Mat<float>>(arma::subview_elem1<float, arma::umat> &a, arma::Mat<float> &b);
    // template arma::Mat<float> divide<arma::subview_elem1<float, arma::umat>, arma::subview<float>>(arma::subview_elem1<float, arma::umat> &a, arma::subview<float> &b);
    // template arma::Mat<float> divide<arma::subview_elem1<float, arma::umat>, arma::diagview<float>>(arma::subview_elem1<float, arma::umat> &a, arma::diagview<float> &b);
    // template arma::Mat<float> divide<arma::subview_elem1<float, arma::umat>, arma::subview_elem2<float, arma::umat, arma::umat>>(arma::subview_elem1<float, arma::umat> &a, arma::subview_elem2<float, arma::umat, arma::umat> &b);
    template arma::Mat<float> divide<arma::subview_elem1<float, arma::umat>, float>(arma::subview_elem1<float, arma::umat> &a, float &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem1<arma::cx_double, arma::umat>, arma::subview_elem1<arma::cx_double, arma::umat>>(arma::subview_elem1<arma::cx_double, arma::umat> &a, arma::subview_elem1<arma::cx_double, arma::umat> &b);
    template arma::Mat<arma::cx_double> divide<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Mat<arma::cx_double>>(arma::subview_elem1<arma::cx_double, arma::umat> &a, arma::Mat<arma::cx_double> &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem1<arma::cx_double, arma::umat>, arma::subview<arma::cx_double>>(arma::subview_elem1<arma::cx_double, arma::umat> &a, arma::subview<arma::cx_double> &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem1<arma::cx_double, arma::umat>, arma::diagview<arma::cx_double>>(arma::subview_elem1<arma::cx_double, arma::umat> &a, arma::diagview<arma::cx_double> &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem1<arma::cx_double, arma::umat>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(arma::subview_elem1<arma::cx_double, arma::umat> &a, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &b);
    template arma::Mat<arma::cx_double> divide<arma::subview_elem1<arma::cx_double, arma::umat>, arma::cx_double>(arma::subview_elem1<arma::cx_double, arma::umat> &a, arma::cx_double &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem1<arma::cx_float, arma::umat>, arma::subview_elem1<arma::cx_float, arma::umat>>(arma::subview_elem1<arma::cx_float, arma::umat> &a, arma::subview_elem1<arma::cx_float, arma::umat> &b);
    template arma::Mat<arma::cx_float> divide<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Mat<arma::cx_float>>(arma::subview_elem1<arma::cx_float, arma::umat> &a, arma::Mat<arma::cx_float> &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem1<arma::cx_float, arma::umat>, arma::subview<arma::cx_float>>(arma::subview_elem1<arma::cx_float, arma::umat> &a, arma::subview<arma::cx_float> &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem1<arma::cx_float, arma::umat>, arma::diagview<arma::cx_float>>(arma::subview_elem1<arma::cx_float, arma::umat> &a, arma::diagview<arma::cx_float> &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem1<arma::cx_float, arma::umat>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(arma::subview_elem1<arma::cx_float, arma::umat> &a, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &b);
    template arma::Mat<arma::cx_float> divide<arma::subview_elem1<arma::cx_float, arma::umat>, arma::cx_float>(arma::subview_elem1<arma::cx_float, arma::umat> &a, arma::cx_float &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem1<arma::uword, arma::umat>, arma::subview_elem1<arma::uword, arma::umat>>(arma::subview_elem1<arma::uword, arma::umat> &a, arma::subview_elem1<arma::uword, arma::umat> &b);
    template arma::Mat<arma::uword> divide<arma::subview_elem1<arma::uword, arma::umat>, arma::Mat<arma::uword>>(arma::subview_elem1<arma::uword, arma::umat> &a, arma::Mat<arma::uword> &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem1<arma::uword, arma::umat>, arma::subview<arma::uword>>(arma::subview_elem1<arma::uword, arma::umat> &a, arma::subview<arma::uword> &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem1<arma::uword, arma::umat>, arma::diagview<arma::uword>>(arma::subview_elem1<arma::uword, arma::umat> &a, arma::diagview<arma::uword> &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem1<arma::uword, arma::umat>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(arma::subview_elem1<arma::uword, arma::umat> &a, arma::subview_elem2<arma::uword, arma::umat, arma::umat> &b);
    template arma::Mat<arma::uword> divide<arma::subview_elem1<arma::uword, arma::umat>, arma::uword>(arma::subview_elem1<arma::uword, arma::umat> &a, arma::uword &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem1<arma::sword, arma::umat>, arma::subview_elem1<arma::sword, arma::umat>>(arma::subview_elem1<arma::sword, arma::umat> &a, arma::subview_elem1<arma::sword, arma::umat> &b);
    template arma::Mat<arma::sword> divide<arma::subview_elem1<arma::sword, arma::umat>, arma::Mat<arma::sword>>(arma::subview_elem1<arma::sword, arma::umat> &a, arma::Mat<arma::sword> &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem1<arma::sword, arma::umat>, arma::subview<arma::sword>>(arma::subview_elem1<arma::sword, arma::umat> &a, arma::subview<arma::sword> &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem1<arma::sword, arma::umat>, arma::diagview<arma::sword>>(arma::subview_elem1<arma::sword, arma::umat> &a, arma::diagview<arma::sword> &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem1<arma::sword, arma::umat>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(arma::subview_elem1<arma::sword, arma::umat> &a, arma::subview_elem2<arma::sword, arma::umat, arma::umat> &b);
    template arma::Mat<arma::sword> divide<arma::subview_elem1<arma::sword, arma::umat>, arma::sword>(arma::subview_elem1<arma::sword, arma::umat> &a, arma::sword &b);

    // template arma::Mat<double> divide<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview_elem2<double, arma::umat, arma::umat>>(arma::subview_elem2<double, arma::umat, arma::umat> &a, arma::subview_elem2<double, arma::umat, arma::umat> &b);
    template arma::Mat<double> divide<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Mat<double>>(arma::subview_elem2<double, arma::umat, arma::umat> &a, arma::Mat<double> &b);
    // template arma::Mat<double> divide<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview<double>>(arma::subview_elem2<double, arma::umat, arma::umat> &a, arma::subview<double> &b);
    // template arma::Mat<double> divide<arma::subview_elem2<double, arma::umat, arma::umat>, arma::diagview<double>>(arma::subview_elem2<double, arma::umat, arma::umat> &a, arma::diagview<double> &b);
    // template arma::Mat<double> divide<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview_elem1<double, arma::umat>>(arma::subview_elem2<double, arma::umat, arma::umat> &a, arma::subview_elem1<double, arma::umat> &b);
    template arma::Mat<double> divide<arma::subview_elem2<double, arma::umat, arma::umat>, double>(arma::subview_elem2<double, arma::umat, arma::umat> &a, double &b);
    // template arma::Mat<float> divide<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview_elem2<float, arma::umat, arma::umat>>(arma::subview_elem2<float, arma::umat, arma::umat> &a, arma::subview_elem2<float, arma::umat, arma::umat> &b);
    template arma::Mat<float> divide<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Mat<float>>(arma::subview_elem2<float, arma::umat, arma::umat> &a, arma::Mat<float> &b);
    // template arma::Mat<float> divide<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview<float>>(arma::subview_elem2<float, arma::umat, arma::umat> &a, arma::subview<float> &b);
    // template arma::Mat<float> divide<arma::subview_elem2<float, arma::umat, arma::umat>, arma::diagview<float>>(arma::subview_elem2<float, arma::umat, arma::umat> &a, arma::diagview<float> &b);
    // template arma::Mat<float> divide<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview_elem1<float, arma::umat>>(arma::subview_elem2<float, arma::umat, arma::umat> &a, arma::subview_elem1<float, arma::umat> &b);
    template arma::Mat<float> divide<arma::subview_elem2<float, arma::umat, arma::umat>, float>(arma::subview_elem2<float, arma::umat, arma::umat> &a, float &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &a, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &b);
    template arma::Mat<arma::cx_double> divide<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Mat<arma::cx_double>>(arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &a, arma::Mat<arma::cx_double> &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::subview<arma::cx_double>>(arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &a, arma::subview<arma::cx_double> &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::diagview<arma::cx_double>>(arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &a, arma::diagview<arma::cx_double> &b);
    // template arma::Mat<arma::cx_double> divide<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::subview_elem1<arma::cx_double, arma::umat>>(arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &a, arma::subview_elem1<arma::cx_double, arma::umat> &b);
    template arma::Mat<arma::cx_double> divide<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::cx_double>(arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> &a, arma::cx_double &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &a, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &b);
    template arma::Mat<arma::cx_float> divide<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Mat<arma::cx_float>>(arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &a, arma::Mat<arma::cx_float> &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::subview<arma::cx_float>>(arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &a, arma::subview<arma::cx_float> &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::diagview<arma::cx_float>>(arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &a, arma::diagview<arma::cx_float> &b);
    // template arma::Mat<arma::cx_float> divide<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::subview_elem1<arma::cx_float, arma::umat>>(arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &a, arma::subview_elem1<arma::cx_float, arma::umat> &b);
    template arma::Mat<arma::cx_float> divide<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::cx_float>(arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> &a, arma::cx_float &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(arma::subview_elem2<arma::uword, arma::umat, arma::umat> &a, arma::subview_elem2<arma::uword, arma::umat, arma::umat> &b);
    template arma::Mat<arma::uword> divide<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Mat<arma::uword>>(arma::subview_elem2<arma::uword, arma::umat, arma::umat> &a, arma::Mat<arma::uword> &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview<arma::uword>>(arma::subview_elem2<arma::uword, arma::umat, arma::umat> &a, arma::subview<arma::uword> &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::diagview<arma::uword>>(arma::subview_elem2<arma::uword, arma::umat, arma::umat> &a, arma::diagview<arma::uword> &b);
    // template arma::Mat<arma::uword> divide<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview_elem1<arma::uword, arma::umat>>(arma::subview_elem2<arma::uword, arma::umat, arma::umat> &a, arma::subview_elem1<arma::uword, arma::umat> &b);
    template arma::Mat<arma::uword> divide<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::uword>(arma::subview_elem2<arma::uword, arma::umat, arma::umat> &a, arma::uword &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(arma::subview_elem2<arma::sword, arma::umat, arma::umat> &a, arma::subview_elem2<arma::sword, arma::umat, arma::umat> &b);
    template arma::Mat<arma::sword> divide<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Mat<arma::sword>>(arma::subview_elem2<arma::sword, arma::umat, arma::umat> &a, arma::Mat<arma::sword> &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview<arma::sword>>(arma::subview_elem2<arma::sword, arma::umat, arma::umat> &a, arma::subview<arma::sword> &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::diagview<arma::sword>>(arma::subview_elem2<arma::sword, arma::umat, arma::umat> &a, arma::diagview<arma::sword> &b);
    // template arma::Mat<arma::sword> divide<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview_elem1<arma::sword, arma::umat>>(arma::subview_elem2<arma::sword, arma::umat, arma::umat> &a, arma::subview_elem1<arma::sword, arma::umat> &b);
    template arma::Mat<arma::sword> divide<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::sword>(arma::subview_elem2<arma::sword, arma::umat, arma::umat> &a, arma::sword &b);
}