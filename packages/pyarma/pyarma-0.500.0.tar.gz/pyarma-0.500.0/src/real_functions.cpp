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
#include <type_traits>
#include "pybind11/complex.h"
#include "functions/fn_det.hpp"
#include "functions/fn_expmat.hpp"
#include "functions/fn_logmat.hpp"
#include "functions/fn_sqrtmat.hpp"
#include "functions/fn_powmat.hpp"
#include "functions/fn_norm.hpp"
#include "functions/noisy_real.hpp"
#include "functions/fn_logdet.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    /* Defining functions and methods that only work on real types 
       (double, float, and their complex forms) */
    template<typename T>
    typename std::enable_if<!(arma::is_supported_blas_type<typename T::elem_type>::value)>::type
    expose_real_funcs(py::module &, py::class_<T, arma::Base<typename T::elem_type, T>> &) { }

    template<typename T>
    typename std::enable_if<arma::is_supported_blas_type<typename T::elem_type>::value>::type
    expose_real_funcs(py::module &m, py::class_<T, arma::Base<typename T::elem_type, T>> &py_class) {
        using Type = typename T::elem_type;
        using Matrix = arma::Mat<Type>;
        using PodType = typename arma::get_pod_type<Type>::result;
        using CxType = typename std::conditional<arma::is_cx<Type>::value, Type, std::complex<Type>>::type;

        expose_det<Type>(m);
        expose_logdet<Type>(m);
        expose_expmat<Type>(m);
        expose_logmat<Type>(m);
        expose_norm<Type>(m);
        expose_sqrtmat<Type>(m);
        expose_powmat<Type>(m);
        expose_noisy_real_funcs<T>(m);

        // Expose methods
        py_class.def("i", [](const T &matrix) { return matrix.i().eval(); })

                .def("is_sympd", [](const T &matrix) { return matrix.is_sympd(); })
                .def("is_sympd", [](const T &matrix, PodType tol) { return matrix.is_sympd(tol); });
        
        // Expose functions
        m.def("symmatu", [](const T &matrix, bool do_conj = true) {
            return symmatu(matrix, do_conj).eval();
        }, "matrix"_a, "do_conj"_a = true)
        .def("symmatl", [](const T &matrix, bool do_conj = true) {
            return symmatl(matrix, do_conj).eval();
        }, "matrix"_a, "do_conj"_a = true)

        .def("rcond", [](const Matrix &matrix) { return rcond(matrix); })

        .def("rank", [](const T &matrix) { return arma::rank(matrix); })
        .def("rank", [](const T &matrix, const PodType &tolerance) { return arma::rank(matrix, tolerance); })

        // Expose signal processing
        .def("fft", [](const T &X) { return fft(X).eval(); })
        .def("fft", [](const T &X, const arma::uword &n) { return fft(X, n).eval(); })

        .def("fft2", [](const T &X) { return fft2(X).eval(); })
        .def("fft2", [](const T &X, const arma::uword &n_rows, const arma::uword &n_cols) {
            return fft2(X, n_rows, n_cols).eval(); 
        })
        
        .def("polyval", [](const T &P, const T &X) { return polyval(P, X).eval(); });
    }

    template void expose_real_funcs<arma::mat>(py::module &m, py::class_<arma::mat, arma::Base<double, arma::Mat<double>>> &py_class);
    // template void expose_real_funcs<arma::subview<double>>(py::module &m, py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    // template void expose_real_funcs<arma::diagview<double>>(py::module &m, py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem1<double, arma::umat>>(py::module &m, py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m, py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    template void expose_real_funcs<arma::Mat<float>>(py::module &m, py::class_<arma::fmat, arma::Base<float, arma::Mat<float>>> &py_class);
    // template void expose_real_funcs<arma::subview<float>>(py::module &m, py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    // template void expose_real_funcs<arma::diagview<float>>(py::module &m, py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem1<float, arma::umat>>(py::module &m, py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m, py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    template void expose_real_funcs<arma::Mat<arma::cx_double>>(py::module &m, py::class_<arma::cx_mat, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    // template void expose_real_funcs<arma::subview<arma::cx_double>>(py::module &m, py::class_<arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    // template void expose_real_funcs<arma::diagview<arma::cx_double>>(py::module &m, py::class_<arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m, py::class_<arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m, py::class_<arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
 
    template void expose_real_funcs<arma::Mat<arma::cx_float>>(py::module &m, py::class_<arma::cx_fmat, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    // template void expose_real_funcs<arma::subview<arma::cx_float>>(py::module &m, py::class_<arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    // template void expose_real_funcs<arma::diagview<arma::cx_float>>(py::module &m, py::class_<arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m, py::class_<arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m, py::class_<arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);

    template void expose_real_funcs<arma::Mat<arma::uword>>(py::module &m, py::class_<arma::umat, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    // template void expose_real_funcs<arma::subview<arma::uword>>(py::module &m, py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    // template void expose_real_funcs<arma::diagview<arma::uword>>(py::module &m, py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m, py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m, py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    template void expose_real_funcs<arma::Mat<arma::sword>>(py::module &m, py::class_<arma::imat, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    // template void expose_real_funcs<arma::subview<arma::sword>>(py::module &m, py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    // template void expose_real_funcs<arma::diagview<arma::sword>>(py::module &m, py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m, py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    // template void expose_real_funcs<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m, py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
}