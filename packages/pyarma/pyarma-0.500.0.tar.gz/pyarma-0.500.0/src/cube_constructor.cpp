// Copyright 2020-2021 Jason Rumengan, Terry Yue Zhuo
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
#include "pybind11/stl.h"
#include "pybind11/complex.h"
// #ifndef PYARMA_NO_NUMPY
// #include "pybind11/numpy.h"
// #endif
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose constructors
    template<typename T>
    void cube_expose_constructor(py::class_<arma::Cube<T>, arma::BaseCube<T, arma::Cube<T>>> & py_class) {
        py_class.def(py::init())
                .def(py::init([](const arma::uword in_n_rows, const arma::uword in_n_cols, const arma::uword in_n_slices) {
                    return arma::Cube<T>(in_n_rows, in_n_cols, in_n_slices, arma::fill::zeros);
                }))
                .def(py::init<arma::uword, arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_none>>())
                .def(py::init<arma::uword, arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_ones>>())
                .def(py::init<arma::uword, arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_zeros>>())
                .def(py::init<arma::uword, arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_randu>>())
                .def(py::init<arma::uword, arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_randn>>())
                .def(py::init<arma::subview_cube<T> &>())
                .def(py::init([](arma::SizeCube &s) {
                    return arma::Cube<T>(s.n_rows, s.n_cols, s.n_slices, arma::fill::zeros);
                }))
                .def(py::init<arma::SizeCube, arma::fill::fill_class<arma::fill::fill_none>>())
                .def(py::init<arma::SizeCube, arma::fill::fill_class<arma::fill::fill_ones>>())
                .def(py::init<arma::SizeCube, arma::fill::fill_class<arma::fill::fill_zeros>>())
                .def(py::init<arma::SizeCube, arma::fill::fill_class<arma::fill::fill_randu>>())
                .def(py::init<arma::SizeCube, arma::fill::fill_class<arma::fill::fill_randn>>())
                .def(py::init([](arma::cube &matrix) {
                    return arma::conv_to<arma::Cube<T>>::from(matrix);
                }))
                .def(py::init([](arma::fcube &matrix) {
                    return arma::conv_to<arma::Cube<T>>::from(matrix);
                }))
                .def(py::init([](arma::cx_cube &matrix) {
                    return arma::conv_to<arma::Cube<T>>::from(matrix);
                }))
                .def(py::init([](arma::cx_fcube &matrix) {
                    return arma::conv_to<arma::Cube<T>>::from(matrix);
                }))
                .def(py::init([](arma::ucube &matrix) {
                    return arma::conv_to<arma::Cube<T>>::from(matrix);
                }))
                .def(py::init([](arma::icube &matrix) {
                    return arma::conv_to<arma::Cube<T>>::from(matrix);
                }))
                .def(py::init([](std::vector<std::vector<std::vector<T>>> &list) {
                arma::uword x_n_slices = arma::uword(list.size());
                arma::uword x_n_rows = 0;
                arma::uword x_n_cols = 0;

                auto it    = list.begin();
                auto it_end = list.end();
                
                for (; it != it_end; ++it) {
                    x_n_rows = (std::max)(x_n_rows, arma::uword((*it).size()));

                    auto itt    = (*it).begin();
                    auto itt_end = (*it).end();

                    for (; itt != itt_end; ++itt) {
                        x_n_cols = (std::max)(x_n_cols, arma::uword((*itt).size()));
                    }
                }

                arma::Cube<T> output(x_n_rows, x_n_cols, x_n_slices, arma::fill::zeros);
                
                arma::uword slice_num = 0;
                
                auto slice_it     = list.begin();
                auto slice_it_end = list.end();

                for (; slice_it != slice_it_end; ++slice_it) {
                    arma::uword row_num = 0;
                    
                    auto row_it     = (*slice_it).begin();
                    auto row_it_end = (*slice_it).end();
                    
                    for (; row_it != row_it_end; ++row_it) {
                        arma::uword col_num = 0;
                        
                        auto col_it     = (*row_it).begin();
                        auto col_it_end = (*row_it).end();
                        
                        for (; col_it != col_it_end; ++col_it) {
                            output.at(row_num, col_num, slice_num) = (*col_it);
                            ++col_num;
                        }
                        
                        ++row_num;
                    }

                    ++slice_num;
                }

                return output;
                }))
                // #ifndef PYARMA_NO_NUMPY
                .def(py::init([](py::buffer b) {
                    py::buffer_info info = b.request();

                    if (info.format != py::format_descriptor<T>::format()) {
                        throw std::runtime_error("Incompatible format: expected a " + py::format_descriptor<T>::format() + " array!");
                    }

                    if (info.ndim != 3) {
                        throw std::runtime_error("Incompatible buffer dimension!");
                    }

                    return arma::Cube<T>(static_cast<T*>(info.ptr), info.shape[1], info.shape[2], info.shape[0]);
                }))
                // #endif
                ;
    }

    template void cube_expose_constructor<double>(py::class_<arma::Cube<double>, arma::BaseCube<double, arma::Cube<double>>> &py_class);
    template void cube_expose_constructor<float>(py::class_<arma::Cube<float>, arma::BaseCube<float, arma::Cube<float>>> &py_class);
    template void cube_expose_constructor<arma::cx_double>(py::class_<arma::Cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> &py_class);
    template void cube_expose_constructor<arma::cx_float>(py::class_<arma::Cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> &py_class);
    template void cube_expose_constructor<arma::uword>(py::class_<arma::Cube<arma::uword>, arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> &py_class);
    template void cube_expose_constructor<arma::sword>(py::class_<arma::Cube<arma::sword>, arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> &py_class);
}