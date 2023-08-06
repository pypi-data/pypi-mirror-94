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
#include "indexing/cube_row.hpp"
#include "indexing/cube_col.hpp"
#include "indexing/head_tail_slices.hpp"
#include "indexing/slice.hpp"
#include "indexing/non_contiguous/slices.hpp"
#include "indexing/non_contiguous/cube_elem.hpp"
#include "indexing/single_slice.hpp"
#include "indexing/subcube.hpp"
#include "indexing/tube.hpp"
#include "indexing_cube_element.hpp"

namespace py = pybind11;

template <typename... Args>
using overload_cast_ = pybind11::detail::overload_cast_impl<Args...>;

namespace pyarma {
    // Defines Python index operator '[]' overloads for Cubes
    template<typename T>
    void cube_def_get_set(py::class_<T, arma::BaseCube<typename T::elem_type, T>> &py_class) {
        using Matrix = arma::Mat<typename T::elem_type>;
        py_class.def("__getitem__", &cube_get_row<T>, py::keep_alive<0,1>())
                .def("__getitem__", &cube_get_col<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_slice<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_subcube<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_tube<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_tube_size<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_tube_span<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_slices<T>, py::keep_alive<0,1>())
                .def("__getitem__", &cube_get_elem<T>, py::keep_alive<0,1>(), py::keep_alive<0,2>())
                .def("__getitem__", &get_subcube_size<T>, py::keep_alive<0,1>())
                .def("__getitem__", &get_single_slice<T>, py::keep_alive<0,1>())

                // TODO: implement subview_cube_slices
                // It should be implicitly convertible one way, so just worry about getting subview_cube_slices to play
                // nicely with other bits and bobs.
                .def("__getitem__", &get_slices<T>, py::keep_alive<0,1>(), py::keep_alive<0,2>())

                .def("__setitem__", &set_single_slice<T>)

                .def("__setitem__", &cube_set_elem<T>)

                .def("__setitem__", &set_slices<T>)

                .def("__setitem__", &set_subcube_size<T, T>)
                .def("__setitem__", &set_subcube_size<T, Matrix>)

                .def("__setitem__", overload_cast_<T &, std::tuple<arma::uword, py::slice, py::slice>, T>()(cube_set_row<T, T>))
                .def("__setitem__", overload_cast_<T &, std::tuple<arma::uword, py::slice, py::slice>, Matrix>()(cube_set_row<T, Matrix>))

                .def("__setitem__", overload_cast_<T &, std::tuple<py::slice, arma::uword, py::slice>, T>()(cube_set_col<T, T>))
                .def("__setitem__", overload_cast_<T &, std::tuple<py::slice, arma::uword, py::slice>, Matrix>()(cube_set_col<T, Matrix>))

                .def("__setitem__", overload_cast_<T &, std::tuple<py::slice, py::slice, arma::uword>, T>()(set_slice<T, T>))
                .def("__setitem__", overload_cast_<T &, std::tuple<py::slice, py::slice, arma::uword>, Matrix>()(set_slice<T, Matrix>))

                .def("__setitem__", &set_subcube<T, T>)
                .def("__setitem__", &set_subcube<T, Matrix>)

                .def("__setitem__", &set_tube<T, T>)
                .def("__setitem__", &set_tube<T, Matrix>)

                .def("__setitem__", &set_tube_span<T, T>)
                .def("__setitem__", &set_tube_span<T, Matrix>)

                .def("__setitem__", &set_tube_size<T, T>)
                .def("__setitem__", &set_tube_size<T, Matrix>)
                
                .def("__getitem__", &get_head_slices<T>)
                .def("__getitem__", &get_tail_slices<T>)

                .def("__setitem__", &set_head_slices<T>)
                .def("__setitem__", &set_tail_slices<T>);

                expose_cube_element_get_set<typename T::elem_type, T>(py_class);
    }
    
    template void cube_def_get_set<arma::cube>(py::class_<arma::cube, arma::BaseCube<double, arma::cube>> &py_class);
    template void cube_def_get_set<arma::fcube>(py::class_<arma::fcube, arma::BaseCube<float, arma::fcube>> &py_class);
    template void cube_def_get_set<arma::cx_cube>(py::class_<arma::cx_cube, arma::BaseCube<arma::cx_double, arma::cx_cube>> &py_class);
    template void cube_def_get_set<arma::cx_fcube>(py::class_<arma::cx_fcube, arma::BaseCube<arma::cx_float, arma::cx_fcube>> &py_class);
    template void cube_def_get_set<arma::ucube>(py::class_<arma::ucube, arma::BaseCube<arma::uword, arma::ucube>> &py_class);
    template void cube_def_get_set<arma::icube>(py::class_<arma::icube, arma::BaseCube<arma::sword, arma::icube>> &py_class);
}