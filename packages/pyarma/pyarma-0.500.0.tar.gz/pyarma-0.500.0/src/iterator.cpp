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

#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Exposes iterators
    template<typename T>
    void expose_iter(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        using Class = arma::Mat<T>;

        // Expose overload to Python's iter() function and iterators
        py_class.def("__iter__", [](const Class &matrix) { return py::make_iterator(matrix.begin(), matrix.end()); }, py::keep_alive<0, 1>());
    }

    template void expose_iter<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_iter<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_iter<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_iter<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_iter<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_iter<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}
