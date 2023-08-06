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
using namespace pybind11::literals;

namespace pyarma {
    // Expose row and column manipulation methods (i.e. swap_rows())
    template<typename T>
    void expose_rows_cols(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        using Class = arma::Mat<T>;
        py_class.def("swap_rows", [](Class &matrix, const arma::uword &row1, const arma::uword &row2) { matrix.swap_rows(row1, row2); })

            .def("swap_cols", [](Class &matrix, const arma::uword &col1, const arma::uword &col2) { matrix.swap_cols(col1, col2); })

            .def("insert_rows", [](Class &matrix, const arma::uword &row_num, Class &insert) {
                matrix.insert_rows(row_num, insert);
            })
            .def("insert_rows", [](Class &matrix, const arma::uword &row_num, const arma::uword &num_rows, bool set_to_zero = true) {
                matrix.insert_rows(row_num, num_rows, set_to_zero);
            }, "row_num"_a, "num_rows"_a, "set_to_zero"_a = true)
            .def("insert_cols", [](Class &matrix, const arma::uword &col_num, Class &insert) {
                matrix.insert_cols(col_num, insert);
            })
            .def("insert_cols", [](Class &matrix, const arma::uword &col_num, const arma::uword &num_cols, bool set_to_zero = true) {
                matrix.insert_cols(col_num, num_cols, set_to_zero);
            }, "col_num"_a, "num_cols"_a, "set_to_zero"_a = true)

            .def("shed_row", [](Class &matrix, const arma::uword &row_num) { matrix.shed_row(row_num); })
            .def("shed_rows", [](Class &matrix, arma::uword first_row, arma::uword last_row) { matrix.shed_rows(first_row, last_row); })
            .def("shed_rows", [](Class &matrix, arma::Mat<arma::uword> indices) { matrix.shed_rows(indices); })
            .def("shed_col", [](Class &matrix, const arma::uword &col_num) { matrix.shed_col(col_num); })
            .def("shed_cols", [](Class &matrix, arma::uword first_col, arma::uword last_col) { matrix.shed_cols(first_col, last_col); })
            .def("shed_cols", [](Class &matrix, arma::Mat<arma::uword> indices) { matrix.shed_cols(indices); }); 
    }

    template void expose_rows_cols<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_rows_cols<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_rows_cols<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_rows_cols<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_rows_cols<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_rows_cols<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}