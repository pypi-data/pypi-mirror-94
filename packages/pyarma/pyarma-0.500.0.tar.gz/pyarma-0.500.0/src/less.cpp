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
// // #include "force_inst.hpp"
// // #include "force_inst_sub.hpp"
// // #include "force_inst_diag.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Defines less-than operators (<, <=)
    template<typename T, typename U>
    void expose_le(py::class_<arma::Base<typename T::elem_type, T>> &py_class) { 
        using Type = typename T::elem_type;
        py_class.def("__le__", [](const T &l, const U &r) { return (l <= r).eval(); }, py::is_operator())
                .def("__le__", [](const T &l, const Type &r) { return (l <= r).eval(); }, py::is_operator())
                .def("__lt__", [](const T &l, const U &r) { return (l < r).eval(); }, py::is_operator())
                .def("__lt__", [](const T &l, const Type &r) { return (l < r).eval(); }, py::is_operator());
    }

    template void expose_le<arma::Mat<double>, arma::Mat<double>>(py::class_<arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_le<arma::subview<double>, arma::Mat<double>>(py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_le<arma::diagview<double>, arma::Mat<double>>(py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    template void expose_le<arma::subview_elem1<double, arma::umat>, arma::Mat<double>>(py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<double, arma::umat, arma::umat>, arma::Mat<double>>(py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    template void expose_le<arma::Mat<float>, arma::Mat<float>>(py::class_<arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_le<arma::subview<float>, arma::Mat<float>>(py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_le<arma::diagview<float>, arma::Mat<float>>(py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    template void expose_le<arma::subview_elem1<float, arma::umat>, arma::Mat<float>>(py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<float, arma::umat, arma::umat>, arma::Mat<float>>(py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    template void expose_le<arma::Mat<arma::uword>, arma::Mat<arma::uword>>(py::class_<arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_le<arma::subview<arma::uword>, arma::Mat<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_le<arma::diagview<arma::uword>, arma::Mat<arma::uword>>(py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    template void expose_le<arma::subview_elem1<arma::uword, arma::umat>, arma::Mat<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::Mat<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    template void expose_le<arma::Mat<arma::sword>, arma::Mat<arma::sword>>(py::class_<arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    template void expose_le<arma::subview<arma::sword>, arma::Mat<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    template void expose_le<arma::diagview<arma::sword>, arma::Mat<arma::sword>>(py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    template void expose_le<arma::subview_elem1<arma::sword, arma::umat>, arma::Mat<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::Mat<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);



    template void expose_le<arma::Mat<double>, arma::subview<double>>(py::class_<arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_le<arma::subview<double>, arma::subview<double>>(py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_le<arma::diagview<double>, arma::subview<double>>(py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    template void expose_le<arma::subview_elem1<double, arma::umat>, arma::subview<double>>(py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview<double>>(py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    template void expose_le<arma::Mat<float>, arma::subview<float>>(py::class_<arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_le<arma::subview<float>, arma::subview<float>>(py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_le<arma::diagview<float>, arma::subview<float>>(py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    template void expose_le<arma::subview_elem1<float, arma::umat>, arma::subview<float>>(py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview<float>>(py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    template void expose_le<arma::Mat<arma::uword>, arma::subview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_le<arma::subview<arma::uword>, arma::subview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_le<arma::diagview<arma::uword>, arma::subview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    template void expose_le<arma::subview_elem1<arma::uword, arma::umat>, arma::subview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    template void expose_le<arma::Mat<arma::sword>, arma::subview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    template void expose_le<arma::subview<arma::sword>, arma::subview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    template void expose_le<arma::diagview<arma::sword>, arma::subview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    template void expose_le<arma::subview_elem1<arma::sword, arma::umat>, arma::subview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    template void expose_le<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);



    // template void expose_le<arma::Mat<double>, arma::diagview<double>>(py::class_<arma::Base<double, arma::Mat<double>>> &py_class);
    // template void expose_le<arma::subview<double>, arma::diagview<double>>(py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    // template void expose_le<arma::diagview<double>, arma::diagview<double>>(py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_le<arma::subview_elem1<double, arma::umat>, arma::diagview<double>>(py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<double, arma::umat, arma::umat>, arma::diagview<double>>(py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<float>, arma::diagview<float>>(py::class_<arma::Base<float, arma::Mat<float>>> &py_class);
    // template void expose_le<arma::subview<float>, arma::diagview<float>>(py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    // template void expose_le<arma::diagview<float>, arma::diagview<float>>(py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_le<arma::subview_elem1<float, arma::umat>, arma::diagview<float>>(py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<float, arma::umat, arma::umat>, arma::diagview<float>>(py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<arma::uword>, arma::diagview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    // template void expose_le<arma::subview<arma::uword>, arma::diagview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    // template void expose_le<arma::diagview<arma::uword>, arma::diagview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_le<arma::subview_elem1<arma::uword, arma::umat>, arma::diagview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::diagview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<arma::sword>, arma::diagview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    // template void expose_le<arma::subview<arma::sword>, arma::diagview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    // template void expose_le<arma::diagview<arma::sword>, arma::diagview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    // template void expose_le<arma::subview_elem1<arma::sword, arma::umat>, arma::diagview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::diagview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);



    // template void expose_le<arma::Mat<double>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::Base<double, arma::Mat<double>>> &py_class);
    // template void expose_le<arma::subview<double>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    // template void expose_le<arma::diagview<double>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_le<arma::subview_elem1<double, arma::umat>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview_elem1<double, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<float>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::Base<float, arma::Mat<float>>> &py_class);
    // template void expose_le<arma::subview<float>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    // template void expose_le<arma::diagview<float>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_le<arma::subview_elem1<float, arma::umat>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview_elem1<float, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<arma::uword>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    // template void expose_le<arma::subview<arma::uword>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    // template void expose_le<arma::diagview<arma::uword>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_le<arma::subview_elem1<arma::uword, arma::umat>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<arma::sword>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    // template void expose_le<arma::subview<arma::sword>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    // template void expose_le<arma::diagview<arma::sword>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    // template void expose_le<arma::subview_elem1<arma::sword, arma::umat>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);



    // template void expose_le<arma::Mat<double>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::Base<double, arma::Mat<double>>> &py_class);
    // template void expose_le<arma::subview<double>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    // template void expose_le<arma::diagview<double>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    // template void expose_le<arma::subview_elem1<double, arma::umat>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<double, arma::umat, arma::umat>, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<float>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::Base<float, arma::Mat<float>>> &py_class);
    // template void expose_le<arma::subview<float>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    // template void expose_le<arma::diagview<float>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    // template void expose_le<arma::subview_elem1<float, arma::umat>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<float, arma::umat, arma::umat>, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<arma::uword>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    // template void expose_le<arma::subview<arma::uword>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    // template void expose_le<arma::diagview<arma::uword>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    // template void expose_le<arma::subview_elem1<arma::uword, arma::umat>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<arma::uword, arma::umat, arma::umat>, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    // template void expose_le<arma::Mat<arma::sword>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    // template void expose_le<arma::subview<arma::sword>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    // template void expose_le<arma::diagview<arma::sword>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    // template void expose_le<arma::subview_elem1<arma::sword, arma::umat>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    // template void expose_le<arma::subview_elem2<arma::sword, arma::umat, arma::umat>, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
}