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
    template<typename... Args>
    void expose_joins(py::module &m) {
        m.def("join_rows", [](Args... args) { return arma::join_rows(args...).eval(); })
        .def("join_horiz", [](Args... args) { return arma::join_rows(args...).eval(); })
        .def("join_cols", [](Args... args) { return arma::join_cols(args...).eval(); })
        .def("join_vert", [](Args... args) { return arma::join_cols(args...).eval(); });
    }

    template<typename T>
    void cube_expose_joins(py::module &m) {
        using CubeClass = arma::Cube<T>;
        using Matrix = arma::Mat<T>;
        m.def("join_slices", [](CubeClass &c, CubeClass &d) { return arma::join_slices(c, d).eval(); })
        .def("join_slices", [](Matrix &m, Matrix &n) { return arma::join_slices(m, n).eval(); })
        .def("join_slices", [](Matrix &m, CubeClass &c) { return arma::join_slices(m, c).eval(); })
        .def("join_slices", [](CubeClass &c, Matrix &m) { return arma::join_slices(c, m).eval(); });
    }

    template void expose_joins<arma::mat, arma::mat>(py::module &m);
    template void expose_joins<arma::mat, arma::mat, arma::mat>(py::module &m);
    template void expose_joins<arma::mat, arma::mat, arma::mat, arma::mat>(py::module &m);

    template void expose_joins<arma::fmat, arma::fmat>(py::module &m);
    template void expose_joins<arma::fmat, arma::fmat, arma::fmat>(py::module &m);
    template void expose_joins<arma::fmat, arma::fmat, arma::fmat, arma::fmat>(py::module &m);

    template void expose_joins<arma::cx_mat, arma::cx_mat>(py::module &m);
    template void expose_joins<arma::cx_mat, arma::cx_mat, arma::cx_mat>(py::module &m);
    template void expose_joins<arma::cx_mat, arma::cx_mat, arma::cx_mat, arma::cx_mat>(py::module &m);

    template void expose_joins<arma::cx_fmat, arma::cx_fmat>(py::module &m);
    template void expose_joins<arma::cx_fmat, arma::cx_fmat, arma::cx_fmat>(py::module &m);
    template void expose_joins<arma::cx_fmat, arma::cx_fmat, arma::cx_fmat, arma::cx_fmat>(py::module &m);

    template void expose_joins<arma::umat, arma::umat>(py::module &m);
    template void expose_joins<arma::umat, arma::umat, arma::umat>(py::module &m);
    template void expose_joins<arma::umat, arma::umat, arma::umat, arma::umat>(py::module &m);

    template void expose_joins<arma::imat, arma::imat>(py::module &m);
    template void expose_joins<arma::imat, arma::imat, arma::imat>(py::module &m);
    template void expose_joins<arma::imat, arma::imat, arma::imat, arma::imat>(py::module &m);

    template void cube_expose_joins<double>(py::module &m);
    template void cube_expose_joins<float>(py::module &m);
    template void cube_expose_joins<arma::cx_double>(py::module &m);
    template void cube_expose_joins<arma::cx_float>(py::module &m);
    template void cube_expose_joins<arma::uword>(py::module &m);
    template void cube_expose_joins<arma::sword>(py::module &m);
}