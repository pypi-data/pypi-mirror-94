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
#include "pybind11/operators.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    arma_cold void define_size(py::module &m) {
        using Class = arma::SizeCube;

        py::class_<Class>(m, "__size_cube")
            .def(py::self + py::self)
            .def(py::self - py::self)
            .def(py::self + arma::uword())
            .def(py::self - arma::uword())
            .def(py::self * arma::uword())
            .def(py::self / arma::uword())
            .def(py::self == py::self)
            .def(py::self != py::self)
            .def("__repr__", [](const Class &size) {
                std::ostringstream stream;
                stream << size;
                return stream.str();
            })
            .def("__getitem__", [](const Class &size, const arma::uword &index) { return size(index); });
    }
}
