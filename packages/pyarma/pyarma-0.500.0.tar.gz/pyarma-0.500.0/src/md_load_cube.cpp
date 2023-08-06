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
#include "pybind11/iostream.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose loading
    template<typename T>
    void expose_load_cube(py::class_<arma::Cube<T>, arma::BaseCube<T, arma::Cube<T>>> &py_class) {
        using Class = arma::Cube<T>;
        py_class.def("load", [](Class &cube, const std::string &filename, const arma::file_type &file_type = arma::auto_detect) {
                return cube.load(filename.c_str(), file_type);
            }, "filename"_a, "file_type"_a = arma::auto_detect, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>());
    }

    template void expose_load_cube<double>(py::class_<arma::Cube<double>, arma::BaseCube<double, arma::Cube<double>>> &py_class);
    template void expose_load_cube<float>(py::class_<arma::Cube<float>, arma::BaseCube<float, arma::Cube<float>>> &py_class);
    template void expose_load_cube<arma::cx_double>(py::class_<arma::Cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> &py_class);
    template void expose_load_cube<arma::cx_float>(py::class_<arma::Cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> &py_class);
    template void expose_load_cube<arma::uword>(py::class_<arma::Cube<arma::uword>, arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> &py_class);
    template void expose_load_cube<arma::sword>(py::class_<arma::Cube<arma::sword>, arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> &py_class);
}