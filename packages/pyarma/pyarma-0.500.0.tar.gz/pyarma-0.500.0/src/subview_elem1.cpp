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
#include "force_inst.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "arithmetic_dir.hpp"

namespace py = pybind11;

namespace pyarma {

    // Expose subview_elem1 and its methods
    template<typename T>
    void declare_subview_elem1(py::module &m, const std::string typestr) {
        using Class = arma::subview_elem1<T, arma::umat>;
        // Mangle the type string
        std::string typestring = "__" + typestr;
        py::class_<Class, arma::Base<T, Class>> subview1 (m, typestring.c_str());

        // Expose methods
        subview1.def("randu", [](Class &matrix) { matrix.randu(); })
                .def("randn", [](Class &matrix) { matrix.randn(); });

        // Expose arithmetic operations
        // As we can't check for the number of rows and columns, all operations are "direct"
        // Other alternative is writing some more code for this:
        // Ensure that only the matrix is checked
        // TODO: ensure that matrices, subviews and diagviews can operate on subview_elem1s.
        // Currently, it uses the same dir_ops.
        // TODO: subview_elem1 has no access to schur
        // expose_dir_ops<Class, Class>(subview1);
        expose_dir_ops<Class, arma::Mat<T>>(subview1);
        // expose_dir_ops<Class, arma::subview<T>>(subview1);
        // expose_dir_ops<Class, arma::diagview<T>>(subview1);
        // expose_dir_ops<Class, arma::subview_elem2<T, arma::umat, arma::umat>>(subview1);
        expose_dir_ops<Class, T>(subview1);
    }

    template void declare_subview_elem1<double>(py::module &m, const std::string typestr);
    template void declare_subview_elem1<float>(py::module &m, const std::string typestr);
    template void declare_subview_elem1<arma::cx_double>(py::module &m, const std::string typestr);
    template void declare_subview_elem1<arma::cx_float>(py::module &m, const std::string typestr);
    template void declare_subview_elem1<arma::uword>(py::module &m, const std::string typestr);
    template void declare_subview_elem1<arma::sword>(py::module &m, const std::string typestr);
}