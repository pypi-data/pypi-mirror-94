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

// // #include "force_inst_diag.hpp"
// // #include "force_inst_sub.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "arithmetic/add/add_diag_rev.hpp"
#include "arithmetic/multiply/multiply.hpp"
#include "arithmetic/subtract/subtract_diag_rev.hpp"
#include "arithmetic/divide/divide_diag_rev.hpp"
#include "arithmetic/schur/schur_diag_rev.hpp"

namespace py = pybind11;

namespace pyarma {     
    // Defines operations with diagviews where the right operand can be broadcast into
    template<typename T, typename U>
    void expose_diagview_ops_r(py::class_<T, arma::Base<typename T::elem_type, T>> &py_class) {
        py_class.def("__add__", &add_mat_r<U>, py::is_operator())
                .def("__sub__", &subtract_mat_r<U>, py::is_operator())
                .def("__iadd__", &add_mat_r<U>, py::is_operator())
                .def("__isub__", &subtract_mat_r<U>, py::is_operator())
                .def("__mul__", &multiply_mat<T, U>, py::is_operator())
                .def("__imul__", &multiply_mat<T, U>, py::is_operator())
                .def("__truediv__", &divide_mat_r<U>, py::is_operator())
                .def("__idiv__", &divide_mat_r<U>, py::is_operator())
                .def("__matmul__", &schur_mat_r<U>, py::is_operator())
                .def("__imatmul__", &schur_mat_r<U>, py::is_operator());
    }

    template void expose_diagview_ops_r<arma::diagview<double>, arma::Mat<double>>(py::class_<arma::diagview<double>, arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_diagview_ops_r<arma::diagview<double>, arma::subview<double>>(py::class_<arma::diagview<double>, arma::Base<double, arma::diagview<double>>> &py_class);
    template void expose_diagview_ops_r<arma::diagview<float>, arma::Mat<float>>(py::class_<arma::diagview<float>, arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_diagview_ops_r<arma::diagview<float>, arma::subview<float>>(py::class_<arma::diagview<float>, arma::Base<float, arma::diagview<float>>> &py_class);
    template void expose_diagview_ops_r<arma::diagview<arma::cx_double>, arma::Mat<arma::cx_double>>(py::class_<arma::diagview<arma::cx_double>, arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    // template void expose_diagview_ops_r<arma::diagview<arma::cx_double>, arma::subview<arma::cx_double>>(py::class_<arma::diagview<arma::cx_double>, arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    template void expose_diagview_ops_r<arma::diagview<arma::cx_float>, arma::Mat<arma::cx_float>>(py::class_<arma::diagview<arma::cx_float>, arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    // template void expose_diagview_ops_r<arma::diagview<arma::cx_float>, arma::subview<arma::cx_float>>(py::class_<arma::diagview<arma::cx_float>, arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    template void expose_diagview_ops_r<arma::diagview<arma::uword>, arma::Mat<arma::uword>>(py::class_<arma::diagview<arma::uword>, arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_diagview_ops_r<arma::diagview<arma::uword>, arma::subview<arma::uword>>(py::class_<arma::diagview<arma::uword>, arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    template void expose_diagview_ops_r<arma::diagview<arma::sword>, arma::Mat<arma::sword>>(py::class_<arma::diagview<arma::sword>, arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    // template void expose_diagview_ops_r<arma::diagview<arma::sword>, arma::subview<arma::sword>>(py::class_<arma::diagview<arma::sword>, arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
}