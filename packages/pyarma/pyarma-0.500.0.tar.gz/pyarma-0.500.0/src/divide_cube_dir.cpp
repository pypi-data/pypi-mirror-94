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
    template<typename T, typename U>
    arma::Cube<typename T::elem_type> cube_divide(T &a, U &b) {
        return a / b;
    }

    template arma::Cube<double> cube_divide<arma::Cube<double>, double>(arma::Cube<double> &a, double &b);
    template arma::Cube<double> cube_divide<arma::subview_cube<double>, double>(arma::subview_cube<double> &a, double &b);

    template arma::Cube<float> cube_divide<arma::Cube<float>, float>(arma::Cube<float> &a, float &b);
    template arma::Cube<float> cube_divide<arma::subview_cube<float>, float>(arma::subview_cube<float> &a, float &b);

    template arma::Cube<arma::cx_double> cube_divide<arma::Cube<arma::cx_double>, arma::cx_double>(arma::Cube<arma::cx_double> &a, arma::cx_double &b);
    template arma::Cube<arma::cx_double> cube_divide<arma::subview_cube<arma::cx_double>, arma::cx_double>(arma::subview_cube<arma::cx_double> &a, arma::cx_double &b);

    template arma::Cube<arma::cx_float> cube_divide<arma::Cube<arma::cx_float>, arma::cx_float>(arma::Cube<arma::cx_float> &a, arma::cx_float &b);
    template arma::Cube<arma::cx_float> cube_divide<arma::subview_cube<arma::cx_float>, arma::cx_float>(arma::subview_cube<arma::cx_float> &a, arma::cx_float &b);

    template arma::Cube<arma::uword> cube_divide<arma::Cube<arma::uword>, arma::uword>(arma::Cube<arma::uword> &a, arma::uword &b);
    template arma::Cube<arma::uword> cube_divide<arma::subview_cube<arma::uword>, arma::uword>(arma::subview_cube<arma::uword> &a, arma::uword &b);

    template arma::Cube<arma::sword> cube_divide<arma::Cube<arma::sword>, arma::sword>(arma::Cube<arma::sword> &a, arma::sword &b);
    template arma::Cube<arma::sword> cube_divide<arma::subview_cube<arma::sword>, arma::sword>(arma::subview_cube<arma::sword> &a, arma::sword &b);
}