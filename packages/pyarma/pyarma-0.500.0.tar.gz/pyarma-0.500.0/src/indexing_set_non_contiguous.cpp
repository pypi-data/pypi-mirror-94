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
#include "indexing/non_contiguous/cols.hpp"
#include "indexing/non_contiguous/rows.hpp"
#include "indexing/non_contiguous/elem.hpp"
#include "indexing/non_contiguous/submat.hpp"

namespace py = pybind11;

namespace pyarma {
    // Exposes Python index operator '[]' overloads for setting non-contiguous submatrix views
    template<typename T>
    void expose_set_non_contiguous(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        /* Expose non-contiguous getters (only matrices have access to this)
           subview_elem requires that the vector of indices be kept alive */
        py_class.def("__setitem__", &set_elem<T>)
            .def("__setitem__", &set_cols<T>)
            .def("__setitem__", &set_rows<T>)
            .def("__setitem__", &set_submat<T>);
    }

    template void expose_set_non_contiguous<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_set_non_contiguous<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_set_non_contiguous<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_set_non_contiguous<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_set_non_contiguous<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_set_non_contiguous<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}
