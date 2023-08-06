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
    class Diag {};

    template<typename T>
    arma::diagview<typename T::elem_type> get_diag(const T &matrix, const std::tuple<Diag, arma::sword> coords) {
        return matrix.diag(std::get<1>(coords));    
    }

    template<typename T>
    arma::diagview<typename T::elem_type> get_main_diag(const T &matrix, const Diag diag_sym) {
        return matrix.diag();    
    }

    template<typename T>
    void set_diag(T &matrix, std::tuple<Diag, arma::sword> coords, arma::Mat<typename T::elem_type> item) {
        matrix.diag(std::get<1>(coords)) = item;    
    }

    template<typename T>
    void set_main_diag(T &matrix, Diag diag_sym, arma::Mat<typename T::elem_type> item) {
        matrix.diag() = item;  
    }

    template arma::diagview<double> get_diag<arma::mat>(const arma::mat &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<float> get_diag<arma::fmat>(const arma::fmat &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::cx_double> get_diag<arma::cx_mat>(const arma::cx_mat &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::cx_float> get_diag<arma::cx_fmat>(const arma::cx_fmat &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::uword> get_diag<arma::umat>(const arma::umat &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::sword> get_diag<arma::imat>(const arma::imat &matrix, const std::tuple<Diag, arma::sword> coords);

    template arma::diagview<double> get_diag<arma::subview<double>>(const arma::subview<double> &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<float> get_diag<arma::subview<float>>(const arma::subview<float> &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::cx_double> get_diag<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::cx_float> get_diag<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::uword> get_diag<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, const std::tuple<Diag, arma::sword> coords);
    template arma::diagview<arma::sword> get_diag<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, const std::tuple<Diag, arma::sword> coords);

    template void set_diag<arma::mat>(arma::mat &matrix, std::tuple<Diag, arma::sword> coords, arma::mat item);
    template void set_diag<arma::fmat>(arma::fmat &matrix, std::tuple<Diag, arma::sword> coords, arma::fmat item);
    template void set_diag<arma::cx_mat>(arma::cx_mat &matrix, std::tuple<Diag, arma::sword> coords, arma::cx_mat item);
    template void set_diag<arma::cx_fmat>(arma::cx_fmat &matrix, std::tuple<Diag, arma::sword> coords, arma::cx_fmat item);
    template void set_diag<arma::umat>(arma::umat &matrix, std::tuple<Diag, arma::sword> coords, arma::umat item);
    template void set_diag<arma::imat>(arma::imat &matrix, std::tuple<Diag, arma::sword> coords, arma::imat item);

    template void set_diag<arma::subview<double>>(arma::subview<double> &matrix, std::tuple<Diag, arma::sword> coords, arma::Mat<double> item);
    template void set_diag<arma::subview<float>>(arma::subview<float> &matrix, std::tuple<Diag, arma::sword> coords, arma::Mat<float> item);
    template void set_diag<arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &matrix, std::tuple<Diag, arma::sword> coords, arma::Mat<arma::cx_double> item);
    template void set_diag<arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &matrix, std::tuple<Diag, arma::sword> coords, arma::Mat<arma::cx_float> item);
    template void set_diag<arma::subview<arma::uword>>(arma::subview<arma::uword> &matrix, std::tuple<Diag, arma::sword> coords, arma::Mat<arma::uword> item);
    template void set_diag<arma::subview<arma::sword>>(arma::subview<arma::sword> &matrix, std::tuple<Diag, arma::sword> coords, arma::Mat<arma::sword> item);

    template arma::diagview<double> get_main_diag<arma::mat>(const arma::mat &matrix, const Diag diag_sym);
    template arma::diagview<float> get_main_diag<arma::fmat>(const arma::fmat &matrix, const Diag diag_sym);
    template arma::diagview<arma::cx_double> get_main_diag<arma::cx_mat>(const arma::cx_mat &matrix, const Diag diag_sym);
    template arma::diagview<arma::cx_float> get_main_diag<arma::cx_fmat>(const arma::cx_fmat &matrix, const Diag diag_sym);
    template arma::diagview<arma::uword> get_main_diag<arma::umat>(const arma::umat &matrix, const Diag diag_sym);
    template arma::diagview<arma::sword> get_main_diag<arma::imat>(const arma::imat &matrix, const Diag diag_sym);

    template arma::diagview<double> get_main_diag<arma::subview<double>>(const arma::subview<double> &matrix, const Diag diag_sym);
    template arma::diagview<float> get_main_diag<arma::subview<float>>(const arma::subview<float> &matrix, const Diag diag_sym);
    template arma::diagview<arma::cx_double> get_main_diag<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, const Diag diag_sym);
    template arma::diagview<arma::cx_float> get_main_diag<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, const Diag diag_sym);
    template arma::diagview<arma::uword> get_main_diag<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, const Diag diag_sym);
    template arma::diagview<arma::sword> get_main_diag<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, const Diag diag_sym);

    template void set_main_diag<arma::mat>(arma::mat &matrix, Diag diag_sym, arma::mat item);
    template void set_main_diag<arma::fmat>(arma::fmat &matrix, Diag diag_sym, arma::fmat item);
    template void set_main_diag<arma::cx_mat>(arma::cx_mat &matrix, Diag diag_sym, arma::cx_mat item);
    template void set_main_diag<arma::cx_fmat>(arma::cx_fmat &matrix, Diag diag_sym, arma::cx_fmat item);
    template void set_main_diag<arma::umat>(arma::umat &matrix, Diag diag_sym, arma::umat item);
    template void set_main_diag<arma::imat>(arma::imat &matrix, Diag diag_sym, arma::imat item);

    template void set_main_diag<arma::subview<double>>(arma::subview<double> &matrix, Diag diag_sym, arma::Mat<double> item);
    template void set_main_diag<arma::subview<float>>(arma::subview<float> &matrix, Diag diag_sym, arma::Mat<float> item);
    template void set_main_diag<arma::subview<arma::cx_double>>(arma::subview<arma::cx_double> &matrix, Diag diag_sym, arma::Mat<arma::cx_double> item);
    template void set_main_diag<arma::subview<arma::cx_float>>(arma::subview<arma::cx_float> &matrix, Diag diag_sym, arma::Mat<arma::cx_float> item);
    template void set_main_diag<arma::subview<arma::uword>>(arma::subview<arma::uword> &matrix, Diag diag_sym, arma::Mat<arma::uword> item);
    template void set_main_diag<arma::subview<arma::sword>>(arma::subview<arma::sword> &matrix, Diag diag_sym, arma::Mat<arma::sword> item);
}