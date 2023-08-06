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
    class Head_Rows {};
    class Head_Cols {};
    class Tail_Rows {};
    class Tail_Cols {};
    
    template<typename T>
    arma::subview<T> get_head_rows(const arma::Mat<T> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows) { 
        return matrix.head_rows(std::get<1>(n_rows));
    }

    template<typename T>
    arma::subview<T> get_head_cols(const arma::Mat<T> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols) { 
        return matrix.head_cols(std::get<1>(n_cols));
    }

    template<typename T>
    arma::subview<T> get_tail_rows(const arma::Mat<T> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows) { 
        return matrix.tail_rows(std::get<1>(n_rows));
    }

    template<typename T>
    arma::subview<T> get_tail_cols(const arma::Mat<T> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols) { 
        return matrix.tail_cols(std::get<1>(n_cols));
    }

    template<typename T>
    void set_head_rows(arma::Mat<T> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<T> &item) { 
        matrix.head_rows(std::get<1>(n_rows)) = item;
    }

    template<typename T>
    void set_head_cols(arma::Mat<T> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<T> &item) { 
        matrix.head_cols(std::get<1>(n_cols)) = item;
    }

    template<typename T>
    void set_tail_rows(arma::Mat<T> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<T> &item) { 
        matrix.tail_rows(std::get<1>(n_rows)) = item;
    }

    template<typename T>
    void set_tail_cols(arma::Mat<T> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<T> &item) { 
        matrix.tail_cols(std::get<1>(n_cols)) = item;
    }

    template arma::subview<double> get_head_rows<double>(const arma::Mat<double> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows);
    template arma::subview<double> get_head_cols<double>(const arma::Mat<double> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols);
    template arma::subview<double> get_tail_rows<double>(const arma::Mat<double> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows);
    template arma::subview<double> get_tail_cols<double>(const arma::Mat<double> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols);
    template void set_head_rows<double>(arma::Mat<double> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<double> &item);
    template void set_head_cols<double>(arma::Mat<double> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<double> &item);
    template void set_tail_rows<double>(arma::Mat<double> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<double> &item);
    template void set_tail_cols<double>(arma::Mat<double> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<double> &item);

    template arma::subview<float> get_head_rows<float>(const arma::Mat<float> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows);
    template arma::subview<float> get_head_cols<float>(const arma::Mat<float> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols);
    template arma::subview<float> get_tail_rows<float>(const arma::Mat<float> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows);
    template arma::subview<float> get_tail_cols<float>(const arma::Mat<float> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols);
    template void set_head_rows<float>(arma::Mat<float> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<float> &item);
    template void set_head_cols<float>(arma::Mat<float> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<float> &item);
    template void set_tail_rows<float>(arma::Mat<float> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<float> &item);
    template void set_tail_cols<float>(arma::Mat<float> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<float> &item);

    template arma::subview<arma::cx_double> get_head_rows<arma::cx_double>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows);
    template arma::subview<arma::cx_double> get_head_cols<arma::cx_double>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols);
    template arma::subview<arma::cx_double> get_tail_rows<arma::cx_double>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows);
    template arma::subview<arma::cx_double> get_tail_cols<arma::cx_double>(const arma::Mat<arma::cx_double> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols);
    template void set_head_rows<arma::cx_double>(arma::Mat<arma::cx_double> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<arma::cx_double> &item);
    template void set_head_cols<arma::cx_double>(arma::Mat<arma::cx_double> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<arma::cx_double> &item);
    template void set_tail_rows<arma::cx_double>(arma::Mat<arma::cx_double> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<arma::cx_double> &item);
    template void set_tail_cols<arma::cx_double>(arma::Mat<arma::cx_double> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<arma::cx_double> &item);

    template arma::subview<arma::cx_float> get_head_rows<arma::cx_float>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows);
    template arma::subview<arma::cx_float> get_head_cols<arma::cx_float>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols);
    template arma::subview<arma::cx_float> get_tail_rows<arma::cx_float>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows);
    template arma::subview<arma::cx_float> get_tail_cols<arma::cx_float>(const arma::Mat<arma::cx_float> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols);
    template void set_head_rows<arma::cx_float>(arma::Mat<arma::cx_float> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<arma::cx_float> &item);
    template void set_head_cols<arma::cx_float>(arma::Mat<arma::cx_float> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<arma::cx_float> &item);
    template void set_tail_rows<arma::cx_float>(arma::Mat<arma::cx_float> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<arma::cx_float> &item);
    template void set_tail_cols<arma::cx_float>(arma::Mat<arma::cx_float> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<arma::cx_float> &item);

    template arma::subview<arma::uword> get_head_rows<arma::uword>(const arma::Mat<arma::uword> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows);
    template arma::subview<arma::uword> get_head_cols<arma::uword>(const arma::Mat<arma::uword> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols);
    template arma::subview<arma::uword> get_tail_rows<arma::uword>(const arma::Mat<arma::uword> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows);
    template arma::subview<arma::uword> get_tail_cols<arma::uword>(const arma::Mat<arma::uword> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols);
    template void set_head_rows<arma::uword>(arma::Mat<arma::uword> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<arma::uword> &item);
    template void set_head_cols<arma::uword>(arma::Mat<arma::uword> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<arma::uword> &item);
    template void set_tail_rows<arma::uword>(arma::Mat<arma::uword> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<arma::uword> &item);
    template void set_tail_cols<arma::uword>(arma::Mat<arma::uword> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<arma::uword> &item);

    template arma::subview<arma::sword> get_head_rows<arma::sword>(const arma::Mat<arma::sword> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows);
    template arma::subview<arma::sword> get_head_cols<arma::sword>(const arma::Mat<arma::sword> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols);
    template arma::subview<arma::sword> get_tail_rows<arma::sword>(const arma::Mat<arma::sword> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows);
    template arma::subview<arma::sword> get_tail_cols<arma::sword>(const arma::Mat<arma::sword> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols);
    template void set_head_rows<arma::sword>(arma::Mat<arma::sword> &matrix, const std::tuple<Head_Rows, arma::uword> n_rows, const arma::Mat<arma::sword> &item);
    template void set_head_cols<arma::sword>(arma::Mat<arma::sword> &matrix, const std::tuple<Head_Cols, arma::uword> n_cols, const arma::Mat<arma::sword> &item);
    template void set_tail_rows<arma::sword>(arma::Mat<arma::sword> &matrix, const std::tuple<Tail_Rows, arma::uword> n_rows, const arma::Mat<arma::sword> &item);
    template void set_tail_cols<arma::sword>(arma::Mat<arma::sword> &matrix, const std::tuple<Tail_Cols, arma::uword> n_cols, const arma::Mat<arma::sword> &item);
}
