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

#pragma once
#include "pybind11/pybind11.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    class Head_Rows {};
    class Head_Cols {};
    class Tail_Rows {};
    class Tail_Cols {};
    
    template<typename T>
    arma::subview<T> get_head_rows(const arma::Mat<T> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows);

    template<typename T>
    arma::subview<T> get_head_cols(const arma::Mat<T> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols);

    template<typename T>
    arma::subview<T> get_tail_rows(const arma::Mat<T> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows);

    template<typename T>
    arma::subview<T> get_tail_cols(const arma::Mat<T> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols);

    template<typename T>
    void set_head_rows(arma::Mat<T> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<T> &item);

    template<typename T>
    void set_head_cols(arma::Mat<T> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<T> &item);

    template<typename T>
    void set_tail_rows(arma::Mat<T> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<T> &item);

    template<typename T>
    void set_tail_cols(arma::Mat<T> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<T> &item);
}
