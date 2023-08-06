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
    void expose_constructor(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        py_class.def(py::init())
                .def(py::init([](const arma::uword in_n_rows, const arma::uword in_n_cols) {
                    return arma::Mat<T>(in_n_rows, in_n_cols, arma::fill::zeros);
                }))
                .def(py::init<arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_none>>())
                .def(py::init<arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_ones>>())
                .def(py::init<arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_zeros>>())
                .def(py::init<arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_eye>>())
                .def(py::init<arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_randu>>())
                .def(py::init<arma::uword, arma::uword, arma::fill::fill_class<arma::fill::fill_randn>>())
                .def(py::init([](arma::SizeMat &s) {
                    return arma::Mat<T>(s.n_rows, s.n_cols, arma::fill::zeros);
                }))
                .def(py::init<arma::SizeMat, arma::fill::fill_class<arma::fill::fill_none>>())
                .def(py::init<arma::SizeMat, arma::fill::fill_class<arma::fill::fill_ones>>())
                .def(py::init<arma::SizeMat, arma::fill::fill_class<arma::fill::fill_zeros>>())
                .def(py::init<arma::SizeMat, arma::fill::fill_class<arma::fill::fill_eye>>())
                .def(py::init<arma::SizeMat, arma::fill::fill_class<arma::fill::fill_randu>>())
                .def(py::init<arma::SizeMat, arma::fill::fill_class<arma::fill::fill_randn>>())
                .def(py::init<arma::subview<T> &>())
                .def(py::init<arma::diagview<T> &>())
                .def(py::init<arma::subview_elem1<T, arma::umat> &>())
                .def(py::init<arma::subview_elem2<T, arma::umat, arma::umat> &>())
                .def(py::init([](arma::mat &matrix) {
                    return arma::conv_to<arma::Mat<T>>::from(matrix);
                }))
                .def(py::init([](arma::fmat &matrix) {
                    return arma::conv_to<arma::Mat<T>>::from(matrix);
                }))
                .def(py::init([](arma::cx_mat &matrix) {
                    return arma::conv_to<arma::Mat<T>>::from(matrix);
                }))
                .def(py::init([](arma::cx_fmat &matrix) {
                    return arma::conv_to<arma::Mat<T>>::from(matrix);
                }))
                .def(py::init([](arma::umat &matrix) {
                    return arma::conv_to<arma::Mat<T>>::from(matrix);
                }))
                .def(py::init([](arma::imat &matrix) {
                    return arma::conv_to<arma::Mat<T>>::from(matrix);
                }))
                .def(py::init<std::string &>())
                // TODO: See if having pybind11 convert this is less efficient than taking Python lists straight
                .def(py::init([](std::vector<T> &list) {
                    // get the number of elements, initialise a matrix with the same number of elements
                    arma::Mat<T> output(1, list.size());
                    // for each element, set the matrix's element to that
                    arma::uword index = 0;
                    for (T element : list) {
                        output[index] = element;
                        ++index;
                    }
                    // return
                    return output;
                }))
                // List of list constructor
                .def(py::init([](std::vector<std::vector<T>> &list) {
                    arma::uword x_n_rows = arma::uword(list.size());
                    arma::uword x_n_cols = 0;
                    
                    auto it     = list.begin();
                    auto it_end = list.end();
                    
                    for (; it != it_end; ++it) {
                        x_n_cols = (std::max)(x_n_cols, arma::uword((*it).size()));
                    }

                    arma::Mat<T> output(x_n_rows, x_n_cols, arma::fill::zeros);
                    
                    arma::uword row_num = 0;
                    
                    auto row_it     = list.begin();
                    auto row_it_end = list.end();
                    
                    for (; row_it != row_it_end; ++row_it) {
                        arma::uword col_num = 0;
                        
                        auto col_it     = (*row_it).begin();
                        auto col_it_end = (*row_it).end();
                        
                        for (; col_it != col_it_end; ++col_it) {
                            output.at(row_num, col_num) = (*col_it);
                            ++col_num;
                        }
                        
                        ++row_num;
                    }

                    return output;
                }))
                // #ifndef PYARMA_NO_NUMPY
                .def(py::init([](py::buffer b) {
                    py::buffer_info info = b.request();

                    if (info.format != py::format_descriptor<T>::format()) {
                        throw std::runtime_error("Incompatible format: expected a " + py::format_descriptor<T>::format() + " array!");
                    }

                    if (info.ndim != 2) {
                        throw std::runtime_error("Incompatible buffer dimension!");
                    }

                    return arma::Mat<T>(static_cast<T*>(info.ptr), info.shape[0], info.shape[1]);
                }))
                // #endif
                ;
    }

    template void expose_constructor<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_constructor<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_constructor<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_constructor<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_constructor<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_constructor<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}
