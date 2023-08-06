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
       Indices are input as [start_row:stop_row, start_col:stop_col, start_slice:stop_slice]
       If left blank, start indices are 0
       and stop indices are the last index */
    template<typename T>
    std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> cube_get_indices(const T &cube, py::slice row_slice, py::slice col_slice, py::slice slice_slice) {
        std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> indices;
        arma::uword start_row, start_col, start_slice, stop_row, stop_col, stop_slice;
        arma::uword last_row = cube.n_rows - 1;
        arma::uword last_col = cube.n_cols - 1;
        arma::uword last_slice = cube.n_slices - 1;
        py::object st_col = col_slice.attr("start"), sp_col = col_slice.attr("stop"),
                   st_row = row_slice.attr("start"), sp_row = row_slice.attr("stop"),
                   st_slice= slice_slice.attr("start"), sp_slice = slice_slice.attr("stop");
        bool is_start_col_none = st_col.is(py::none()), is_stop_col_none = sp_col.is(py::none()),
             is_start_row_none = st_row.is(py::none()), is_stop_row_none = sp_row.is(py::none()),
             is_start_slice_none = st_slice.is(py::none()), is_stop_slice_none = sp_slice.is(py::none());

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
        if (!is_start_slice_none) {
            start_slice = st_slice.cast<arma::uword>();
        }
        if (!is_stop_slice_none) {
            stop_slice = sp_slice.cast<arma::uword>();
        }

        // Start getting
        if (is_start_slice_none && is_stop_slice_none) {
            // Start getting
            if (is_start_row_none) { // m[:(), ():()]
                if (is_stop_row_none) { // m[:, ():()]
                    if (is_start_col_none) { // m[:, :()]
                        if (is_stop_col_none) { // This is where m[:,:] is passed: that's the same cube.
                            indices = std::make_tuple(0, last_row, 0, last_col, 0, last_slice);
                        } else { // This is m[:, :y1] where you get all rows but limit columns to y1.
                            indices = std::make_tuple(0, last_row, 0, stop_col, 0, last_slice);
                        }
                    } else { // So m[:, y0:(y1 or none)]
                        if (is_stop_col_none) { // m[:, y0:]
                            indices = std::make_tuple(0, last_row, start_col, last_col, 0, last_slice);
                        } else { // m[:, y0:y1]
                            indices = std::make_tuple(0, last_row, start_col, stop_col, 0, last_slice);
                        }             
                    }
                } else { // m[:x1, ():()]
                    if (is_start_col_none) { // m[:x1, :()]
                        if (is_stop_col_none) { // m[:x1, :]
                            indices = std::make_tuple(0, stop_row, 0, last_col, 0, last_slice);
                        } else { // m [:x1, :y1]
                            indices = std::make_tuple(0, stop_row, 0, stop_col, 0, last_slice);
                        }
                    } else { // So m[:x1, y0:()]
                        if (is_stop_col_none) { // m[:x1, y0:]
                            indices = std::make_tuple(0, stop_row, start_col, last_col, 0, last_slice);
                        } else { // m[:x1, y0:y1]
                            indices = std::make_tuple(0, stop_row, start_col, stop_col, 0, last_slice);
                        }             
                    }
                }
            } else { // m[x0:(), ():()]
                if (is_stop_row_none) { // m[x0:, ():()]
                    if (is_start_col_none) { // m[x0:, :()]
                        if (is_stop_col_none) { // m[x0:, :]
                            indices = std::make_tuple(start_row, last_row, 0, last_col, 0, last_slice);
                        } else { // m[x0:, :y1]
                            indices = std::make_tuple(start_row, last_row, 0, stop_col, 0, last_slice);
                        }
                    } else { // So m[x0:, y0:()]
                        if (is_stop_col_none) { // m[x0:, y0:]
                            indices = std::make_tuple(start_row, last_row, start_col, last_col, 0, last_slice);
                        } else { // m[x0:, y0:y1]
                            indices = std::make_tuple(start_row, last_row, start_col, stop_col, 0, last_slice);
                        }             
                    }
                } else { // m[x0:x1, ():()]
                    if (is_start_col_none) { // m[x0:x1, :()]
                        if (is_stop_col_none) { // m[x0:x1, :]
                            indices = std::make_tuple(start_row, stop_row, 0, last_col, 0, last_slice);
                        } else { // m [x0:x1, :y1]
                            indices = std::make_tuple(start_row, stop_row, 0, stop_col, 0, last_slice);
                        }
                    } else { // So m[x0:x1, y0:()]
                        if (is_stop_col_none) { // m[x0:x1, y0:]
                            indices = std::make_tuple(start_row, stop_row, start_col, last_col, 0, last_slice);
                        } else { // m[x0:x1, y0:y1]
                            indices = std::make_tuple(start_row, stop_row, start_col, stop_col, 0, last_slice);
                        }             
                    }
                }
            }
        } else if (!is_start_slice_none && is_stop_slice_none) {
            // Start getting
            if (is_start_row_none) { // m[:(), ():()]
                if (is_stop_row_none) { // m[:, ():()]
                    if (is_start_col_none) { // m[:, :()]
                        if (is_stop_col_none) { // This is where m[:,:] is passed: that's the same cube.
                            indices = std::make_tuple(0, last_row, 0, last_col, start_slice, last_slice);
                        } else { // This is m[:, :y1] where you get all rows but limit columns to y1.
                            indices = std::make_tuple(0, last_row, 0, stop_col, start_slice, last_slice);
                        }
                    } else { // So m[:, y0:(y1 or none)]
                        if (is_stop_col_none) { // m[:, y0:]
                            indices = std::make_tuple(0, last_row, start_col, last_col, start_slice, last_slice);
                        } else { // m[:, y0:y1]
                            indices = std::make_tuple(0, last_row, start_col, stop_col, start_slice, last_slice);
                        }             
                    }
                } else { // m[:x1, ():()]
                    if (is_start_col_none) { // m[:x1, :()]
                        if (is_stop_col_none) { // m[:x1, :]
                            indices = std::make_tuple(0, stop_row, 0, last_col, start_slice, last_slice);
                        } else { // m [:x1, :y1]
                            indices = std::make_tuple(0, stop_row, 0, stop_col, start_slice, last_slice);
                        }
                    } else { // So m[:x1, y0:()]
                        if (is_stop_col_none) { // m[:x1, y0:]
                            indices = std::make_tuple(0, stop_row, start_col, last_col, start_slice, last_slice);
                        } else { // m[:x1, y0:y1]
                            indices = std::make_tuple(0, stop_row, start_col, stop_col, start_slice, last_slice);
                        }             
                    }
                }
            } else { // m[x0:(), ():()]
                if (is_stop_row_none) { // m[x0:, ():()]
                    if (is_start_col_none) { // m[x0:, :()]
                        if (is_stop_col_none) { // m[x0:, :]
                            indices = std::make_tuple(start_row, last_row, 0, last_col, start_slice, last_slice);
                        } else { // m[x0:, :y1]
                            indices = std::make_tuple(start_row, last_row, 0, stop_col, start_slice, last_slice);
                        }
                    } else { // So m[x0:, y0:()]
                        if (is_stop_col_none) { // m[x0:, y0:]
                            indices = std::make_tuple(start_row, last_row, start_col, last_col, start_slice, last_slice);
                        } else { // m[x0:, y0:y1]
                            indices = std::make_tuple(start_row, last_row, start_col, stop_col, start_slice, last_slice);
                        }             
                    }
                } else { // m[x0:x1, ():()]
                    if (is_start_col_none) { // m[x0:x1, :()]
                        if (is_stop_col_none) { // m[x0:x1, :]
                            indices = std::make_tuple(start_row, stop_row, 0, last_col, start_slice, last_slice);
                        } else { // m [x0:x1, :y1]
                            indices = std::make_tuple(start_row, stop_row, 0, stop_col, start_slice, last_slice);
                        }
                    } else { // So m[x0:x1, y0:()]
                        if (is_stop_col_none) { // m[x0:x1, y0:]
                            indices = std::make_tuple(start_row, stop_row, start_col, last_col, start_slice, last_slice);
                        } else { // m[x0:x1, y0:y1]
                            indices = std::make_tuple(start_row, stop_row, start_col, stop_col, start_slice, last_slice);
                        }             
                    }
                }
            }
        } else if (is_start_slice_none && !is_stop_slice_none) {
            // Start getting
            if (is_start_row_none) { // m[:(), ():()]
                if (is_stop_row_none) { // m[:, ():()]
                    if (is_start_col_none) { // m[:, :()]
                        if (is_stop_col_none) { // This is where m[:,:] is passed: that's the same cube.
                            indices = std::make_tuple(0, last_row, 0, last_col, 0, stop_slice);
                        } else { // This is m[:, :y1] where you get all rows but limit columns to y1.
                            indices = std::make_tuple(0, last_row, 0, stop_col, 0, stop_slice);
                        }
                    } else { // So m[:, y0:(y1 or none)]
                        if (is_stop_col_none) { // m[:, y0:]
                            indices = std::make_tuple(0, last_row, start_col, last_col, 0, stop_slice);
                        } else { // m[:, y0:y1]
                            indices = std::make_tuple(0, last_row, start_col, stop_col, 0, stop_slice);
                        }             
                    }
                } else { // m[:x1, ():()]
                    if (is_start_col_none) { // m[:x1, :()]
                        if (is_stop_col_none) { // m[:x1, :]
                            indices = std::make_tuple(0, stop_row, 0, last_col, 0, stop_slice);
                        } else { // m [:x1, :y1]
                            indices = std::make_tuple(0, stop_row, 0, stop_col, 0, stop_slice);
                        }
                    } else { // So m[:x1, y0:()]
                        if (is_stop_col_none) { // m[:x1, y0:]
                            indices = std::make_tuple(0, stop_row, start_col, last_col, 0, stop_slice);
                        } else { // m[:x1, y0:y1]
                            indices = std::make_tuple(0, stop_row, start_col, stop_col, 0, stop_slice);
                        }             
                    }
                }
            } else { // m[x0:(), ():()]
                if (is_stop_row_none) { // m[x0:, ():()]
                    if (is_start_col_none) { // m[x0:, :()]
                        if (is_stop_col_none) { // m[x0:, :]
                            indices = std::make_tuple(start_row, last_row, 0, last_col, 0, stop_slice);
                        } else { // m[x0:, :y1]
                            indices = std::make_tuple(start_row, last_row, 0, stop_col, 0, stop_slice);
                        }
                    } else { // So m[x0:, y0:()]
                        if (is_stop_col_none) { // m[x0:, y0:]
                            indices = std::make_tuple(start_row, last_row, start_col, last_col, 0, stop_slice);
                        } else { // m[x0:, y0:y1]
                            indices = std::make_tuple(start_row, last_row, start_col, stop_col, 0, stop_slice);
                        }             
                    }
                } else { // m[x0:x1, ():()]
                    if (is_start_col_none) { // m[x0:x1, :()]
                        if (is_stop_col_none) { // m[x0:x1, :]
                            indices = std::make_tuple(start_row, stop_row, 0, last_col, 0, stop_slice);
                        } else { // m [x0:x1, :y1]
                            indices = std::make_tuple(start_row, stop_row, 0, stop_col, 0, stop_slice);
                        }
                    } else { // So m[x0:x1, y0:()]
                        if (is_stop_col_none) { // m[x0:x1, y0:]
                            indices = std::make_tuple(start_row, stop_row, start_col, last_col, 0, stop_slice);
                        } else { // m[x0:x1, y0:y1]
                            indices = std::make_tuple(start_row, stop_row, start_col, stop_col, 0, stop_slice);
                        }             
                    }
                }
            }
        } else {
            // Start getting
            if (is_start_row_none) { // m[:(), ():()]
                if (is_stop_row_none) { // m[:, ():()]
                    if (is_start_col_none) { // m[:, :()]
                        if (is_stop_col_none) { // This is where m[:,:] is passed: that's the same cube.
                            indices = std::make_tuple(0, last_row, 0, last_col, start_slice, stop_slice);
                        } else { // This is m[:, :y1] where you get all rows but limit columns to y1.
                            indices = std::make_tuple(0, last_row, 0, stop_col, start_slice, stop_slice);
                        }
                    } else { // So m[:, y0:(y1 or none)]
                        if (is_stop_col_none) { // m[:, y0:]
                            indices = std::make_tuple(0, last_row, start_col, last_col, start_slice, stop_slice);
                        } else { // m[:, y0:y1]
                            indices = std::make_tuple(0, last_row, start_col, stop_col, start_slice, stop_slice);
                        }             
                    }
                } else { // m[:x1, ():()]
                    if (is_start_col_none) { // m[:x1, :()]
                        if (is_stop_col_none) { // m[:x1, :]
                            indices = std::make_tuple(0, stop_row, 0, last_col, start_slice, stop_slice);
                        } else { // m [:x1, :y1]
                            indices = std::make_tuple(0, stop_row, 0, stop_col, start_slice, stop_slice);
                        }
                    } else { // So m[:x1, y0:()]
                        if (is_stop_col_none) { // m[:x1, y0:]
                            indices = std::make_tuple(0, stop_row, start_col, last_col, start_slice, stop_slice);
                        } else { // m[:x1, y0:y1]
                            indices = std::make_tuple(0, stop_row, start_col, stop_col, start_slice, stop_slice);
                        }             
                    }
                }
            } else { // m[x0:(), ():()]
                if (is_stop_row_none) { // m[x0:, ():()]
                    if (is_start_col_none) { // m[x0:, :()]
                        if (is_stop_col_none) { // m[x0:, :]
                            indices = std::make_tuple(start_row, last_row, 0, last_col, start_slice, stop_slice);
                        } else { // m[x0:, :y1]
                            indices = std::make_tuple(start_row, last_row, 0, stop_col, start_slice, stop_slice);
                        }
                    } else { // So m[x0:, y0:()]
                        if (is_stop_col_none) { // m[x0:, y0:]
                            indices = std::make_tuple(start_row, last_row, start_col, last_col, start_slice, stop_slice);
                        } else { // m[x0:, y0:y1]
                            indices = std::make_tuple(start_row, last_row, start_col, stop_col, start_slice, stop_slice);
                        }             
                    }
                } else { // m[x0:x1, ():()]
                    if (is_start_col_none) { // m[x0:x1, :()]
                        if (is_stop_col_none) { // m[x0:x1, :]
                            indices = std::make_tuple(start_row, stop_row, 0, last_col, start_slice, stop_slice);
                        } else { // m [x0:x1, :y1]
                            indices = std::make_tuple(start_row, stop_row, 0, stop_col, start_slice, stop_slice);
                        }
                    } else { // So m[x0:x1, y0:()]
                        if (is_stop_col_none) { // m[x0:x1, y0:]
                            indices = std::make_tuple(start_row, stop_row, start_col, last_col, start_slice, stop_slice);
                        } else { // m[x0:x1, y0:y1]
                            indices = std::make_tuple(start_row, stop_row, start_col, stop_col, start_slice, stop_slice);
                        }             
                    }
                }
            }    
        }
        return indices;
    }

    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> cube_get_indices<arma::Cube<arma::sword>>(const arma::Cube<arma::sword> &cube, py::slice row_slice, py::slice col_slice, py::slice slice_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> cube_get_indices<arma::Cube<arma::uword>>(const arma::Cube<arma::uword> &cube, py::slice row_slice, py::slice col_slice, py::slice slice_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> cube_get_indices<arma::Cube<arma::cx_float>>(const arma::Cube<arma::cx_float> &cube, py::slice row_slice, py::slice col_slice, py::slice slice_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> cube_get_indices<arma::Cube<arma::cx_double>>(const arma::Cube<arma::cx_double> &cube, py::slice row_slice, py::slice col_slice, py::slice slice_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> cube_get_indices<arma::Cube<float>>(const arma::Cube<float> &cube, py::slice row_slice, py::slice col_slice, py::slice slice_slice);
    template std::tuple<arma::uword, arma::uword, arma::uword, arma::uword, arma::uword, arma::uword> cube_get_indices<arma::Cube<double>>(const arma::Cube<double> &cube, py::slice row_slice, py::slice col_slice, py::slice slice_slice);
}
