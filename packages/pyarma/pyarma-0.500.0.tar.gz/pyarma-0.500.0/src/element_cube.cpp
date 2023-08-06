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
    template<typename T>
    typename T::elem_type cube_get_element(const T &cube, const std::tuple<arma::uword, arma::uword, arma::uword> coords) {
        return cube(std::get<0>(coords), std::get<1>(coords), std::get<2>(coords));
    }

    template<typename T>
    typename T::elem_type cube_get_element_single(const T &cube, const arma::uword coord) {
        return cube(coord);
    }

    template<typename T>
    void cube_set_element_single(T &cube, arma::uword coord, typename T::elem_type item) {
        cube(coord) = item;
    }

    template<typename T>
    void cube_set_element(T &cube, std::tuple<arma::uword, arma::uword, arma::uword> coords, typename T::elem_type item) {
        cube(std::get<0>(coords), std::get<1>(coords), std::get<2>(coords)) = item;
    }

    template double cube_get_element<arma::Cube<double>>(const arma::Cube<double> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::Cube<double>>(arma::Cube<double> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, double item);
    template double cube_get_element_single<arma::Cube<double>>(const arma::Cube<double> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::Cube<double>>(arma::Cube<double> &matrix, arma::uword coord, double item);

    template double cube_get_element<arma::subview_cube<double>>(const arma::subview_cube<double> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::subview_cube<double>>(arma::subview_cube<double> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, double item);
    template double cube_get_element_single<arma::subview_cube<double>>(const arma::subview_cube<double> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::subview_cube<double>>(arma::subview_cube<double> &matrix, arma::uword coord, double item);

    template float cube_get_element<arma::Cube<float>>(const arma::Cube<float> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::Cube<float>>(arma::Cube<float> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, float item);
    template float cube_get_element_single<arma::Cube<float>>(const arma::Cube<float> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::Cube<float>>(arma::Cube<float> &matrix, arma::uword coord, float item);

    template float cube_get_element<arma::subview_cube<float>>(const arma::subview_cube<float> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::subview_cube<float>>(arma::subview_cube<float> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, float item);
    template float cube_get_element_single<arma::subview_cube<float>>(const arma::subview_cube<float> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::subview_cube<float>>(arma::subview_cube<float> &matrix, arma::uword coord, float item);

    template arma::cx_double cube_get_element<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::cx_double item);
    template arma::cx_double cube_get_element_single<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::Cube<arma::cx_double>>(arma::Cube<arma::cx_double> &matrix, arma::uword coord, arma::cx_double item);

    template arma::cx_double cube_get_element<arma::subview_cube<arma::cx_double>>(const arma::subview_cube<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::subview_cube<arma::cx_double>>(arma::subview_cube<arma::cx_double> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::cx_double item);
    template arma::cx_double cube_get_element_single<arma::subview_cube<arma::cx_double>>(const arma::subview_cube<arma::cx_double> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::subview_cube<arma::cx_double>>(arma::subview_cube<arma::cx_double> &matrix, arma::uword coord, arma::cx_double item);

    template arma::cx_float cube_get_element<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::cx_float item);
    template arma::cx_float cube_get_element_single<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::Cube<arma::cx_float>>(arma::Cube<arma::cx_float> &matrix, arma::uword coord, arma::cx_float item);

    template arma::cx_float cube_get_element<arma::subview_cube<arma::cx_float>>(const arma::subview_cube<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::subview_cube<arma::cx_float>>(arma::subview_cube<arma::cx_float> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::cx_float item);
    template arma::cx_float cube_get_element_single<arma::subview_cube<arma::cx_float>>(const arma::subview_cube<arma::cx_float> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::subview_cube<arma::cx_float>>(arma::subview_cube<arma::cx_float> &matrix, arma::uword coord, arma::cx_float item);

    template arma::uword cube_get_element<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::Cube<arma::uword>>(arma::Cube<arma::uword> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::uword item);
    template arma::uword cube_get_element_single<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::Cube<arma::uword>>(arma::Cube<arma::uword> &matrix, arma::uword coord, arma::uword item);

    template arma::uword cube_get_element<arma::subview_cube<arma::uword>>(const arma::subview_cube<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::subview_cube<arma::uword>>(arma::subview_cube<arma::uword> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::uword item);
    template arma::uword cube_get_element_single<arma::subview_cube<arma::uword>>(const arma::subview_cube<arma::uword> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::subview_cube<arma::uword>>(arma::subview_cube<arma::uword> &matrix, arma::uword coord, arma::uword item);

    template arma::sword cube_get_element<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::Cube<arma::sword>>(arma::Cube<arma::sword> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::sword item);
    template arma::sword cube_get_element_single<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::Cube<arma::sword>>(arma::Cube<arma::sword> &matrix, arma::uword coord, arma::sword item);

    template arma::sword cube_get_element<arma::subview_cube<arma::sword>>(const arma::subview_cube<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword, arma::uword> coords);
    template void cube_set_element<arma::subview_cube<arma::sword>>(arma::subview_cube<arma::sword> &matrix, std::tuple<arma::uword, arma::uword, arma::uword> coords, arma::sword item);
    template arma::sword cube_get_element_single<arma::subview_cube<arma::sword>>(const arma::subview_cube<arma::sword> &matrix, const arma::uword coord);
    template void cube_set_element_single<arma::subview_cube<arma::sword>>(arma::subview_cube<arma::sword> &matrix, arma::uword coord, arma::sword item);
}