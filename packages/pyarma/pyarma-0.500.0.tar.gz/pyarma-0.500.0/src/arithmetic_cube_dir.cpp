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

// // #include "force_inst_cube.hpp"
#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "arithmetic/add/add_cube_dir.hpp"
#include "arithmetic/multiply/multiply_cube_dir.hpp"
#include "arithmetic/subtract/subtract_cube_dir.hpp"
#include "arithmetic/subtract/subtract_cube_dir_rev.hpp"
#include "arithmetic/divide/divide_cube_dir.hpp"

namespace py = pybind11;

namespace pyarma {     
    template<typename T, typename U>
    void cube_def_dir_ops(py::class_<T, arma::BaseCube<typename T::elem_type, T>> &py_class) {
        py_class.def("__add__", &cube_add<T, U>, py::is_operator())
                .def("__sub__", &cube_subtract<T, U>, py::is_operator())
                .def("__iadd__", &cube_add<T, U>, py::is_operator())
                .def("__isub__", &cube_subtract<T, U>, py::is_operator())
                .def("__mul__", &cube_multiply<T, U>, py::is_operator())
                .def("__imul__", &cube_multiply<T, U>, py::is_operator())
                .def("__truediv__", &cube_divide<T, U>, py::is_operator())
                .def("__idiv__", &cube_divide<T, U>, py::is_operator())
                .def("__rsub__", &cube_rev_subtract<T, U>, py::is_operator())        
                .def("__rmul__", &cube_multiply<T, U>, py::is_operator())
                .def("__radd__", &cube_add<T, U>, py::is_operator());
    }

    template void cube_def_dir_ops<arma::Cube<double>, double>(py::class_<arma::Cube<double>, arma::BaseCube<double, arma::Cube<double>>> &py_class);
    template void cube_def_dir_ops<arma::subview_cube<double>, double>(py::class_<arma::subview_cube<double>, arma::BaseCube<double, arma::subview_cube<double>>> &py_class);

    template void cube_def_dir_ops<arma::Cube<float>, float>(py::class_<arma::Cube<float>, arma::BaseCube<float, arma::Cube<float>>> &py_class);
    template void cube_def_dir_ops<arma::subview_cube<float>, float>(py::class_<arma::subview_cube<float>, arma::BaseCube<float, arma::subview_cube<float>>> &py_class);

    template void cube_def_dir_ops<arma::Cube<arma::cx_double>, arma::cx_double>(py::class_<arma::Cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> &py_class);
    template void cube_def_dir_ops<arma::subview_cube<arma::cx_double>, arma::cx_double>(py::class_<arma::subview_cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::subview_cube<arma::cx_double>>> &py_class);

    template void cube_def_dir_ops<arma::Cube<arma::cx_float>, arma::cx_float>(py::class_<arma::Cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> &py_class);
    template void cube_def_dir_ops<arma::subview_cube<arma::cx_float>, arma::cx_float>(py::class_<arma::subview_cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::subview_cube<arma::cx_float>>> &py_class);

    template void cube_def_dir_ops<arma::Cube<arma::uword>, arma::uword>(py::class_<arma::Cube<arma::uword>, arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> &py_class);
    template void cube_def_dir_ops<arma::subview_cube<arma::uword>, arma::uword>(py::class_<arma::subview_cube<arma::uword>, arma::BaseCube<arma::uword, arma::subview_cube<arma::uword>>> &py_class);

    template void cube_def_dir_ops<arma::Cube<arma::sword>, arma::sword>(py::class_<arma::Cube<arma::sword>, arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> &py_class);
    template void cube_def_dir_ops<arma::subview_cube<arma::sword>, arma::sword>(py::class_<arma::subview_cube<arma::sword>, arma::BaseCube<arma::sword, arma::subview_cube<arma::sword>>> &py_class);
}