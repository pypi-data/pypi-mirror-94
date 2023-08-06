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
#include <type_traits>

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Defines convolutions
    template<typename Class>
    void expose_conv(py::module &m) {
        m.def("conv", [](const Class &a, const Class &b, std::string shape = "full") {
            return arma::conv(a, b, shape.c_str()).eval();
        }, "a"_a, "b"_a, "shape"_a = "full")
        
        .def("conv2", [](const Class &a, const Class &b, std::string shape = "full") {
            return arma::conv2(a, b, shape.c_str()).eval();
        }, "a"_a, "b"_a, "shape"_a = "full");
    }

    // Defines inverse fast Fourier transforms for complex types
    template<typename Class>
    typename std::enable_if<!(arma::is_arma_type<Class>::value && 
    (arma::is_cx_float<typename Class::elem_type>::yes ||
     arma::is_cx_double<typename Class::elem_type>::yes))>::type expose_ifft(py::module &) { }

    template<typename Class>
    typename std::enable_if<arma::is_arma_type<Class>::value && 
    (arma::is_cx_float<typename Class::elem_type>::yes ||
     arma::is_cx_double<typename Class::elem_type>::yes)>::type
    expose_ifft(py::module &m) {
        m.def("ifft", [](const Class &Y) { return arma::ifft(Y).eval(); })
         .def("ifft", [](const Class &Y, const arma::uword &n) { return arma::ifft(Y, n).eval(); })
         .def("ifft2", [](const Class &Y) { return arma::ifft2(Y).eval(); })
         .def("ifft2", [](const Class &Y, const arma::uword &n_rows, const arma::uword &n_cols) { return arma::ifft2(Y, n_rows, n_cols).eval(); });
    }
        
    // Defines interpolation for floating-point types
    template<typename Class>
    typename std::enable_if<!(arma::is_real<typename Class::elem_type>::value)>::type
    expose_interp(py::module &) { }

    template<typename Class>
    typename std::enable_if<arma::is_real<typename Class::elem_type>::value>::type
    expose_interp(py::module &m) {
        using Type = typename Class::elem_type;
        m.def("interp1", [](const Class &X, 
                           const Class &Y, 
                           arma::Mat<Type> &XI, 
                           arma::Mat<Type> &YI, 
                           std::string method = "linear", 
                           Type extrapolation_value = arma::Datum<Type>::nan) {
            arma::interp1(X, Y, XI, YI, method.c_str(), extrapolation_value);
        }, "X"_a, "Y"_a, "XI"_a, "YI"_a, "method"_a = "linear", "extrapolation_value"_a = arma::Datum<Type>::nan)
        
        .def("interp2", [](const Class &X, 
                           const Class &Y, 
                           const Class &Z,
                           arma::Mat<Type> &XI, 
                           arma::Mat<Type> &YI, 
                           arma::Mat<Type> &ZI,
                           std::string method = "linear", 
                           Type extrapolation_value = arma::Datum<Type>::nan) {
            arma::interp2(X, Y, Z, XI, YI, ZI, method.c_str(), extrapolation_value);
        }, "X"_a, "Y"_a, "Z"_a, "XI"_a, "YI"_a, "ZI"_a, "method"_a = "linear", "extrapolation_value"_a = arma::Datum<Type>::nan);
    }

    template void expose_conv<arma::mat>(py::module &m);
    // template void expose_conv<arma::subview<double>>(py::module &m);
    // template void expose_conv<arma::diagview<double>>(py::module &m);
    // template void expose_conv<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_conv<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_conv<arma::fmat>(py::module &m);
    // template void expose_conv<arma::subview<float>>(py::module &m);
    // template void expose_conv<arma::diagview<float>>(py::module &m);
    // template void expose_conv<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_conv<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_conv<arma::cx_mat>(py::module &m);
    // template void expose_conv<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_conv<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_conv<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_conv<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);

    template void expose_conv<arma::cx_fmat>(py::module &m);
    // template void expose_conv<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_conv<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_conv<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_conv<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_conv<arma::umat>(py::module &m);
    // template void expose_conv<arma::subview<arma::uword>>(py::module &m);
    // template void expose_conv<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_conv<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_conv<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_conv<arma::imat>(py::module &m);
    // template void expose_conv<arma::subview<arma::sword>>(py::module &m);
    // template void expose_conv<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_conv<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_conv<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);

    template void expose_ifft<arma::mat>(py::module &m);
    // template void expose_ifft<arma::subview<double>>(py::module &m);
    // template void expose_ifft<arma::diagview<double>>(py::module &m);
    // template void expose_ifft<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_ifft<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_ifft<arma::fmat>(py::module &m);
    // template void expose_ifft<arma::subview<float>>(py::module &m);
    // template void expose_ifft<arma::diagview<float>>(py::module &m);
    // template void expose_ifft<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_ifft<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_ifft<arma::cx_mat>(py::module &m);
    // template void expose_ifft<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_ifft<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_ifft<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_ifft<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);

    template void expose_ifft<arma::cx_fmat>(py::module &m);
    // template void expose_ifft<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_ifft<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_ifft<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_ifft<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_ifft<arma::umat>(py::module &m);
    // template void expose_ifft<arma::subview<arma::uword>>(py::module &m);
    // template void expose_ifft<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_ifft<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_ifft<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_ifft<arma::imat>(py::module &m);
    // template void expose_ifft<arma::subview<arma::sword>>(py::module &m);
    // template void expose_ifft<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_ifft<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_ifft<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);

    template void expose_interp<arma::mat>(py::module &m);
    // template void expose_interp<arma::subview<double>>(py::module &m);
    // template void expose_interp<arma::diagview<double>>(py::module &m);
    // template void expose_interp<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_interp<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_interp<arma::fmat>(py::module &m);
    // template void expose_interp<arma::subview<float>>(py::module &m);
    // template void expose_interp<arma::diagview<float>>(py::module &m);
    // template void expose_interp<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_interp<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_interp<arma::cx_mat>(py::module &m);
    // template void expose_interp<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_interp<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_interp<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_interp<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);

    template void expose_interp<arma::cx_fmat>(py::module &m);
    // template void expose_interp<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_interp<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_interp<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_interp<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_interp<arma::umat>(py::module &m);
    // template void expose_interp<arma::subview<arma::uword>>(py::module &m);
    // template void expose_interp<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_interp<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_interp<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_interp<arma::imat>(py::module &m);
    // template void expose_interp<arma::subview<arma::sword>>(py::module &m);
    // template void expose_interp<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_interp<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_interp<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);
}