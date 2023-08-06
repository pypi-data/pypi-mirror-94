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
#include "pybind11/complex.h"
#include "armadillo"
#include "force_inst.hpp"
#include "force_inst_sub.hpp"
#include "force_inst_diag.hpp"
#include "methods/md_is_mat.hpp"
#include "methods/md_chk.hpp"
#include "methods/md_extremum.hpp"
#include "methods/md_fill.hpp"
#include "methods/md_is_symm.hpp"
#include "methods/md_print.hpp"
#include "methods/md_save.hpp"
#include "methods/md_trans.hpp"
#include "methods/md_vec.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose base methods
    template<typename T, typename Derived>
    void expose_base_methods(py::class_<arma::Base<T, Derived>> &py_class) {
        // exposing Base methods
        expose_is_mat<T, Derived>(py_class);
        expose_chk<T, Derived>(py_class);
        expose_extremum_md<T, Derived>(py_class);
        expose_is_symm<T, Derived>(py_class);
        expose_print<T, Derived>(py_class);
        expose_save<T, Derived>(py_class);
        expose_trans_md<T, Derived>(py_class);
        expose_fill_md<T, Derived>(py_class);
        expose_vec<T, Derived>(py_class);

        py_class.def("is_vec", [](const Derived &matrix) { return matrix.is_vec(); })

            .def("is_colvec", [](const Derived &matrix) { return matrix.is_colvec(); })

            .def("is_rowvec", [](const Derived &matrix) { return matrix.is_rowvec(); })

            .def("is_square", [](const Derived &matrix) { return matrix.is_square(); })

            .def("is_empty", [](const Derived &matrix) { return matrix.is_empty(); })

            .def("replace", [](Derived &matrix, const T &old_value, const T &new_value) { matrix.replace(old_value, new_value); })

            .def("eval", [](Derived &matrix) { return matrix.eval(); })

            // negation
            .def("__neg__", [](const Derived &matrix) { return (-matrix).eval(); })

            // methods normally exclusive to Mat<T>
            .def("in_range", [](const arma::Mat<T> &matrix, const arma::uword i) { return matrix.in_range(i); })
            .def("in_range", [](const arma::Mat<T> &matrix, const arma::uword row, const arma::uword col) { return matrix.in_range(row, col); })
            .def("in_range", [](const arma::Mat<T> &matrix, const arma::uword row, const arma::uword col, const arma::SizeMat &size) { return matrix.in_range(row, col, size); })
            .def("in_range", [](const arma::Mat<T> &matrix, const py::slice &rows, const py::slice &cols) { 
                py::object st_col = cols.attr("start"), sp_col = cols.attr("stop"),
                    st_row = rows.attr("start"), sp_row = rows.attr("stop");
                arma::uword start_row, start_col, stop_row, stop_col;
                start_col = st_col.cast<arma::uword>();
                stop_col = sp_col.cast<arma::uword>();
                start_row = st_row.cast<arma::uword>();
                stop_row = sp_row.cast<arma::uword>();
                return matrix.in_range(arma::span(start_row, stop_row), arma::span(start_col, stop_col)); 
            })
            .def("in_range", [](const arma::Mat<T> &matrix, const py::slice &elems) {
                py::object st_elem = elems.attr("start"), sp_elem = elems.attr("stop");
                arma::uword start_elem, stop_elem;
                start_elem = st_elem.cast<arma::uword>();
                stop_elem = sp_elem.cast<arma::uword>();
                return matrix.in_range(arma::span(start_elem, stop_elem));
            })

            // overloading Python's len() function
            .def("__len__", [](const arma::Mat<T> &matrix) { return matrix.size(); });
    }

    template void expose_base_methods<double, arma::mat>(py::class_<arma::Base<double, arma::mat>> &py_class);
    template void expose_base_methods<double, arma::subview<double>>(py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_base_methods<double, arma::diagview<double>>(py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    template void expose_base_methods<double, arma::subview_elem1<double, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    template void expose_base_methods<double, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    template void expose_base_methods<float, arma::Mat<float>>(py::class_<arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_base_methods<float, arma::subview<float>>(py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_base_methods<float, arma::diagview<float>>(py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    template void expose_base_methods<float, arma::subview_elem1<float, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    template void expose_base_methods<float, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    template void expose_base_methods<arma::cx_double, arma::Mat<arma::cx_double>>(py::class_<arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_base_methods<arma::cx_double, arma::subview<arma::cx_double>>(py::class_<arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    template void expose_base_methods<arma::cx_double, arma::diagview<arma::cx_double>>(py::class_<arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    template void expose_base_methods<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>(py::class_<arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    template void expose_base_methods<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::class_<arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
 
    template void expose_base_methods<arma::cx_float, arma::Mat<arma::cx_float>>(py::class_<arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_base_methods<arma::cx_float, arma::subview<arma::cx_float>>(py::class_<arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    template void expose_base_methods<arma::cx_float, arma::diagview<arma::cx_float>>(py::class_<arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    template void expose_base_methods<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>(py::class_<arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    template void expose_base_methods<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::class_<arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);

    template void expose_base_methods<arma::uword, arma::Mat<arma::uword>>(py::class_<arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_base_methods<arma::uword, arma::subview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_base_methods<arma::uword, arma::diagview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    template void expose_base_methods<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    template void expose_base_methods<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    template void expose_base_methods<arma::sword, arma::Mat<arma::sword>>(py::class_<arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    template void expose_base_methods<arma::sword, arma::subview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    template void expose_base_methods<arma::sword, arma::diagview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    template void expose_base_methods<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    template void expose_base_methods<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
}