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
    arma::Cube<typename T::elem_type> multiply_cube(T &a, U &b) {
        using Type = typename T::elem_type;
        arma::Cube<Type> output;
        arma::Cube<Type> new_a = a;
        arma::Cube<Type> new_b = b;
        if (new_a.n_rows == 1 && new_a.n_cols == 1 && new_a.n_slices == 1) {
            output = as_scalar(new_a) * new_b;
        } else if (new_b.n_rows == 1 && new_b.n_cols == 1 && new_b.n_slices == 1) {
            output = new_a * as_scalar(new_b);
        } else {
            throw py::type_error("Cubes cannot be multiplied with each other");
        }
        return output;
    }

    template arma::Cube<double> multiply_cube<arma::Cube<double>, arma::Cube<double>>(arma::Cube<double> &a, arma::Cube<double> &b);
    template arma::Cube<double> multiply_cube<arma::subview_cube<double>, arma::Cube<double>>(arma::subview_cube<double> &a, arma::Cube<double> &b);
    template arma::Cube<double> multiply_cube<arma::subview_cube<double>, arma::subview_cube<double>>(arma::subview_cube<double> &a, arma::subview_cube<double> &b);

    template arma::Cube<float> multiply_cube<arma::Cube<float>, arma::Cube<float>>(arma::Cube<float> &a, arma::Cube<float> &b);
    template arma::Cube<float> multiply_cube<arma::subview_cube<float>, arma::Cube<float>>(arma::subview_cube<float> &a, arma::Cube<float> &b);
    template arma::Cube<float> multiply_cube<arma::subview_cube<float>, arma::subview_cube<float>>(arma::subview_cube<float> &a, arma::subview_cube<float> &b);

    template arma::Cube<arma::cx_double> multiply_cube<arma::Cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &a, arma::Cube<arma::cx_double> &b);
    template arma::Cube<arma::cx_double> multiply_cube<arma::subview_cube<arma::cx_double>, arma::Cube<arma::cx_double>>(arma::subview_cube<arma::cx_double> &a, arma::Cube<arma::cx_double> &b);
    template arma::Cube<arma::cx_double> multiply_cube<arma::subview_cube<arma::cx_double>, arma::subview_cube<arma::cx_double>>(arma::subview_cube<arma::cx_double> &a, arma::subview_cube<arma::cx_double> &b);

    template arma::Cube<arma::cx_float> multiply_cube<arma::Cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &a, arma::Cube<arma::cx_float> &b);
    template arma::Cube<arma::cx_float> multiply_cube<arma::subview_cube<arma::cx_float>, arma::Cube<arma::cx_float>>(arma::subview_cube<arma::cx_float> &a, arma::Cube<arma::cx_float> &b);
    template arma::Cube<arma::cx_float> multiply_cube<arma::subview_cube<arma::cx_float>, arma::subview_cube<arma::cx_float>>(arma::subview_cube<arma::cx_float> &a, arma::subview_cube<arma::cx_float> &b);

    template arma::Cube<arma::uword> multiply_cube<arma::Cube<arma::uword>, arma::Cube<arma::uword>>(arma::Cube<arma::uword> &a, arma::Cube<arma::uword> &b);
    template arma::Cube<arma::uword> multiply_cube<arma::subview_cube<arma::uword>, arma::Cube<arma::uword>>(arma::subview_cube<arma::uword> &a, arma::Cube<arma::uword> &b);
    template arma::Cube<arma::uword> multiply_cube<arma::subview_cube<arma::uword>, arma::subview_cube<arma::uword>>(arma::subview_cube<arma::uword> &a, arma::subview_cube<arma::uword> &b);

    template arma::Cube<arma::sword> multiply_cube<arma::Cube<arma::sword>, arma::Cube<arma::sword>>(arma::Cube<arma::sword> &a, arma::Cube<arma::sword> &b);
    template arma::Cube<arma::sword> multiply_cube<arma::subview_cube<arma::sword>, arma::Cube<arma::sword>>(arma::subview_cube<arma::sword> &a, arma::Cube<arma::sword> &b);
    template arma::Cube<arma::sword> multiply_cube<arma::subview_cube<arma::sword>, arma::subview_cube<arma::sword>>(arma::subview_cube<arma::sword> &a, arma::subview_cube<arma::sword> &b);
}