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
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose size setting methods (i.e. reset())
    template<typename T>
    void expose_size_md(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        using Class = arma::Mat<T>;
        py_class.def("reshape" , [](Class &matrix, const arma::uword &n_rows, const arma::uword &n_cols) { matrix.reshape(n_rows, n_cols); })
            .def("reshape" , [](Class &matrix, arma::SizeMat &size) { matrix.reshape(size); })

            .def("resize", [](Class &matrix, const arma::uword &n_rows, const arma::uword &n_cols) { matrix.resize(n_rows, n_cols); })
            .def("resize", [](Class &matrix, arma::SizeMat &size) { matrix.resize(size); })
            
            .def("reset", [](Class &matrix) { matrix.reset(); })
            
            .def("set_size", [](Class &matrix, const arma::uword &n_rows, const arma::uword &n_cols) { matrix.set_size(n_rows, n_cols); })
            .def("set_size", [](Class &matrix, arma::SizeMat &size) { matrix.set_size(size); })

            .def("copy_size", [](Class &matrix, const arma::Mat<double> &copy_from) { matrix.copy_size(copy_from); })
            .def("copy_size", [](Class &matrix, const arma::Mat<float> &copy_from) { matrix.copy_size(copy_from); })
            .def("copy_size", [](Class &matrix, const arma::Mat<arma::cx_double> &copy_from) { matrix.copy_size(copy_from); })
            .def("copy_size", [](Class &matrix, const arma::Mat<arma::cx_float> &copy_from) { matrix.copy_size(copy_from); })
            .def("copy_size", [](Class &matrix, const arma::Mat<arma::uword> &copy_from) { matrix.copy_size(copy_from); })
            .def("copy_size", [](Class &matrix, const arma::Mat<arma::sword> &copy_from) { matrix.copy_size(copy_from); });
    }

    template void expose_size_md<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_size_md<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_size_md<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_size_md<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_size_md<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_size_md<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}