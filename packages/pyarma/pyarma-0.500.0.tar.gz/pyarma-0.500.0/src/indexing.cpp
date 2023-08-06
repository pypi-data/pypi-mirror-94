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

// // #include "force_inst_sub.hpp"
// // #include "force_inst_diag.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "indexing/element.hpp"
#include "indexing/row.hpp"
#include "indexing/col.hpp"
#include "indexing/submatrix.hpp"
#include "indexing/diag.hpp"

namespace py = pybind11;

namespace pyarma {
    // Exposes Python index operator '[]' overloads shared by matrices and subviews
    template<typename T>
    void expose_get_set(py::class_<T, arma::Base<typename T::elem_type, T>> &py_class) {
        using Type = typename T::elem_type;
        using Matrix = arma::Mat<Type>;
        using Diagview = arma::diagview<Type>;
        py_class.def("__getitem__", &get_diag<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_main_diag<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_row<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_col<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_submatrix<T>, py::keep_alive<0,1>())
                
                // .def("__setitem__", &set_row<T, T>)
                .def("__setitem__", &set_row<T>)
                // .def("__setitem__", &set_row<T, Diagview>)
                // .def("__setitem__", &set_row<T, Type>)

                // .def("__setitem__", &set_col<T, T>)
                .def("__setitem__", &set_col<T>)
                // .def("__setitem__", &set_col<T, Diagview>)
                // .def("__setitem__", &set_col<T, Type>)

                // .def("__setitem__", &set_submatrix<T, T>)
                .def("__setitem__", &set_submatrix<T>)
                // .def("__setitem__", &set_submatrix<T, Diagview>)
                // .def("__setitem__", &set_submatrix<T, Type>)

                .def("__setitem__", &set_diag<T>)
                .def("__setitem__", &set_main_diag<T>);
    }

    template void expose_get_set<arma::mat>(py::class_<arma::mat, arma::Base<double, arma::mat>> &py_class);
    template void expose_get_set<arma::fmat>(py::class_<arma::fmat, arma::Base<float, arma::fmat>> &py_class);
    template void expose_get_set<arma::cx_mat>(py::class_<arma::cx_mat, arma::Base<arma::cx_double, arma::cx_mat>> &py_class);
    template void expose_get_set<arma::cx_fmat>(py::class_<arma::cx_fmat, arma::Base<arma::cx_float, arma::cx_fmat>> &py_class);
    template void expose_get_set<arma::umat>(py::class_<arma::umat, arma::Base<arma::uword, arma::umat>> &py_class);
    template void expose_get_set<arma::imat>(py::class_<arma::imat, arma::Base<arma::sword, arma::imat>> &py_class);

    template void expose_get_set<arma::subview<double>>(py::class_<arma::subview<double>, arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_get_set<arma::subview<float>>(py::class_<arma::subview<float>, arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_get_set<arma::subview<arma::cx_double>>(py::class_<arma::subview<arma::cx_double>, arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    template void expose_get_set<arma::subview<arma::cx_float>>(py::class_<arma::subview<arma::cx_float>, arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    template void expose_get_set<arma::subview<arma::uword>>(py::class_<arma::subview<arma::uword>, arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_get_set<arma::subview<arma::sword>>(py::class_<arma::subview<arma::sword>, arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
}