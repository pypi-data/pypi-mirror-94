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

#define ARMA_DONT_PRINT_ERRORS
#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "methods/md_load_cube.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose cube methods
    template<typename T>
    void expose_cube_methods(py::class_<arma::Cube<T>, arma::BaseCube<T, arma::Cube<T>>> &py_class) {
        using Class = arma::Cube<T>;
        expose_load_cube<T>(py_class);

        py_class.def_buffer([](Class &cube) -> py::buffer_info {
            return py::buffer_info(
                cube.memptr(),
                sizeof(T),
                py::format_descriptor<T>::format(),
                3,
                std::vector<py::ssize_t>{
                    py::ssize_t(cube.n_slices),
                    py::ssize_t(cube.n_rows),
                    py::ssize_t(cube.n_cols) },
                std::vector<py::ssize_t>{ 
                    py::ssize_t(sizeof(T) * py::ssize_t(cube.n_rows) * py::ssize_t(cube.n_cols)),
                    sizeof(T),
                    py::ssize_t(sizeof(T) * py::ssize_t(cube.n_rows)) }
            );
        })
        
            .def("set_imag", [](Class &cube, arma::Cube<typename arma::get_pod_type<T>::result> set_to) { cube.set_imag(set_to); })
            .def("set_real", [](Class &cube, arma::Cube<typename arma::get_pod_type<T>::result> set_to) { cube.set_real(set_to); })
            .def("__iter__", [](Class &cube) { return py::make_iterator(cube.begin(), cube.end()); }, py::keep_alive<0, 1>())
            
            .def("zeros", [](Class &cube) { cube.zeros(); })
            .def("zeros", [](Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { cube.zeros(n_rows, n_cols, n_slices); })
            .def("zeros", [](Class &cube, arma::SizeCube &size) { cube.zeros(size); })

            .def("ones", [](Class &cube) { cube.ones(); })
            .def("ones", [](Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { cube.ones(n_rows, n_cols, n_slices); })
            .def("ones", [](Class &cube, arma::SizeCube &size) { cube.ones(size); })

            .def("randu", [](Class &cube) { cube.randu(); })
            .def("randu", [](Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { cube.randu(n_rows, n_cols, n_slices); })
            .def("randu", [](Class &cube, arma::SizeCube &size) { cube.randu(size); })

            .def("randn", [](Class &cube) { cube.randn(); })
            .def("randn", [](Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { cube.randn(n_rows, n_cols, n_slices); })
            .def("randn", [](Class &cube, arma::SizeCube &size) { cube.randn(size); })

            .def("clean", [](Class &cube, double value) { cube.clean(value); })

            .def("set_size", [](Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { cube.set_size(n_rows, n_cols, n_slices); })
            .def("set_size", [](Class &cube, arma::SizeCube &size) { cube.set_size(size); })

            .def("reshape" , [](Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { cube.reshape(n_rows, n_cols, n_slices); })
            .def("reshape" , [](Class &cube, arma::SizeCube &size) { cube.reshape(size); })

            .def("resize", [](Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { cube.resize(n_rows, n_cols, n_slices); })
            .def("resize", [](Class &cube, arma::SizeCube &size) { cube.resize(size); })

            .def("copy_size", [](Class &cube, arma::Cube<double> &copy_from) { cube.copy_size(copy_from); })
            .def("copy_size", [](Class &cube, arma::Cube<float> &copy_from) { cube.copy_size(copy_from); })
            .def("copy_size", [](Class &cube, arma::Cube<arma::cx_double> &copy_from) { cube.copy_size(copy_from); })
            .def("copy_size", [](Class &cube, arma::Cube<arma::cx_float> &copy_from) { cube.copy_size(copy_from); })
            .def("copy_size", [](Class &cube, arma::Cube<arma::uword> &copy_from) { cube.copy_size(copy_from); })
            .def("copy_size", [](Class &cube, arma::Cube<arma::sword> &copy_from) { cube.copy_size(copy_from); })

            .def("reset", [](Class &cube) { cube.reset(); })
            .def("insert_rows", [](Class &cube, arma::uword row_num, Class &insert) {
                cube.insert_rows(row_num, insert);
            })
            .def("insert_rows", [](Class &cube, arma::uword row_num, arma::uword num_rows, bool cube_set_to_zero = true) {
                cube.insert_rows(row_num, num_rows, cube_set_to_zero);
            }, "row_num"_a, "num_rows"_a, "cube_set_to_zero"_a = true)
            .def("insert_cols", [](Class &cube, arma::uword col_num, Class &insert) {
                cube.insert_cols(col_num, insert);
            })
            .def("insert_cols", [](Class &cube, arma::uword col_num, arma::uword num_cols, bool cube_set_to_zero = true) {
                cube.insert_cols(col_num, num_cols, cube_set_to_zero);
            }, "col_num"_a, "num_cols"_a, "cube_set_to_zero"_a = true)
            .def("insert_slices", [](Class &cube, arma::uword slice_num, arma::uword num_slices, bool cube_set_to_zero = true) {
                cube.insert_slices(slice_num, num_slices, cube_set_to_zero);
            }, "slice_num"_a, "num_slices"_a, "cube_set_to_zero"_a = true)
                        .def("insert_slices", [](Class &cube, arma::uword slice_num, Class &insert) {
                cube.insert_slices(slice_num, insert);
            })
            .def("insert_slices", [](Class &cube, arma::uword slice_num, arma::uword num_slices, bool cube_set_to_zero = true) {
                cube.insert_slices(slice_num, num_slices, cube_set_to_zero);
            }, "slice_num"_a, "num_slices"_a, "cube_set_to_zero"_a = true)
            .def("shed_row", [](Class &cube, arma::uword row_num) { cube.shed_row(row_num); })
            .def("shed_rows", [](Class &cube, arma::uword first_row, arma::uword last_row) { cube.shed_rows(first_row, last_row); })
            .def("shed_col", [](Class &cube, arma::uword col_num) { cube.shed_col(col_num); })
            .def("shed_cols", [](Class &cube, arma::uword first_col, arma::uword last_col) { cube.shed_cols(first_col, last_col); })
            .def("shed_slice", [](Class &cube, arma::uword slice_num) { cube.shed_slice(slice_num); })
            .def("shed_slices", [](Class &cube, arma::uword first_slice, arma::uword last_slice) { cube.shed_slices(first_slice, last_slice); })
            .def("shed_slices", [](Class &cube, arma::Mat<arma::uword> indices) { cube.shed_slices(indices); })          
            // Same caveat: same types only. Can be fixed by manually listing the allowed objects
            .def("swap", [](Class &cube, Class &swap_with) { cube.swap(swap_with); });
    }

    template void expose_cube_methods<double>(py::class_<arma::Cube<double>, arma::BaseCube<double, arma::Cube<double>>> &py_class);
    template void expose_cube_methods<float>(py::class_<arma::Cube<float>, arma::BaseCube<float, arma::Cube<float>>> &py_class);
    template void expose_cube_methods<arma::cx_double>(py::class_<arma::Cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> &py_class);
    template void expose_cube_methods<arma::cx_float>(py::class_<arma::Cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> &py_class);
    template void expose_cube_methods<arma::uword>(py::class_<arma::Cube<arma::uword>, arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> &py_class);
    template void expose_cube_methods<arma::sword>(py::class_<arma::Cube<arma::sword>, arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> &py_class);
}