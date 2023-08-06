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
    // Expose element setting methods (i.e. zeros())
    template<typename T>
    void expose_set(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        using Class = arma::Mat<T>;
        py_class.def("set_imag", [](Class &matrix, arma::Mat<typename arma::get_pod_type<T>::result> set_to) { matrix.set_imag(set_to); })
            .def("set_real", [](Class &matrix, arma::Mat<typename arma::get_pod_type<T>::result> set_to) { matrix.set_real(set_to); })
            
            .def("zeros", [](Class &matrix) { matrix.zeros(); })
            .def("zeros", [](Class &matrix, const arma::uword &n_rows, const arma::uword &n_cols) { matrix.zeros(n_rows, n_cols); })
            .def("zeros", [](Class &matrix, arma::SizeMat &size) { matrix.zeros(size); })

            .def("ones", [](Class &matrix) { matrix.ones(); })
            .def("ones", [](Class &matrix, const arma::uword &n_rows, const arma::uword &n_cols) { matrix.ones(n_rows, n_cols); })
            .def("ones", [](Class &matrix, arma::SizeMat &size) { matrix.ones(size); })

            .def("eye", [](Class &matrix) { matrix.eye(); })
            .def("eye", [](Class &matrix, const arma::uword &n_rows, const arma::uword &n_cols) { matrix.eye(n_rows, n_cols); })
            .def("eye", [](Class &matrix, arma::SizeMat &size) { matrix.eye(size); });
    }

    template void expose_set<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_set<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_set<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_set<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_set<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_set<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}