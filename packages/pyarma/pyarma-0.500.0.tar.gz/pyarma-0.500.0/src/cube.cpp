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
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "arithmetic_cube.hpp"
#include "arithmetic_cube_dir.hpp"
#include "indexing_cube.hpp"
#include "joins.hpp"
#include "functions/trig.hpp"
#include "functions/stats.hpp"
#include "functions/fn_cube.hpp"
#include "methods/md_cube.hpp"
#include "cube_constructor.hpp"
#include "functions/element_wise.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    template<typename T>
    py::class_<arma::Cube<T>, arma::BaseCube<T, arma::Cube<T>>> declare_cube(py::module &m, std::string typestr) {
        using Class = arma::Cube<T>;

        expose_cube_functions<T>(m);

        cube_expose_joins<T>(m);

        py::class_<Class, arma::BaseCube<T, Class>> cube (m, typestr.c_str(), py::buffer_protocol());
        
        expose_cube_methods<T>(cube);

        cube_def_ops<Class, Class>(cube);
        cube_def_dir_ops<Class, T>(cube);
        cube_def_get_set<Class>(cube);
        expose_trig<Class>(m);
        expose_stats<Class>(m);
        cube_expose_constructor<T>(cube);
        
        // expose element-wise functions
        expose_element_wise<Class>(m);
        return cube;
    }
    
    template<typename T>
    void expose_cube(py::module &m, std::string typestr) {
        py::class_<arma::Cube<T>, arma::BaseCube<T, arma::Cube<T>>> cube_cls = declare_cube<T>(m, typestr.c_str());
        m.def("clamp", [](const arma::Cube<T> &cube, T min, T max) { 
            return clamp(cube, min, max).eval(); 
        });
    }

    template<>
    void expose_cube<arma::cx_double>(py::module &m, std::string typestr) {
        py::class_<arma::cx_cube, arma::BaseCube<arma::cx_double, arma::cx_cube>> cube_cls = declare_cube<arma::cx_double>(m, typestr.c_str());
        cube_cls.def(py::init<arma::cube, arma::cube>(), "real"_a.noconvert(), "imag"_a.noconvert());
        m.def("conj", [](const arma::cx_cube &cube) { return conj(cube).eval(); });
    }

    template<>
    void expose_cube<arma::cx_float>(py::module &m, std::string typestr) {
        py::class_<arma::cx_fcube, arma::BaseCube<arma::cx_float, arma::cx_fcube>> cube_cls = declare_cube<arma::cx_float>(m, typestr.c_str());
        cube_cls.def(py::init<arma::fcube, arma::fcube>(), "real"_a.noconvert(), "imag"_a.noconvert());
        m.def("conj", [](const arma::cx_fcube &cube) { return conj(cube).eval(); });
    }

    template py::class_<arma::Cube<double>, arma::BaseCube<double, arma::Cube<double>>> declare_cube<double>(py::module &m, const std::string typestr);
    template py::class_<arma::Cube<float>, arma::BaseCube<float, arma::Cube<float>>> declare_cube<float>(py::module &m, const std::string typestr);
    template py::class_<arma::Cube<arma::cx_double>, arma::BaseCube<arma::cx_double, arma::Cube<arma::cx_double>>> declare_cube<arma::cx_double>(py::module &m, const std::string typestr);
    template py::class_<arma::Cube<arma::cx_float>, arma::BaseCube<arma::cx_float, arma::Cube<arma::cx_float>>> declare_cube<arma::cx_float>(py::module &m, const std::string typestr);
    template py::class_<arma::Cube<arma::uword>, arma::BaseCube<arma::uword, arma::Cube<arma::uword>>> declare_cube<arma::uword>(py::module &m, const std::string typestr);
    template py::class_<arma::Cube<arma::sword>, arma::BaseCube<arma::sword, arma::Cube<arma::sword>>> declare_cube<arma::sword>(py::module &m, const std::string typestr);

    template void expose_cube<double>(py::module &m, const std::string typestr);
    template void expose_cube<float>(py::module &m, const std::string typestr);
    template void expose_cube<arma::cx_double>(py::module &m, const std::string typestr);
    template void expose_cube<arma::cx_float>(py::module &m, const std::string typestr);
    template void expose_cube<arma::uword>(py::module &m, const std::string typestr);
    template void expose_cube<arma::sword>(py::module &m, const std::string typestr);
}
