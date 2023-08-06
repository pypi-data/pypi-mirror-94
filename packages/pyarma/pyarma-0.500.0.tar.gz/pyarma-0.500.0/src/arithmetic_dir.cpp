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
// // #include "force_inst.hpp"
#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "arithmetic/add/add_dir.hpp"
#include "arithmetic/multiply/multiply_dir.hpp"
#include "arithmetic/subtract/subtract_dir.hpp"
#include "arithmetic/subtract/subtract_dir_rev.hpp"
#include "arithmetic/divide/divide_dir.hpp"
#include "arithmetic/schur/schur_dir.hpp"

namespace py = pybind11;

namespace pyarma {     
    /* Defines operations that do not involve broadcasting.
       This includes diagview operations and scalar operations. */
    template<typename T, typename U>
    void expose_dir_ops(py::class_<T, arma::Base<typename T::elem_type, T>> &py_class) {
        py_class.def("__add__", &add<T, U>, py::is_operator())
                .def("__sub__", &subtract<T, U>, py::is_operator())
                .def("__iadd__", &add<T, U>, py::is_operator())
                .def("__isub__", &subtract<T, U>, py::is_operator())
                .def("__mul__", &multiply<T, U>, py::is_operator())
                .def("__imul__", &multiply<T, U>, py::is_operator())
                .def("__truediv__", &divide<T, U>, py::is_operator())
                .def("__idiv__", &divide<T, U>, py::is_operator())
                .def("__rsub__", &rev_subtract<T, U>, py::is_operator())
                .def("__rmul__", &multiply<T, U>, py::is_operator())
                .def("__radd__", &add<T, U>, py::is_operator());
    }

    // template void expose_dir_ops<arma::diagview<double>, arma::diagview<double>>(py::class_<arma::diagview<double>, arma::Base<double, arma::diagview<double>>> &py_class);
    template void expose_dir_ops<arma::diagview<double>, double>(py::class_<arma::diagview<double>, arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_dir_ops<arma::diagview<double>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::diagview<double>, arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_dir_ops<arma::diagview<double>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::diagview<double>, arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_dir_ops<arma::diagview<float>, arma::diagview<float>>(py::class_<arma::diagview<float>, arma::Base<float, arma::diagview<float>>> &py_class);
    template void expose_dir_ops<arma::diagview<float>, float>(py::class_<arma::diagview<float>, arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_dir_ops<arma::diagview<float>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::diagview<float>, arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_dir_ops<arma::diagview<float>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::diagview<float>, arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::cx_double>, arma::diagview<arma::cx_double>>(py::class_<arma::diagview<arma::cx_double>, arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    template void expose_dir_ops<arma::diagview<arma::cx_double>, arma::cx_double>(py::class_<arma::diagview<arma::cx_double>, arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::cx_double>, arma::subview_elem1<arma::cx_double, arma::umat>>(py::class_<arma::diagview<arma::cx_double>, arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::cx_double>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::class_<arma::diagview<arma::cx_double>, arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::cx_float>, arma::diagview<arma::cx_float>>(py::class_<arma::diagview<arma::cx_float>, arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    template void expose_dir_ops<arma::diagview<arma::cx_float>, arma::cx_float>(py::class_<arma::diagview<arma::cx_float>, arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::cx_float>, arma::subview_elem1<arma::cx_float, arma::umat>>(py::class_<arma::diagview<arma::cx_float>, arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::cx_float>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::class_<arma::diagview<arma::cx_float>, arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::uword>, arma::diagview<arma::uword>>(py::class_<arma::diagview<arma::uword>, arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    template void expose_dir_ops<arma::diagview<arma::uword>, arma::uword>(py::class_<arma::diagview<arma::uword>, arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::uword>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::diagview<arma::uword>, arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::uword>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::diagview<arma::uword>, arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::sword>, arma::diagview<arma::sword>>(py::class_<arma::diagview<arma::sword>, arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    template void expose_dir_ops<arma::diagview<arma::sword>, arma::sword>(py::class_<arma::diagview<arma::sword>, arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::sword>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::diagview<arma::sword>, arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    // template void expose_dir_ops<arma::diagview<arma::sword>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::diagview<arma::sword>, arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);                      

    template void expose_dir_ops<arma::Mat<double>, double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_dir_ops<arma::Mat<float>, float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_dir_ops<arma::Mat<arma::cx_double>, arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_dir_ops<arma::Mat<arma::cx_float>, arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_dir_ops<arma::Mat<arma::uword>, arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_dir_ops<arma::Mat<arma::sword>, arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);

    template void expose_dir_ops<arma::subview<double>, double>(py::class_<arma::subview<double>, arma::Base<double, arma::subview<double>>> &py_class);
    // template void expose_dir_ops<arma::subview<double>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::subview<double>, arma::Base<double, arma::subview<double>>> &py_class);
    // template void expose_dir_ops<arma::subview<double>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::subview<double>, arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_dir_ops<arma::subview<float>, float>(py::class_<arma::subview<float>, arma::Base<float, arma::subview<float>>> &py_class);
    // template void expose_dir_ops<arma::subview<float>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::subview<float>, arma::Base<float, arma::subview<float>>> &py_class);
    // template void expose_dir_ops<arma::subview<float>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::subview<float>, arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_dir_ops<arma::subview<arma::cx_double>, arma::cx_double>(py::class_<arma::subview<arma::cx_double>, arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::cx_double>, arma::subview_elem1<arma::cx_double, arma::umat>>(py::class_<arma::subview<arma::cx_double>, arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::cx_double>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::class_<arma::subview<arma::cx_double>, arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    template void expose_dir_ops<arma::subview<arma::cx_float>, arma::cx_float>(py::class_<arma::subview<arma::cx_float>, arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::cx_float>, arma::subview_elem1<arma::cx_float, arma::umat>>(py::class_<arma::subview<arma::cx_float>, arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::cx_float>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::class_<arma::subview<arma::cx_float>, arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    template void expose_dir_ops<arma::subview<arma::uword>, arma::uword>(py::class_<arma::subview<arma::uword>, arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::uword>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::subview<arma::uword>, arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::uword>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::subview<arma::uword>, arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_dir_ops<arma::subview<arma::sword>, arma::sword>(py::class_<arma::subview<arma::sword>, arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::sword>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::subview<arma::sword>, arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    // template void expose_dir_ops<arma::subview<arma::sword>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::subview<arma::sword>, arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);

    // template void expose_dir_ops<arma::subview_elem1<double, arma::umat>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::subview_elem1<double, arma::umat>, arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<double, arma::umat>, arma::Mat<double>>(py::class_<arma::subview_elem1<double, arma::umat>, arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<double, arma::umat>, arma::subview<double>>(py::class_<arma::subview_elem1<double, arma::umat>, arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<double, arma::umat>, arma::diagview<double>>(py::class_<arma::subview_elem1<double, arma::umat>, arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<double, arma::umat>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::subview_elem1<double, arma::umat>, arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<double, arma::umat>, double>(py::class_<arma::subview_elem1<double, arma::umat>, arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<float, arma::umat>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::subview_elem1<float, arma::umat>, arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<float, arma::umat>, arma::Mat<float>>(py::class_<arma::subview_elem1<float, arma::umat>, arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<float, arma::umat>, arma::subview<float>>(py::class_<arma::subview_elem1<float, arma::umat>, arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<float, arma::umat>, arma::diagview<float>>(py::class_<arma::subview_elem1<float, arma::umat>, arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<float, arma::umat>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::subview_elem1<float, arma::umat>, arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<float, arma::umat>, float>(py::class_<arma::subview_elem1<float, arma::umat>, arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_double, arma::umat>, arma::subview_elem1<arma::cx_double, arma::umat>>(py::class_<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Mat<arma::cx_double>>(py::class_<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_double, arma::umat>, arma::subview<arma::cx_double>>(py::class_<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_double, arma::umat>, arma::diagview<arma::cx_double>>(py::class_<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_double, arma::umat>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::class_<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::cx_double, arma::umat>, arma::cx_double>(py::class_<arma::subview_elem1<arma::cx_double, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_float, arma::umat>, arma::subview_elem1<arma::cx_float, arma::umat>>(py::class_<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Mat<arma::cx_float>>(py::class_<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_float, arma::umat>, arma::subview<arma::cx_float>>(py::class_<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_float, arma::umat>, arma::diagview<arma::cx_float>>(py::class_<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::cx_float, arma::umat>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::class_<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::cx_float, arma::umat>, arma::cx_float>(py::class_<arma::subview_elem1<arma::cx_float, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::uword, arma::umat>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::subview_elem1<arma::uword, arma::umat>, arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::uword, arma::umat>, arma::Mat<arma::uword>>(py::class_<arma::subview_elem1<arma::uword, arma::umat>, arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::uword, arma::umat>, arma::subview<arma::uword>>(py::class_<arma::subview_elem1<arma::uword, arma::umat>, arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::uword, arma::umat>, arma::diagview<arma::uword>>(py::class_<arma::subview_elem1<arma::uword, arma::umat>, arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::uword, arma::umat>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::subview_elem1<arma::uword, arma::umat>, arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::uword, arma::umat>, arma::uword>(py::class_<arma::subview_elem1<arma::uword, arma::umat>, arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::sword, arma::umat>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::subview_elem1<arma::sword, arma::umat>, arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::sword, arma::umat>, arma::Mat<arma::sword>>(py::class_<arma::subview_elem1<arma::sword, arma::umat>, arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::sword, arma::umat>, arma::subview<arma::sword>>(py::class_<arma::subview_elem1<arma::sword, arma::umat>, arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::sword, arma::umat>, arma::diagview<arma::sword>>(py::class_<arma::subview_elem1<arma::sword, arma::umat>, arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem1<arma::sword, arma::umat>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::subview_elem1<arma::sword, arma::umat>, arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem1<arma::sword, arma::umat>, arma::sword>(py::class_<arma::subview_elem1<arma::sword, arma::umat>, arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);

    // template void expose_dir_ops<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Mat<double>>(py::class_<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview<double>>(py::class_<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<double, arma::umat, arma::umat>, arma::diagview<double>>(py::class_<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<double, arma::umat, arma::umat>, double>(py::class_<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Mat<float>>(py::class_<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview<float>>(py::class_<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<float, arma::umat, arma::umat>, arma::diagview<float>>(py::class_<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<float, arma::umat, arma::umat>, float>(py::class_<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::class_<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Mat<arma::cx_double>>(py::class_<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::subview<arma::cx_double>>(py::class_<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::diagview<arma::cx_double>>(py::class_<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::subview_elem1<arma::cx_double, arma::umat>>(py::class_<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::cx_double>(py::class_<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>, arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::class_<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Mat<arma::cx_float>>(py::class_<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::subview<arma::cx_float>>(py::class_<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::diagview<arma::cx_float>>(py::class_<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::subview_elem1<arma::cx_float, arma::umat>>(py::class_<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::cx_float>(py::class_<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>, arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Mat<arma::uword>>(py::class_<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview<arma::uword>>(py::class_<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::diagview<arma::uword>>(py::class_<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::uword>(py::class_<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Mat<arma::sword>>(py::class_<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview<arma::sword>>(py::class_<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::diagview<arma::sword>>(py::class_<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
    // template void expose_dir_ops<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
    template void expose_dir_ops<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::sword>(py::class_<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
}