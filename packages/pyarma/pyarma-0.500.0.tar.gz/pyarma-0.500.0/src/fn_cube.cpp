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
#include "pybind11/complex.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose cube standalone functions
    template<typename T>
    void expose_cube_functions(py::module &m) {
        using Class = arma::Cube<T>;
        m.def("sum", [](const Class &cube) { 
            Class output;
            if (cube.n_elem == 0) {
                output.set_size(1,1,1);
                output[0] = T(0);
            } else if (cube.n_slices == cube.n_elem) {
                output = arma::sum(cube, 2);
            } else if (cube.n_rows == 1) {
                output = arma::sum(cube, 1);
            } else {
                output = arma::sum(cube, 0);
            }
            return output;
         }, "cube"_a)
         .def("sum", [](const Class &cube, arma::uword dim) { 
            return arma::sum(cube, dim).eval(); 
         }, "cube"_a, "dim"_a)
        .def("abs", [](const Class &cube) { return abs(cube).eval(); })
        .def("accu", [](const Class &cube) { return arma::accu(cube); })
        .def("approx_equal", [](const Class &a, const Class &b, std::string method, double tol) {
            return approx_equal(a, b, method.c_str(), tol);
        })
        .def("approx_equal", [](const Class &a, const Class &b, std::string method, double abstol, double reltol) {
            return approx_equal(a, b, method.c_str(), abstol, reltol);
        })
        .def("arg", [](const Class &cube) { return arg(cube).eval(); })
        .def("as_scalar", [](const Class &cube) { return as_scalar(cube); })
        .def("find", [](const Class &cube, arma::uword k = 0, std::string s = "first") { return find(cube, k, s.c_str()).eval(); }, "cube"_a, "k"_a = 0, "s"_a = "first")
        .def("find_finite", [](const Class &cube) { return find_finite(cube).eval(); })
        .def("find_nonfinite", [](const Class &cube) { return find_nonfinite(cube).eval(); })
        .def("find_unique", [](const Class &cube, bool ascending_indices = true) {
            return find_unique(cube, ascending_indices).eval();
        }, "cube"_a, "ascending_indices"_a = true)
        .def("ind2sub", [](const arma::SizeCube &size, arma::uword index) { return arma::umat(ind2sub(size, index)); })
        .def("ind2sub", [](const arma::SizeCube &size, arma::umat indices) { return ind2sub(size, indices); })
        
        .def("reshape", [](const Class &cube, arma::SizeCube &size) { return reshape(cube, size).eval(); })
        .def("reshape", [](const Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { return reshape(cube, n_rows, n_cols, n_slices).eval(); })

        .def("resize", [](const Class &cube, arma::SizeCube &size) { return resize(cube, size).eval(); })
        .def("resize", [](const Class &cube, arma::uword n_rows, arma::uword n_cols, arma::uword n_slices) { return resize(cube, n_rows, n_cols, n_slices).eval(); })

        .def("size", [](const Class &cube) { return arma::size(cube); })
        .def("size", [](const arma::uword rows, const arma::uword cols, const arma::uword slices) { return arma::size(rows, cols, slices); })
        
        .def("sub2ind", [](const arma::SizeCube &size, arma::uword row, arma::uword col, arma::uword slice) { return sub2ind(size, row, col, slice); })
        .def("sub2ind", [](const arma::SizeCube &size, arma::umat indices) { return arma::umat(sub2ind(size, indices)); })

        .def("vectorise", [](const Class &cube) { return vectorise(cube).eval(); })

        .def("iterator", [](const Class &cube, const arma::uword begin_elem = 0, const arma::sword end_elem = -1) {
            arma::uword true_end_elem;
            // If the user does not specify an ending index, use the last element
            if (end_elem == -1) { 
                true_end_elem = cube.n_elem - 1; 
            } else {
                true_end_elem = arma::uword(end_elem);
            }
            if (begin_elem >= cube.n_elem) {
                throw py::value_error("Starting element cannot be greater than or equal to the number of elements");
            }
            if (true_end_elem >= cube.n_elem) {
                throw py::value_error("Ending element cannot be greater than or equal to the number of elements");
            }
            return py::make_iterator(cube.begin()+begin_elem, cube.begin()+true_end_elem+1);
        }, "cube"_a, "begin_elem"_a = 0, "end_elem"_a = -1, py::keep_alive<0,1>())
        .def("slice_iter", [](const Class &cube, const arma::uword begin_slice = 0, const arma::sword end_slice = -1) {
            arma::uword true_end_slice;
            // If the user does not specify an ending index, use the last column
            if (end_slice == -1) { 
                true_end_slice = cube.n_slices - 1; 
            } else {
                true_end_slice = arma::uword(end_slice);
            }
            return py::make_iterator(cube.begin_slice(begin_slice), cube.end_slice(true_end_slice));
        }, "cube"_a, "begin_slice"_a = 0, "end_slice"_a = -1, py::keep_alive<0,1>());
    }

    template void expose_cube_functions<double>(py::module &m);
    template void expose_cube_functions<float>(py::module &m);
    template void expose_cube_functions<arma::uword>(py::module &m);
    template void expose_cube_functions<arma::sword>(py::module &m);
    template void expose_cube_functions<arma::cx_double>(py::module &m);
    template void expose_cube_functions<arma::cx_float>(py::module &m);
}