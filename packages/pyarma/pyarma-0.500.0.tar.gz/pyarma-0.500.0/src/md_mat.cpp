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
#include "indexing/submatrix_size.hpp"
#include "indexing_get_non_contiguous.hpp"
#include "indexing_set_non_contiguous.hpp"
#include "iterator.hpp"
#include "methods/md_set.hpp"
#include "methods/md_rand_set.hpp"
#include "methods/md_functor.hpp"
#include "methods/md_size.hpp"
#include "methods/md_rows_cols.hpp"
#include "methods/md_load.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose matrix methods
    template<typename T>
    void expose_matrix_methods(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        using Class = arma::Mat<T>;
        
        expose_get_non_contiguous<T>(py_class);
        expose_set_non_contiguous<T>(py_class);
        expose_iter<T>(py_class);
        expose_set<T>(py_class);
        expose_rand_set<T>(py_class);
        expose_functor<T>(py_class);
        expose_size_md<T>(py_class);
        expose_rows_cols<T>(py_class);
        expose_load<T>(py_class);

        // Expose methods, starting with a buffer protocol definition
        py_class.def_buffer([](Class &matrix) -> py::buffer_info {
            return py::buffer_info(
                matrix.memptr(),
                sizeof(T),
                py::format_descriptor<T>::format(),
                2,
                std::vector<py::ssize_t>{ py::ssize_t(matrix.n_rows), py::ssize_t(matrix.n_cols) },
                std::vector<py::ssize_t>{ sizeof(T),
                  py::ssize_t(sizeof(T)) * py::ssize_t(matrix.n_rows) }
            );
        })
            // Get/set submatrices using size(X) (only for matrices, not for subviews/diagviews)
            .def("__getitem__", &get_submatrix_size<Class>, py::keep_alive<0,1>())
            .def("__setitem__", &set_submatrix_size<Class, Class>)
            // .def("__setitem__", &set_submatrix_size<Class, T>)

            .def("clean", [](Class &matrix, double value) { matrix.clean(value); })

            // Same caveat: same types only. Can be fixed by manually listing the allowed objects
            // Ccurrently may allow via implicit conversion.
            .def("swap", [](Class &matrix, Class &swap_with) { matrix.swap(swap_with); });
    }

    template void expose_matrix_methods<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_matrix_methods<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_matrix_methods<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_matrix_methods<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_matrix_methods<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_matrix_methods<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}