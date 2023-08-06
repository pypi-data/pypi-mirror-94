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
#include "force_inst.hpp"
#include "force_inst_sub.hpp"
#include "force_inst_diag.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose printing methods
    template<typename T, typename Derived>
    void expose_print(py::class_<arma::Base<T, Derived>> &py_class) {
        py_class.def("print", [](const Derived &matrix, std::string header = "") {
                std::ostringstream stream;
                matrix.print(stream, header);
                py::print(stream.str(), "end"_a="");
            }, "header"_a = "")

            // Overload str() and repr()
            .def("__repr__", [](const Derived &matrix) {
                std::ostringstream stream;
                py::object type = py::type::of(py::cast(matrix));
                py::str module = type.attr("__module__");
                py::str qualname = type.attr("__qualname__");
                stream << "<" << std::string(module) << "." << std::string(qualname) << " object at " << &matrix << ">" << std::endl;
                matrix.brief_print(stream);
                return stream.str();
            })
            .def("brief_print", [](const Derived &matrix, std::string header = "") {
                std::ostringstream stream;
                matrix.brief_print(stream, header);
                py::print(stream.str(), "end"_a="");
            }, "header"_a = "");
    }

    template void expose_print<double, arma::mat>(py::class_<arma::Base<double, arma::mat>> &py_class);
    template void expose_print<double, arma::subview<double>>(py::class_<arma::Base<double, arma::subview<double>>> &py_class);
    template void expose_print<double, arma::diagview<double>>(py::class_<arma::Base<double, arma::diagview<double>>> &py_class);
    template void expose_print<double, arma::subview_elem1<double, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem1<double, arma::umat>>> &py_class);
    template void expose_print<double, arma::subview_elem2<double, arma::umat, arma::umat>>(py::class_<arma::Base<double, arma::subview_elem2<double, arma::umat, arma::umat>>> &py_class);

    template void expose_print<float, arma::Mat<float>>(py::class_<arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_print<float, arma::subview<float>>(py::class_<arma::Base<float, arma::subview<float>>> &py_class);
    template void expose_print<float, arma::diagview<float>>(py::class_<arma::Base<float, arma::diagview<float>>> &py_class);
    template void expose_print<float, arma::subview_elem1<float, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem1<float, arma::umat>>> &py_class);
    template void expose_print<float, arma::subview_elem2<float, arma::umat, arma::umat>>(py::class_<arma::Base<float, arma::subview_elem2<float, arma::umat, arma::umat>>> &py_class);

    template void expose_print<arma::cx_double, arma::Mat<arma::cx_double>>(py::class_<arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_print<arma::cx_double, arma::subview<arma::cx_double>>(py::class_<arma::Base<arma::cx_double, arma::subview<arma::cx_double>>> &py_class);
    template void expose_print<arma::cx_double, arma::diagview<arma::cx_double>>(py::class_<arma::Base<arma::cx_double, arma::diagview<arma::cx_double>>> &py_class);
    template void expose_print<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>(py::class_<arma::Base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>> &py_class);
    template void expose_print<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::class_<arma::Base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>> &py_class);
 
    template void expose_print<arma::cx_float, arma::Mat<arma::cx_float>>(py::class_<arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_print<arma::cx_float, arma::subview<arma::cx_float>>(py::class_<arma::Base<arma::cx_float, arma::subview<arma::cx_float>>> &py_class);
    template void expose_print<arma::cx_float, arma::diagview<arma::cx_float>>(py::class_<arma::Base<arma::cx_float, arma::diagview<arma::cx_float>>> &py_class);
    template void expose_print<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>(py::class_<arma::Base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>> &py_class);
    template void expose_print<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::class_<arma::Base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>> &py_class);

    template void expose_print<arma::uword, arma::Mat<arma::uword>>(py::class_<arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_print<arma::uword, arma::subview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::subview<arma::uword>>> &py_class);
    template void expose_print<arma::uword, arma::diagview<arma::uword>>(py::class_<arma::Base<arma::uword, arma::diagview<arma::uword>>> &py_class);
    template void expose_print<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>> &py_class);
    template void expose_print<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>> &py_class);

    template void expose_print<arma::sword, arma::Mat<arma::sword>>(py::class_<arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
    template void expose_print<arma::sword, arma::subview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::subview<arma::sword>>> &py_class);
    template void expose_print<arma::sword, arma::diagview<arma::sword>>(py::class_<arma::Base<arma::sword, arma::diagview<arma::sword>>> &py_class);
    template void expose_print<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>> &py_class);
    template void expose_print<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::class_<arma::Base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>> &py_class);
}