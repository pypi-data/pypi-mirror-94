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
    class Head_Slices {};
    class Tail_Slices {};

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_head_slices(const T &cube, const std::tuple<Head_Slices, arma::uword> n_slices) { 
        return cube.head_slices(std::get<1>(n_slices));
    }

    template<typename T>
    arma::subview_cube<typename T::elem_type> get_tail_slices(const T &cube, const std::tuple<Tail_Slices, arma::uword> n_slices) { 
        return cube.tail_slices(std::get<1>(n_slices));
    }

    template<typename T>
    void set_head_slices(T &cube, const std::tuple<Head_Slices, arma::uword> n_slices, const T &item) { 
        cube.head_slices(std::get<1>(n_slices)) = item;
    }

    template<typename T>
    void set_tail_slices(T &cube, const std::tuple<Tail_Slices, arma::uword> n_slices, const T &item) { 
        cube.tail_slices(std::get<1>(n_slices)) = item;
    }

    template arma::subview_cube<double> get_head_slices<arma::Cube<double>>(const arma::Cube<double> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices);
    template arma::subview_cube<double> get_tail_slices<arma::Cube<double>>(const arma::Cube<double> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices);
    template void set_head_slices<arma::Cube<double>>(arma::Cube<double> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices, const arma::Cube<double> &item);
    template void set_tail_slices<arma::Cube<double>>(arma::Cube<double> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices, const arma::Cube<double> &item);

    template arma::subview_cube<float> get_head_slices<arma::Cube<float>>(const arma::Cube<float> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices);
    template arma::subview_cube<float> get_tail_slices<arma::Cube<float>>(const arma::Cube<float> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices);
    template void set_head_slices<arma::Cube<float>>(arma::Cube<float> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices, const arma::Cube<float> &item);
    template void set_tail_slices<arma::Cube<float>>(arma::Cube<float> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices, const arma::Cube<float> &item);

    template arma::subview_cube<arma::cx_double> get_head_slices<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices);
    template arma::subview_cube<arma::cx_double> get_tail_slices<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices);
    template void set_head_slices<arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices, const arma::Cube<arma::cx_double> &item);
    template void set_tail_slices<arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices, const arma::Cube<arma::cx_double> &item);

    template arma::subview_cube<arma::cx_float> get_head_slices<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices);
    template arma::subview_cube<arma::cx_float> get_tail_slices<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices);
    template void set_head_slices<arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices, const arma::Cube<arma::cx_float> &item);
    template void set_tail_slices<arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices, const arma::Cube<arma::cx_float> &item);

    template arma::subview_cube<arma::uword> get_head_slices<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices);
    template arma::subview_cube<arma::uword> get_tail_slices<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices);
    template void set_head_slices<arma::Cube<arma::uword>>(arma::Cube<arma::uword> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices, const arma::Cube<arma::uword> &item);
    template void set_tail_slices<arma::Cube<arma::uword>>(arma::Cube<arma::uword> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices, const arma::Cube<arma::uword> &item);

    template arma::subview_cube<arma::sword> get_head_slices<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices);
    template arma::subview_cube<arma::sword> get_tail_slices<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices);
    template void set_head_slices<arma::Cube<arma::sword>>(arma::Cube<arma::sword> &matrix, const std::tuple<Head_Slices, arma::uword> n_slices, const arma::Cube<arma::sword> &item);
    template void set_tail_slices<arma::Cube<arma::sword>>(arma::Cube<arma::sword> &matrix, const std::tuple<Tail_Slices, arma::uword> n_slices, const arma::Cube<arma::sword> &item);
}
