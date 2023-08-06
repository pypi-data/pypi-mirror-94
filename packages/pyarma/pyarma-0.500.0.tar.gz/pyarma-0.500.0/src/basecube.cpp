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

// #include "force_inst_cube.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "cube_comparisons.hpp"
#include "indexing.hpp"
#include "properties.hpp"
#include "functions/sigproc.hpp"
#include "functions/stats.hpp"
#include "functions/trig.hpp"
#include "functions/real_functions.hpp"
#include "functions/kmeans.hpp"
#include "functions/element_wise.hpp"
#include "indexing/element.hpp"
#include "functions/fn_basecube.hpp"
#include "methods/md_basecube.hpp"

namespace py = pybind11;

namespace pyarma {
    template<typename T, typename Derived>
    void cube_declare_base(py::module &m, std::string typestr) {
        using Class = arma::BaseCube<T, Derived>;
        py::class_<Class> basecube (m, typestr.c_str());
        expose_base_cube_functions<T, Derived>(m);
        expose_base_cube_methods<T, Derived>(basecube);
        cube_expose_comparisons<Derived, arma::Cube<T>>(basecube);
        // cube_expose_comparisons<Derived, Derived>(basecube);
        
        // // expose element-wise functions
        // expose_element_wise<Derived>(m);
    }
    
    template void cube_declare_base<double, arma::Cube<double>>(py::module &m, const std::string typestr);
    template void cube_declare_base<double, arma::subview_cube<double>>(py::module &m, const std::string typestr);

    template void cube_declare_base<float, arma::Cube<float>>(py::module &m, const std::string typestr);
    template void cube_declare_base<float, arma::subview_cube<float>>(py::module &m, const std::string typestr);

    template void cube_declare_base<arma::cx_double, arma::Cube<arma::cx_double>>(py::module &m, const std::string typestr);
    template void cube_declare_base<arma::cx_double, arma::subview_cube<arma::cx_double>>(py::module &m, const std::string typestr);

    template void cube_declare_base<arma::cx_float, arma::Cube<arma::cx_float>>(py::module &m, const std::string typestr);
    template void cube_declare_base<arma::cx_float, arma::subview_cube<arma::cx_float>>(py::module &m, const std::string typestr);

    template void cube_declare_base<arma::uword, arma::Cube<arma::uword>>(py::module &m, const std::string typestr);
    template void cube_declare_base<arma::uword, arma::subview_cube<arma::uword>>(py::module &m, const std::string typestr);

    template void cube_declare_base<arma::sword, arma::Cube<arma::sword>>(py::module &m, const std::string typestr);
    template void cube_declare_base<arma::sword, arma::subview_cube<arma::sword>>(py::module &m, const std::string typestr);
}