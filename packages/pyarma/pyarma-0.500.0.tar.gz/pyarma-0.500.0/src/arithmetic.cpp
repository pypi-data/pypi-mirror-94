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
#include "pybind11/pybind11.h"
#include "armadillo"
#include "arithmetic/add/add.hpp"
#include "arithmetic/multiply/multiply.hpp"
#include "arithmetic/subtract/subtract.hpp"
#include "arithmetic/divide/divide.hpp"
#include "arithmetic/schur/schur.hpp"

namespace py = pybind11;

namespace pyarma {     
    // TODO: For efficiency's sake, iadd could be its own method that modifies the matrix (new)
    // instead of returning a matrix that overwrites the previous matrix (now).
    // Defines arithmetic operators
    template<typename T, typename U>
    void expose_ops(py::class_<T, arma::Base<typename T::elem_type, T>> &py_class) {
        py_class.def("__add__", &add_mat<T, U>, py::is_operator())
                .def("__sub__", &subtract_mat<T, U>, py::is_operator())
                .def("__iadd__", &add_mat<T, U>, py::is_operator())
                .def("__isub__", &subtract_mat<T, U>, py::is_operator())
                .def("__mul__", &multiply_mat<T, U>, py::is_operator())
                .def("__imul__", &multiply_mat<T, U>, py::is_operator())
                .def("__truediv__", &divide_mat<T, U>, py::is_operator())
                .def("__idiv__", &divide_mat<T, U>, py::is_operator())
                .def("__matmul__", &schur_mat<T, U>, py::is_operator())
                .def("__imatmul__", &schur_mat<T, U>, py::is_operator());
    }

    template void expose_ops<arma::Mat<double>, arma::Mat<double>>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_ops<arma::Mat<float>, arma::Mat<float>>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_ops<arma::Mat<arma::cx_double>, arma::Mat<arma::cx_double>>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_ops<arma::Mat<arma::cx_float>, arma::Mat<arma::cx_float>>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_ops<arma::Mat<arma::uword>, arma::Mat<arma::uword>>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_ops<arma::Mat<arma::sword>, arma::Mat<arma::sword>>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);

    template void expose_ops<arma::subview<double>, arma::subview<double>>(py::class_<arma::subview<double>, arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_ops<arma::subview<double>, arma::Mat<double>>(py::class_<arma::subview<double>, arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_ops<arma::subview<float>, arma::subview<float>>(py::class_<arma::subview<float>, arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_ops<arma::subview<float>, arma::Mat<float>>(py::class_<arma::subview<float>, arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_ops<arma::subview<arma::cx_double>, arma::subview<arma::cx_double>>(py::class_<arma::subview<arma::cx_double>, arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    template void expose_ops<arma::subview<arma::cx_double>, arma::Mat<arma::cx_double>>(py::class_<arma::subview<arma::cx_double>, arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    template void expose_ops<arma::subview<arma::cx_float>, arma::subview<arma::cx_float>>(py::class_<arma::subview<arma::cx_float>, arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    template void expose_ops<arma::subview<arma::cx_float>, arma::Mat<arma::cx_float>>(py::class_<arma::subview<arma::cx_float>, arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    template void expose_ops<arma::subview<arma::uword>, arma::subview<arma::uword>>(py::class_<arma::subview<arma::uword>, arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_ops<arma::subview<arma::uword>, arma::Mat<arma::uword>>(py::class_<arma::subview<arma::uword>, arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_ops<arma::subview<arma::sword>, arma::subview<arma::sword>>(py::class_<arma::subview<arma::sword>, arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    template void expose_ops<arma::subview<arma::sword>, arma::Mat<arma::sword>>(py::class_<arma::subview<arma::sword>, arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
}