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
#include "force_inst_sub.hpp"
#include "pybind11/pybind11.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "arithmetic.hpp"
#include "arithmetic_dir.hpp"
#include "indexing.hpp"
#include "indexing_element.hpp"

namespace py = pybind11;

namespace pyarma {
    // Expose a subview along with its functions and methods
    template<typename T>
    void declare_subview(py::module &m, const std::string typestr) {
        using Class = arma::subview<T>;

        // Mangle the type string
        std::string typestring = "__" + typestr;
        
        py::class_<Class, arma::Base<T, Class>> subview (m, typestring.c_str());

        // Expose methods
        subview.def("eye", [](Class &matrix) { matrix.eye(); })
            .def("clean", [](Class &matrix, double value) { matrix.clean(value); })
            .def("randu", [](Class &matrix) { matrix.randu(); })
            .def("randn", [](Class &matrix) { matrix.randn(); })
            .def("swap_rows", [](Class &matrix, arma::uword row1, arma::uword row2) { matrix.swap_rows(row1, row2); })
            .def("swap_cols", [](Class &matrix, arma::uword col1, arma::uword col2) { matrix.swap_cols(col1, col2); })
            .def("__iter__", [](Class &matrix) { 
                return py::make_iterator(matrix.begin(), matrix.end()); 
            }, py::keep_alive<0, 1>());

        // Expose arithmetic operations
        expose_ops<Class, Class>(subview);
        expose_ops<Class, arma::Mat<T>>(subview);
        expose_dir_ops<Class, T>(subview);
        // expose_dir_ops<Class, arma::subview_elem1<T, arma::umat>>(subview);
        // expose_dir_ops<Class, arma::subview_elem2<T, arma::umat, arma::umat>>(subview);

        // Expose getters and setters
        expose_get_set<Class>(subview);
        expose_element_get_set<T, Class>(subview);
    }

    template void declare_subview<double>(py::module &m, const std::string typestr);
    template void declare_subview<float>(py::module &m, const std::string typestr);
    template void declare_subview<arma::cx_double>(py::module &m, const std::string typestr);
    template void declare_subview<arma::cx_float>(py::module &m, const std::string typestr);
    template void declare_subview<arma::uword>(py::module &m, const std::string typestr);
    template void declare_subview<arma::sword>(py::module &m, const std::string typestr);
}