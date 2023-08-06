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
#include "armadillo"
#include "indexing/head_tail.hpp"

namespace py = pybind11;

namespace pyarma {
    // Exposes head/tail_rows/cols index operator overloads
    template<typename T>
    void expose_head_tail(py::class_<T, arma::Base<typename T::elem_type, T>> &py_class) {
        using Type = typename T::elem_type;
        py_class.def("__getitem__", &get_head_rows<Type>)
                .def("__getitem__", &get_head_cols<Type>)
                .def("__getitem__", &get_tail_rows<Type>)
                .def("__getitem__", &get_tail_cols<Type>)
                .def("__setitem__", &set_head_rows<Type>)
                .def("__setitem__", &set_head_cols<Type>)
                .def("__setitem__", &set_tail_rows<Type>)
                .def("__setitem__", &set_tail_cols<Type>);
    }

    template void expose_head_tail<arma::mat>(py::class_<arma::mat, arma::Base<double, arma::mat>> &py_class);
    template void expose_head_tail<arma::fmat>(py::class_<arma::fmat, arma::Base<float, arma::fmat>> &py_class);
    template void expose_head_tail<arma::cx_mat>(py::class_<arma::cx_mat, arma::Base<arma::cx_double, arma::cx_mat>> &py_class);
    template void expose_head_tail<arma::cx_fmat>(py::class_<arma::cx_fmat, arma::Base<arma::cx_float, arma::cx_fmat>> &py_class);
    template void expose_head_tail<arma::umat>(py::class_<arma::umat, arma::Base<arma::uword, arma::umat>> &py_class);
    template void expose_head_tail<arma::imat>(py::class_<arma::imat, arma::Base<arma::sword, arma::imat>> &py_class);
}