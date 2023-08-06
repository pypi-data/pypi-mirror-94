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
#include "pybind11/iostream.h"
#include "armadillo"
#include <type_traits>
#include "pybind11/complex.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    /* Defining functions that only work on real types 
       (double, float, and their complex forms)
       and require scoped stream redirections */
    template<typename T>
    void expose_noisy_real_funcs(py::module &m) {
        using Type = typename T::elem_type;
        using Matrix = arma::Mat<Type>;
        using PodType = typename arma::get_pod_type<Type>::result;
        using CxType = typename std::conditional<arma::is_cx<Type>::value, Type, std::complex<Type>>::type;
        
        // Expose functions
        m.def("roots", [](const T &matrix) { 
            arma::Mat<CxType> temp;
            roots(temp, matrix);
            return temp; 
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("roots", [](arma::Mat<CxType> &result, const T &matrix) {
            return roots(result, matrix); 
        }, "result"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("cond", [](const T &matrix) { 
            return cond(matrix);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        // Expose signal processing
        .def("polyfit", [](const T &X, const T &Y, const arma::uword &N) { 
            Matrix P;
            polyfit(P, X, Y, N);
            return P;
        }, "X"_a, "Y"_a, "N"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("polyfit", [](Matrix &P, const T &X, const T &Y, const arma::uword &N) {
            return polyfit(P, X, Y, N);
        }, "P"_a, "X"_a, "Y"_a, "N"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
                // Principal component analysis
        .def("princomp", [](const T &matrix) {
            Matrix coeff, score;
            arma::Col<PodType> latent;
            arma::Col<Type> tsquared;
            arma::princomp(coeff, score, latent, tsquared, matrix);
            return std::make_tuple(coeff, score, arma::Mat<PodType>(latent), Matrix(tsquared));
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("princomp", [](Matrix &coeff, const T &matrix) {
            return arma::princomp(coeff, matrix);
        }, "coeff"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("princomp", [](Matrix &coeff, Matrix &score, const T &matrix) {
            return arma::princomp(coeff, score, matrix);
        }, "coeff"_a, "score"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("princomp", [](Matrix &coeff, Matrix &score, arma::Mat<PodType> &latent, const T &matrix) {
            arma::Col<PodType> temp_latent;
            bool result = arma::princomp(coeff, score, temp_latent, matrix);
            latent = temp_latent; 
            return result;
        }, "coeff"_a, "score"_a, "latent"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("princomp", [](Matrix &coeff, Matrix &score, arma::Mat<PodType> &latent, Matrix &tsquared, const T &matrix) {
            arma::Col<PodType> temp_latent;
            arma::Col<Type> temp_tsquared;
            bool result = arma::princomp(coeff, score, temp_latent, temp_tsquared, matrix);
            latent = temp_latent; 
            tsquared = temp_tsquared;
            return result;
        }, "coeff"_a, "score"_a, "latent"_a, "tsquared"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>());
    }

    template void expose_noisy_real_funcs<arma::mat>(py::module &m);

    template void expose_noisy_real_funcs<arma::Mat<float>>(py::module &m);

    template void expose_noisy_real_funcs<arma::Mat<arma::cx_double>>(py::module &m);
 
    template void expose_noisy_real_funcs<arma::Mat<arma::cx_float>>(py::module &m);
}