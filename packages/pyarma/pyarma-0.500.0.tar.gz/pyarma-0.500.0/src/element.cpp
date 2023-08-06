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
    typename T::elem_type get_element(const T &matrix, const std::tuple<arma::uword, arma::uword> coords) {
        return matrix(std::get<0>(coords), std::get<1>(coords));
    }

    template<typename T>
    void set_element(T &matrix, std::tuple<arma::uword, arma::uword> coords, typename T::elem_type item) {
        matrix(std::get<0>(coords), std::get<1>(coords)) = item;
    }

    // Get/set elements by specifying (column-wise) element index
    template<typename T>
    typename T::elem_type get_element_single(const T &matrix, const arma::uword coord) {
        return matrix(coord);
    }
    
    template<typename T>
    void set_element_single(T &matrix, arma::uword coord, typename T::elem_type item) {
        matrix(coord) = item;
    }

    template double get_element<arma::Mat<double>>(const arma::Mat<double> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::Mat<double>>(arma::Mat<double> &matrix, std::tuple<arma::uword, arma::uword> coords, double item);
    template double get_element_single<arma::Mat<double>>(const arma::Mat<double> &matrix, const arma::uword coord);
    template void set_element_single<arma::Mat<double>>(arma::Mat<double> &matrix, arma::uword coord, double item);

    template double get_element<arma::subview<double>>(const arma::subview<double> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::subview<double>>(arma::subview<double> &matrix, std::tuple<arma::uword, arma::uword> coords, double item);
    template double get_element_single<arma::subview<double>>(const arma::subview<double> &matrix, const arma::uword coord);
    template void set_element_single<arma::subview<double>>(arma::subview<double> &matrix, arma::uword coord, double item);

    template double get_element<arma::diagview<double>>(const arma::diagview<double> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::diagview<double>>(arma::diagview<double> &matrix, std::tuple<arma::uword, arma::uword> coords, double item);
    template double get_element_single<arma::diagview<double>>(const arma::diagview<double> &matrix, const arma::uword coord);
    template void set_element_single<arma::diagview<double>>(arma::diagview<double> &matrix, arma::uword coord, double item);

    template float get_element<arma::Mat<float>>(const arma::Mat<float> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::Mat<float>>(arma::Mat<float> &matrix, std::tuple<arma::uword, arma::uword> coords, float item);
    template float get_element_single<arma::Mat<float>>(const arma::Mat<float> &matrix, const arma::uword coord);
    template void set_element_single<arma::Mat<float>>(arma::Mat<float> &matrix, arma::uword coord, float item);

    template float get_element<arma::subview<float>>(const arma::subview<float> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::subview<float>>(arma::subview<float> &matrix, std::tuple<arma::uword, arma::uword> coords, float item);
    template float get_element_single<arma::subview<float>>(const arma::subview<float> &matrix, const arma::uword coord);
    template void set_element_single<arma::subview<float>>(arma::subview<float> &matrix, arma::uword coord, float item);

    template float get_element<arma::diagview<float>>(const arma::diagview<float> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::diagview<float>>(arma::diagview<float> &matrix, std::tuple<arma::uword, arma::uword> coords, float item);
    template float get_element_single<arma::diagview<float>>(const arma::diagview<float> &matrix, const arma::uword coord);
    template void set_element_single<arma::diagview<float>>(arma::diagview<float> &matrix, arma::uword coord, float item);

    template arma::cx_double get_element<arma::Mat<arma::cx_double>>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::Mat<arma::cx_double>>(arma::Mat<arma::cx_double> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::cx_double item);
    template arma::cx_double get_element_single<arma::Mat<arma::cx_double>>(const arma::Mat<arma::cx_double> &matrix, const arma::uword coord);
    template void set_element_single<arma::Mat<arma::cx_double>>(arma::Mat<arma::cx_double> &matrix, arma::uword coord, arma::cx_double item);

    template arma::cx_double get_element<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::cx_double item);
    template arma::cx_double get_element_single<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, const arma::uword coord);
    template void set_element_single<arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &matrix, arma::uword coord, arma::cx_double item);

    template arma::cx_double get_element<arma::diagview<arma::cx_double>>(const arma::diagview<arma::cx_double> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::diagview<arma::cx_double>>(arma::diagview<arma::cx_double> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::cx_double item);
    template arma::cx_double get_element_single<arma::diagview<arma::cx_double>>(const arma::diagview<arma::cx_double> &matrix, const arma::uword coord);
    template void set_element_single<arma::diagview<arma::cx_double>>(arma::diagview<arma::cx_double> &matrix, arma::uword coord, arma::cx_double item);

    template arma::cx_float get_element<arma::Mat<arma::cx_float>>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::Mat<arma::cx_float>>(arma::Mat<arma::cx_float> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::cx_float item);
    template arma::cx_float get_element_single<arma::Mat<arma::cx_float>>(const arma::Mat<arma::cx_float> &matrix, const arma::uword coord);
    template void set_element_single<arma::Mat<arma::cx_float>>(arma::Mat<arma::cx_float> &matrix, arma::uword coord, arma::cx_float item);

    template arma::cx_float get_element<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::cx_float item);
    template arma::cx_float get_element_single<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, const arma::uword coord);
    template void set_element_single<arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &matrix, arma::uword coord, arma::cx_float item);

    template arma::cx_float get_element<arma::diagview<arma::cx_float>>(const arma::diagview<arma::cx_float> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::diagview<arma::cx_float>>(arma::diagview<arma::cx_float> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::cx_float item);
    template arma::cx_float get_element_single<arma::diagview<arma::cx_float>>(const arma::diagview<arma::cx_float> &matrix, const arma::uword coord);
    template void set_element_single<arma::diagview<arma::cx_float>>(arma::diagview<arma::cx_float> &matrix, arma::uword coord, arma::cx_float item);

    template arma::uword get_element<arma::Mat<arma::uword>>(const arma::Mat<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::Mat<arma::uword>>(arma::Mat<arma::uword> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::uword item);
    template arma::uword get_element_single<arma::Mat<arma::uword>>(const arma::Mat<arma::uword> &matrix, const arma::uword coord);
    template void set_element_single<arma::Mat<arma::uword>>(arma::Mat<arma::uword> &matrix, arma::uword coord, arma::uword item);

    template arma::uword get_element<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::subview<arma::uword>>(arma::subview<arma::uword> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::uword item);
    template arma::uword get_element_single<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, const arma::uword coord);
    template void set_element_single<arma::subview<arma::uword>>(arma::subview<arma::uword> &matrix, arma::uword coord, arma::uword item);

    template arma::uword get_element<arma::diagview<arma::uword>>(const arma::diagview<arma::uword> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::diagview<arma::uword>>(arma::diagview<arma::uword> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::uword item);
    template arma::uword get_element_single<arma::diagview<arma::uword>>(const arma::diagview<arma::uword> &matrix, const arma::uword coord);
    template void set_element_single<arma::diagview<arma::uword>>(arma::diagview<arma::uword> &matrix, arma::uword coord, arma::uword item);

    template arma::sword get_element<arma::Mat<arma::sword>>(const arma::Mat<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::Mat<arma::sword>>(arma::Mat<arma::sword> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::sword item);
    template arma::sword get_element_single<arma::Mat<arma::sword>>(const arma::Mat<arma::sword> &matrix, const arma::uword coord);
    template void set_element_single<arma::Mat<arma::sword>>(arma::Mat<arma::sword> &matrix, arma::uword coord, arma::sword item);

    template arma::sword get_element<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::subview<arma::sword>>(arma::subview<arma::sword> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::sword item);
    template arma::sword get_element_single<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, const arma::uword coord);
    template void set_element_single<arma::subview<arma::sword>>(arma::subview<arma::sword> &matrix, arma::uword coord, arma::sword item);

    template arma::sword get_element<arma::diagview<arma::sword>>(const arma::diagview<arma::sword> &matrix, const std::tuple<arma::uword, arma::uword> coords);
    template void set_element<arma::diagview<arma::sword>>(arma::diagview<arma::sword> &matrix, std::tuple<arma::uword, arma::uword> coords, arma::sword item);
    template arma::sword get_element_single<arma::diagview<arma::sword>>(const arma::diagview<arma::sword> &matrix, const arma::uword coord);
    template void set_element_single<arma::diagview<arma::sword>>(arma::diagview<arma::sword> &matrix, arma::uword coord, arma::sword item);
}