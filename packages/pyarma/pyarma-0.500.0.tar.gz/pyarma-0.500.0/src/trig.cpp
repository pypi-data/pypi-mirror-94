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

#include "pybind11/pybind11.h"
#include "armadillo"
#include <type_traits>
#include "functions/trig/atrig.hpp"
#include "functions/trig/strig.hpp"
#include "functions/trig/atrigh.hpp"
#include "functions/trig/trigh.hpp"
#include "functions/trig/sinc.hpp"
#include "functions/trig/dual.hpp"

namespace py = pybind11;

namespace pyarma {
    // Defines trigonometric functions
    template<typename T>
    typename std::enable_if<!(arma::is_real<typename T::elem_type>::value)>::type 
    expose_trig(py::module &m) { 
        expose_atrig<T>(m);
        expose_atrigh<T>(m);
        expose_strig<T>(m);
        expose_trigh<T>(m);
        expose_sinc<T>(m);
    }
    
    template<typename T>
    typename std::enable_if<arma::is_real<typename T::elem_type>::value>::type
    expose_trig(py::module &m) {
        expose_atrig<T>(m);
        expose_atrigh<T>(m);
        expose_strig<T>(m);
        expose_trigh<T>(m);
        expose_sinc<T>(m);
        expose_dual<T>(m);
    }

    template void expose_trig<arma::mat>(py::module &m);

    template void expose_trig<arma::fmat>(py::module &m);

    template void expose_trig<arma::cx_mat>(py::module &m);

    template void expose_trig<arma::cx_fmat>(py::module &m);

    template void expose_trig<arma::umat>(py::module &m);

    template void expose_trig<arma::imat>(py::module &m);

    template void expose_trig<arma::Cube<double>>(py::module &m);

    template void expose_trig<arma::Cube<float>>(py::module &m);

    template void expose_trig<arma::Cube<arma::cx_double>>(py::module &m);

    template void expose_trig<arma::Cube<arma::cx_float>>(py::module &m);

    template void expose_trig<arma::Cube<arma::uword>>(py::module &m);

    template void expose_trig<arma::Cube<arma::sword>>(py::module &m);
}