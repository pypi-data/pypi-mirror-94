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
#include "arithmetic/add/add_rev.hpp"
#include "arithmetic/multiply/multiply_rev.hpp"
#include "arithmetic/subtract/subtract_rev.hpp"
#include "arithmetic/divide/divide_rev.hpp"
#include "arithmetic/schur/schur_rev.hpp"

namespace py = pybind11;

namespace pyarma {     
    // Defines reverse type-promotion arithmetic operators
    // TODO: currently not working using broadcasting
    template<typename LHS, typename RHS>
    void expose_rops(py::class_<LHS, arma::Base<typename LHS::elem_type, LHS>> &py_class) {
        py_class.def("__add__", &add_r<LHS, RHS>, py::is_operator())
                .def("__sub__", &subtract_r<LHS, RHS>, py::is_operator())
                .def("__iadd__", &add_r<LHS, RHS>, py::is_operator())
                .def("__isub__", &subtract_r<LHS, RHS>, py::is_operator())
                .def("__mul__", &multiply_r<LHS, RHS>, py::is_operator())
                .def("__imul__", &multiply_r<LHS, RHS>, py::is_operator())
                .def("__truediv__", &divide_r<LHS, RHS>, py::is_operator())
                .def("__idiv__", &divide_r<LHS, RHS>, py::is_operator())
                .def("__matmul__", &schur_r<LHS, RHS>, py::is_operator())
                .def("__imatmul__", &schur_r<LHS, RHS>, py::is_operator());
    }

    template void expose_rops<arma::mat, arma::cx_mat>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_rops<arma::fmat, arma::cx_mat>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_rops<arma::fmat, arma::cx_fmat>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_rops<arma::fmat, arma::mat>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_rops<arma::umat, arma::mat>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_rops<arma::umat, arma::fmat>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_rops<arma::imat, arma::mat>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    template void expose_rops<arma::imat, arma::fmat>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}