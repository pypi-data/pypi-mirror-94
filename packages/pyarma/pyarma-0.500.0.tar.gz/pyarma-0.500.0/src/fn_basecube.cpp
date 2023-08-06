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
using namespace pybind11::literals;

namespace pyarma {
    // Expose base cube standalone functions
    template<typename T, typename Derived>
    void expose_base_cube_functions(py::module &m) {

        m.def("imag", [](const Derived &cube) { return imag(cube).eval(); })
        .def("real", [](const Derived &cube) { return real(cube).eval(); })

        // standalone (index_)min/max
        .def("min", [](const arma::Cube<T> &cube) {
            arma::Cube<T> output;

            if (cube.n_elem == 0) {
                output = cube;
            } else if (cube.n_slices == cube.n_elem) {
                output = min(cube, 2);
            } else if (cube.n_rows == 1) {
                output = min(cube, 1);
            } else {
                output = min(cube, 0);
            }
            return output;
        }, "cube"_a)
        .def("min", [](const arma::Cube<T> &cube, arma::uword dim) {
            return min(cube, dim).eval();
        }, "cube"_a, "dim"_a) 
        .def("min", [](const arma::Cube<T> &a, const arma::Cube<T> &b) {
            return arma::min(a, b).eval();
        })
        .def("max", [](const arma::Cube<T> &cube) {
            arma::Cube<T> output;

            if (cube.n_elem == 0) {
                output = cube;
            } else if (cube.n_slices == cube.n_elem) {
                output = max(cube, 2);
            } else if (cube.n_rows == 1) {
                output = max(cube, 1);
            } else {
                output = max(cube, 0);
            }
            return output;
        }, "cube"_a)
        .def("max", [](const arma::Cube<T> &cube, arma::uword dim) {
            return max(cube, dim).eval();
        }, "cube"_a, "dim"_a)
        .def("max", [](const arma::Cube<T> &a, const arma::Cube<T> &b) {
            return arma::max(a, b).eval();
        })
        .def("index_min", [](const arma::Cube<T> &cube) {
            arma::ucube output;

            if (cube.n_slices == cube.n_elem) {
                output = index_min(cube, 2);
            } else if (cube.n_rows == 1) {
                output = index_min(cube, 1);
            } else {
                output = index_min(cube, 0);
            }
            return output;
        }, "cube"_a)
        .def("index_min", [](const arma::Cube<T> &cube, arma::uword dim) {
            return index_min(cube, dim).eval();
        })
        .def("index_max", [](const arma::Cube<T> &cube) {
            arma::ucube output;

            if (cube.n_slices == cube.n_elem) {
                output = index_max(cube, 2);
            } else if (cube.n_rows == 1) {
                output = index_max(cube, 1);
            } else {
                output = index_max(cube, 0);
            }
            return output;
        }, "cube"_a)
        .def("index_max", [](const arma::Cube<T> &cube, arma::uword dim) {
            return index_max(cube, dim).eval();
        });
    }

    template void expose_base_cube_functions<double, arma::Cube<double>>(py::module &m);
    template void expose_base_cube_functions<double, arma::subview_cube<double>>(py::module &m);

    template void expose_base_cube_functions<float, arma::Cube<float>>(py::module &m);
    template void expose_base_cube_functions<float, arma::subview_cube<float>>(py::module &m);

    template void expose_base_cube_functions<arma::cx_double, arma::Cube<arma::cx_double>>(py::module &m);
    template void expose_base_cube_functions<arma::cx_double, arma::subview_cube<arma::cx_double>>(py::module &m);

    template void expose_base_cube_functions<arma::cx_float, arma::Cube<arma::cx_float>>(py::module &m);
    template void expose_base_cube_functions<arma::cx_float, arma::subview_cube<arma::cx_float>>(py::module &m);

    template void expose_base_cube_functions<arma::uword, arma::Cube<arma::uword>>(py::module &m);
    template void expose_base_cube_functions<arma::uword, arma::subview_cube<arma::uword>>(py::module &m);

    template void expose_base_cube_functions<arma::sword, arma::Cube<arma::sword>>(py::module &m);
    template void expose_base_cube_functions<arma::sword, arma::subview_cube<arma::sword>>(py::module &m);
}