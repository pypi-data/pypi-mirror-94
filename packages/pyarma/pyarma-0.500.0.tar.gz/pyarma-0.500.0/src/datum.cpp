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

namespace py = pybind11;

namespace pyarma {
    // Expose the datum and fdatum classes
    arma_cold void expose_const(py::module &m) {
        py::class_<arma::datum>(m, "datum")
            .def_readonly_static("pi", &arma::datum::pi)
            .def_readonly_static("inf", &arma::datum::inf)
            .def_readonly_static("nan", &arma::datum::nan)
            .def_readonly_static("e", &arma::datum::e)
            .def_readonly_static("sqrt2", &arma::datum::sqrt2)
            .def_readonly_static("sqrt2pi", &arma::datum::sqrt2pi)
            .def_readonly_static("eps", &arma::datum::eps)
            .def_readonly_static("log_min", &arma::datum::log_min)
            .def_readonly_static("log_max", &arma::datum::log_max)
            .def_readonly_static("euler", &arma::datum::euler)
            .def_readonly_static("gratio", &arma::datum::gratio)
            .def_readonly_static("m_u", &arma::datum::m_u)
            .def_readonly_static("N_A", &arma::datum::N_A)
            .def_readonly_static("k", &arma::datum::k)
            .def_readonly_static("k_evk", &arma::datum::k_evk)
            .def_readonly_static("a_0", &arma::datum::a_0)
            .def_readonly_static("mu_B", &arma::datum::mu_B)
            .def_readonly_static("Z_0", &arma::datum::Z_0)
            .def_readonly_static("G_0", &arma::datum::G_0)
            .def_readonly_static("k_e", &arma::datum::k_e)
            .def_readonly_static("eps_0", &arma::datum::eps_0)
            .def_readonly_static("m_e", &arma::datum::m_e)
            .def_readonly_static("eV", &arma::datum::eV)
            .def_readonly_static("ec", &arma::datum::ec)
            .def_readonly_static("F", &arma::datum::F)
            .def_readonly_static("alpha", &arma::datum::alpha)
            .def_readonly_static("alpha_inv", &arma::datum::alpha_inv)
            .def_readonly_static("K_J", &arma::datum::K_J)
            .def_readonly_static("mu_0", &arma::datum::mu_0)
            .def_readonly_static("phi_0", &arma::datum::phi_0)
            .def_readonly_static("R", &arma::datum::R)
            .def_readonly_static("G", &arma::datum::G)
            .def_readonly_static("h", &arma::datum::h)
            .def_readonly_static("h_bar", &arma::datum::h_bar)
            .def_readonly_static("m_p", &arma::datum::m_p)
            .def_readonly_static("R_inf", &arma::datum::R_inf)
            .def_readonly_static("c_0", &arma::datum::c_0)
            .def_readonly_static("sigma", &arma::datum::sigma)
            .def_readonly_static("R_k", &arma::datum::R_k)
            .def_readonly_static("b", &arma::datum::b);

            py::class_<arma::fdatum>(m, "fdatum")
            .def_readonly_static("pi", &arma::fdatum::pi)
            .def_readonly_static("inf", &arma::fdatum::inf)
            .def_readonly_static("nan", &arma::fdatum::nan)
            .def_readonly_static("e", &arma::fdatum::e)
            .def_readonly_static("sqrt2", &arma::fdatum::sqrt2)
            .def_readonly_static("sqrt2pi", &arma::fdatum::sqrt2pi)
            .def_readonly_static("eps", &arma::fdatum::eps)
            .def_readonly_static("log_min", &arma::fdatum::log_min)
            .def_readonly_static("log_max", &arma::fdatum::log_max)
            .def_readonly_static("euler", &arma::fdatum::euler)
            .def_readonly_static("gratio", &arma::fdatum::gratio)
            .def_readonly_static("m_u", &arma::fdatum::m_u)
            .def_readonly_static("N_A", &arma::fdatum::N_A)
            .def_readonly_static("k", &arma::fdatum::k)
            .def_readonly_static("k_evk", &arma::fdatum::k_evk)
            .def_readonly_static("a_0", &arma::fdatum::a_0)
            .def_readonly_static("mu_B", &arma::fdatum::mu_B)
            .def_readonly_static("Z_0", &arma::fdatum::Z_0)
            .def_readonly_static("G_0", &arma::fdatum::G_0)
            .def_readonly_static("k_e", &arma::fdatum::k_e)
            .def_readonly_static("eps_0", &arma::fdatum::eps_0)
            .def_readonly_static("m_e", &arma::fdatum::m_e)
            .def_readonly_static("eV", &arma::fdatum::eV)
            .def_readonly_static("ec", &arma::fdatum::ec)
            .def_readonly_static("F", &arma::fdatum::F)
            .def_readonly_static("alpha", &arma::fdatum::alpha)
            .def_readonly_static("alpha_inv", &arma::fdatum::alpha_inv)
            .def_readonly_static("K_J", &arma::fdatum::K_J)
            .def_readonly_static("mu_0", &arma::fdatum::mu_0)
            .def_readonly_static("phi_0", &arma::fdatum::phi_0)
            .def_readonly_static("R", &arma::fdatum::R)
            .def_readonly_static("G", &arma::fdatum::G)
            .def_readonly_static("h", &arma::fdatum::h)
            .def_readonly_static("h_bar", &arma::fdatum::h_bar)
            .def_readonly_static("m_p", &arma::fdatum::m_p)
            .def_readonly_static("R_inf", &arma::fdatum::R_inf)
            .def_readonly_static("c_0", &arma::fdatum::c_0)
            .def_readonly_static("sigma", &arma::fdatum::sigma)
            .def_readonly_static("R_k", &arma::fdatum::R_k)
            .def_readonly_static("b", &arma::fdatum::b);
    }
}