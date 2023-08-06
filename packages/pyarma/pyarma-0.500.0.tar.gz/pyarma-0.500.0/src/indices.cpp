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

#include "pybind11/pybind11.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    /* Gets the indices input by a user 
       Indices are input as [start_row:stop_row, start_col:stop_col]
       If left blank, start indices are 0
       and stop indices are the last index */
    template<typename T>
    std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices(const T &matrix, py::slice row_slice, py::slice col_slice) {
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> indices;
        arma::uword start_row, start_col, stop_row, stop_col;
        arma::uword last_row = matrix.n_rows - 1;
        arma::uword last_col = matrix.n_cols - 1;
        py::object st_col = col_slice.attr("start"), sp_col = col_slice.attr("stop"),
                st_row = row_slice.attr("start"), sp_row = row_slice.attr("stop");
        bool is_start_col_none = st_col.is(py::none()), is_stop_col_none = sp_col.is(py::none()),
            is_start_row_none = st_row.is(py::none()), is_stop_row_none = sp_row.is(py::none());

        // If it's NOT None, cast as arma::uword. This prevents users from inputting anything else
        if (!is_start_col_none) {
            start_col = st_col.cast<arma::uword>();
        }
        if (!is_stop_col_none) {
            stop_col = sp_col.cast<arma::uword>();
        }
        if (!is_start_row_none) {
            start_row = st_row.cast<arma::uword>();
        }
        if (!is_stop_row_none) {
            stop_row = sp_row.cast<arma::uword>();
        }
        // Start getting
        if (is_start_row_none) { // m[:(), ():()]
            if (is_stop_row_none) { // m[:, ():()]
                if (is_start_col_none) { // m[:, :()]
                    if (is_stop_col_none) { // This is where m[:,:] is passed: that's the same matrix.
                        indices = std::make_tuple(0, last_row, 0, last_col);
                    } else { // This is m[:, :y1] where you get all rows but limit columns to y1.
                        indices = std::make_tuple(0, last_row, 0, stop_col);
                    }
                } else { // So m[:, y0:(y1 or none)]
                    if (is_stop_col_none) { // m[:, y0:]
                        indices = std::make_tuple(0, last_row, start_col, last_col);
                    } else { // m[:, y0:y1]
                        indices = std::make_tuple(0, last_row, start_col, stop_col);
                    }             
                }
            } else { // m[:x1, ():()]
                if (is_start_col_none) { // m[:x1, :()]
                    if (is_stop_col_none) { // m[:x1, :]
                        indices = std::make_tuple(0, stop_row, 0, last_col);
                    } else { // m [:x1, :y1]
                        indices = std::make_tuple(0, stop_row, 0, stop_col);
                    }
                } else { // So m[:x1, y0:()]
                    if (is_stop_col_none) { // m[:x1, y0:]
                        indices = std::make_tuple(0, stop_row, start_col, last_col);
                    } else { // m[:x1, y0:y1]
                        indices = std::make_tuple(0, stop_row, start_col, stop_col);
                    }             
                }
            }
        } else { // m[x0:(), ():()]
            if (is_stop_row_none) { // m[x0:, ():()]
                if (is_start_col_none) { // m[x0:, :()]
                    if (is_stop_col_none) { // m[x0:, :]
                        indices = std::make_tuple(start_row, last_row, 0, last_col);
                    } else { // m[x0:, :y1]
                        indices = std::make_tuple(start_row, last_row, 0, stop_col);
                    }
                } else { // So m[x0:, y0:()]
                    if (is_stop_col_none) { // m[x0:, y0:]
                        indices = std::make_tuple(start_row, last_row, start_col, last_col);
                    } else { // m[x0:, y0:y1]
                        indices = std::make_tuple(start_row, last_row, start_col, stop_col);
                    }             
                }
            } else { // m[x0:x1, ():()]
                if (is_start_col_none) { // m[x0:x1, :()]
                    if (is_stop_col_none) { // m[x0:x1, :]
                        indices = std::make_tuple(start_row, stop_row, 0, last_col);
                    } else { // m [x0:x1, :y1]
                        indices = std::make_tuple(start_row, stop_row, 0, stop_col);
                    }
                } else { // So m[x0:x1, y0:()]
                    if (is_stop_col_none) { // m[x0:x1, y0:]
                        indices = std::make_tuple(start_row, stop_row, start_col, last_col);
                    } else { // m[x0:x1, y0:y1]
                        indices = std::make_tuple(start_row, stop_row, start_col, stop_col);
                    }             
                }
            }
        }
        return indices;
    }

    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Mat<double>>(const arma::Mat<double> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::subview<double>>(const arma::subview<double> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Cube<double>>(const arma::Cube<double> &matrix, py::slice row_slice, py::slice col_slice);

    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Mat<float>>(const arma::Mat<float> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::subview<float>>(const arma::subview<float> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Cube<float>>(const arma::Cube<float> &matrix, py::slice row_slice, py::slice col_slice);

    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Mat<arma::cx_double>>(const arma::Mat<arma::cx_double> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::subview<arma::cx_double>>(const arma::subview<arma::cx_double> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &matrix, py::slice row_slice, py::slice col_slice);

    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Mat<arma::cx_float>>(const arma::Mat<arma::cx_float> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::subview<arma::cx_float>>(const arma::subview<arma::cx_float> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &matrix, py::slice row_slice, py::slice col_slice);

    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Mat<arma::uword>>(const arma::Mat<arma::uword> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::subview<arma::uword>>(const arma::subview<arma::uword> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &matrix, py::slice row_slice, py::slice col_slice);

    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Mat<arma::sword>>(const arma::Mat<arma::sword> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::subview<arma::sword>>(const arma::subview<arma::sword> &matrix, py::slice row_slice, py::slice col_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword> get_indices<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &matrix, py::slice row_slice, py::slice col_slice);
}
