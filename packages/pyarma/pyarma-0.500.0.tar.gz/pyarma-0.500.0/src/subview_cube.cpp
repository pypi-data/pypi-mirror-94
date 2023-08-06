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

#define ARMA_DONT_PRINT_ERRORS
// #include "force_inst_cube.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "arithmetic_cube.hpp"
#include "arithmetic_cube_dir.hpp"
#include "indexing_cube_element.hpp"

namespace py = pybind11;

namespace pyarma {
    template<typename T>
    void define_subview_cube(py::module &m, std::string typestr) {
        using Class = arma::subview_cube<T>;
        // Mangle the type string
        std::string typestring = "__" + typestr;

        py::class_<Class, arma::BaseCube<T, Class>> subview_cube (m, typestring.c_str());
        subview_cube.def("clean", [](Class &cube, double value) { cube.clean(value); })
                    .def("randu", [](Class &cube) { cube.randu(); })
                    .def("randn", [](Class &cube) { cube.randn(); });
        cube_def_ops<Class, Class>(subview_cube);
        cube_def_ops<Class, arma::Cube<T>>(subview_cube);
        cube_def_dir_ops<Class, T>(subview_cube);
        // expose_stats<Class>(m);
        // expose_trig<Class>(m);
        expose_cube_element_get_set<T, Class>(subview_cube);
    }

    template void define_subview_cube<double>(py::module &m, std::string typestr);
    template void define_subview_cube<float>(py::module &m, std::string typestr);
    template void define_subview_cube<arma::cx_double>(py::module &m, std::string typestr);
    template void define_subview_cube<arma::cx_float>(py::module &m, std::string typestr);
    template void define_subview_cube<arma::uword>(py::module &m, std::string typestr);
    template void define_subview_cube<arma::sword>(py::module &m, std::string typestr);
}
