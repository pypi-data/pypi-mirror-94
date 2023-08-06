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
#include "pybind11/iostream.h"
#include "armadillo"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    template<typename T>
    void expose_noisy_stats(py::module &m) { 
        using Type = typename T::elem_type;
        using Matrix = arma::Mat<Type>;
        using PodType = typename arma::get_pod_type<Type>::result;
        
        m.def("mvnrnd", [](const Matrix &M, const Matrix  &C, const arma::uword &N = 1) {
            Matrix X;
            arma::mvnrnd(X, M, C, N);
            return X;
        }, "M"_a, "C"_a, "N"_a = 1, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("mvnrnd", [](Matrix &X, const Matrix &M, const Matrix &C, const arma::uword &N = 1) {
            return arma::mvnrnd(X, M, C, N);
        }, "X"_a, "M"_a, "C"_a, "N"_a = 1, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("wishrnd", [](const Matrix &S, const Type &df) {
            Matrix W;
            arma::wishrnd(W, S, df);
            return W;
        }, "S"_a, "df"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("wishrnd", [](const Matrix &S, const Type &df, const Matrix &D) {
            Matrix W;
            arma::wishrnd(W, S, df, D);
            return W;
        }, "S"_a, "df"_a, "D"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("wishrnd", [](Matrix &W, const Matrix &S, const Type &df) {
            return arma::wishrnd(W, S, df);
        }, "W"_a, "S"_a, "df"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("wishrnd", [](Matrix &W, const Matrix &S, const Type &df, const Matrix &D) {
            return arma::wishrnd(W, S, df, D);
        }, "W"_a, "S"_a, "df"_a, "D"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>());
    }

    template void expose_noisy_stats<arma::mat>(py::module &m);

    template void expose_noisy_stats<arma::fmat>(py::module &m);
}
