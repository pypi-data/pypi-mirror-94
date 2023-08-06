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

#include "pybind11/pybind11.h"
#include "indexing/diag.hpp"
#include "indexing/head_tail.hpp"
#include "indexing/head_tail_slices.hpp"
#include "indexing/single_slice.hpp"

namespace py = pybind11;

namespace pyarma {
    class Diag;
    class Head_Rows;
    class Head_Cols;
    class Tail_Rows;
    class Tail_Cols;
    class Head_Slices;
    class Tail_Slices;
    class Single_Slice;

    // Expose empty Diag class as attribute
    arma_cold void expose_diag(py::module &m) {
        py::class_<Diag> diag_class (m, "__diag");
        m.attr("diag") = py::cast(Diag());
    }

    // Expose empty classes as attributes
    arma_cold void expose_head_tail(py::module &m) {
        py::class_<Head_Rows>(m, "__head_rows");
        m.attr("head_rows") = py::cast(Head_Rows());

        py::class_<Head_Cols>(m, "__head_cols");
        m.attr("head_cols") = py::cast(Head_Cols());

        py::class_<Tail_Rows>(m, "__tail_rows");
        m.attr("tail_rows") = py::cast(Tail_Rows());

        py::class_<Tail_Cols>(m, "__tail_cols");
        m.attr("tail_cols") = py::cast(Tail_Cols());

        py::class_<Head_Slices>(m, "__head_slices");
        m.attr("head_slices") = py::cast(Head_Slices());

        py::class_<Tail_Slices>(m, "__tail_slices");
        m.attr("tail_slices") = py::cast(Tail_Slices());
    }

    // Expose empty SingleSlice class as attribute
    arma_cold void expose_single_slice(py::module &m) {
        py::class_<Single_Slice> single_slice_class (m, "__single_slice");
        m.attr("single_slice") = py::cast(Single_Slice());
    }
}
