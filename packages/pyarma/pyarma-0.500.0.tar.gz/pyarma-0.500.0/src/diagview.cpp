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

#include "force_inst_diag.hpp"
// #include "force_inst_sub.hpp"
// #include "force_inst.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "arithmetic_diag_rev.hpp"
#include "arithmetic/schur/schur_dir.hpp"
#include "arithmetic_dir.hpp"
#include "indexing_element.hpp"

namespace py = pybind11;

namespace pyarma {
    // Expose a diagview and its methods
    template<typename T>
    void declare_diagview(py::module &m, const std::string typestr) {
        using Class = arma::diagview<T>;
        // Mangle the type string
        std::string typestring = "__" + typestr;
        py::class_<Class, arma::Base<T, Class>> diagview (m, typestring.c_str());

        // Expose methods and overload for element-wise multiplication
        diagview.def("randu", [](Class &matrix) { matrix.randu(); })
                .def("randn", [](Class &matrix) { matrix.randn(); })
                // TODO: port to use dir_ops or some other form, possible diagview_ops_r.
                .def("__matmul__", &schur<Class, Class>)
                .def("__imatmul__", &schur<Class, Class>);

        // expose_dir_ops<Class, Class>(diagview);
        expose_diagview_ops_r<Class, arma::Mat<T>>(diagview);
        // expose_diagview_ops_r<Class, arma::subview<T>>(diagview);
        expose_dir_ops<Class, T>(diagview);
        // expose_dir_ops<Class, arma::subview_elem1<T, arma::umat>>(diagview);
        // expose_dir_ops<Class, arma::subview_elem2<T, arma::umat, arma::umat>>(diagview);
        expose_element_get_set<T, Class>(diagview);
    }

    template void declare_diagview<double>(py::module &m, const std::string typestr);
    template void declare_diagview<float>(py::module &m, const std::string typestr);
    template void declare_diagview<arma::cx_double>(py::module &m, const std::string typestr);
    template void declare_diagview<arma::cx_float>(py::module &m, const std::string typestr);
    template void declare_diagview<arma::uword>(py::module &m, const std::string typestr);
    template void declare_diagview<arma::sword>(py::module &m, const std::string typestr);
}

