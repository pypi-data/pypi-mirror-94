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
    class pyarma_solve_opts {
    public:
        static const arma::solve_opts::opts_none none;
        static const arma::solve_opts::opts_fast fast;
        static const arma::solve_opts::opts_refine refine;
        static const arma::solve_opts::opts_equilibrate equilibrate;
        static const arma::solve_opts::opts_likely_sympd likely_sympd;
        static const arma::solve_opts::opts_allow_ugly allow_sympd;
        static const arma::solve_opts::opts_no_approx no_approx;
        static const arma::solve_opts::opts_no_band no_band;
        static const arma::solve_opts::opts_no_trimat no_trimat;
        static const arma::solve_opts::opts_no_sympd no_sympd;
    };

    const arma::solve_opts::opts_none pyarma_solve_opts::none;
    const arma::solve_opts::opts_fast pyarma_solve_opts::fast;
    const arma::solve_opts::opts_refine pyarma_solve_opts::refine;
    const arma::solve_opts::opts_equilibrate pyarma_solve_opts::equilibrate;
    const arma::solve_opts::opts_likely_sympd pyarma_solve_opts::likely_sympd;
    const arma::solve_opts::opts_allow_ugly pyarma_solve_opts::allow_sympd;
    const arma::solve_opts::opts_no_approx pyarma_solve_opts::no_approx;
    const arma::solve_opts::opts_no_band pyarma_solve_opts::no_band;
    const arma::solve_opts::opts_no_trimat pyarma_solve_opts::no_trimat;
    const arma::solve_opts::opts_no_sympd pyarma_solve_opts::no_sympd;

    // Expose solve options
    arma_cold void expose_solve_opts(py::module &m) {
        // Internal solve_opts exposure
        py::class_<arma::solve_opts::opts>(m, "__solve_opts").def_readonly("flags", &arma::solve_opts::opts::flags)
            .def("__add__", [](const arma::solve_opts::opts &left, const arma::solve_opts::opts &right) {
                return left + right;
            });

        // Expose solve_opts
        py::class_<arma::solve_opts::opts_none, arma::solve_opts::opts>(m, "__solve_opts.none");
        py::class_<arma::solve_opts::opts_fast, arma::solve_opts::opts>(m, "__solve_opts.fast");
        py::class_<arma::solve_opts::opts_refine, arma::solve_opts::opts>(m, "__solve_opts.refine");
        py::class_<arma::solve_opts::opts_equilibrate, arma::solve_opts::opts>(m, "__solve_opts.equilibrate");
        py::class_<arma::solve_opts::opts_likely_sympd, arma::solve_opts::opts>(m, "__solve_opts.likely_sympd");
        py::class_<arma::solve_opts::opts_allow_ugly, arma::solve_opts::opts>(m, "__solve_opts.allow_sympd");
        py::class_<arma::solve_opts::opts_no_approx, arma::solve_opts::opts>(m, "__solve_opts.no_approx");
        py::class_<arma::solve_opts::opts_no_band, arma::solve_opts::opts>(m, "__solve_opts.no_band");
        py::class_<arma::solve_opts::opts_no_trimat, arma::solve_opts::opts>(m, "__solve_opts.no_trimat");
        py::class_<arma::solve_opts::opts_no_sympd, arma::solve_opts::opts>(m, "__solve_opts.no_sympd");
        py::class_<pyarma_solve_opts>(m, "solve_opts")
            .def_readonly_static("fast", &pyarma_solve_opts::fast)
            .def_readonly_static("refine", &pyarma_solve_opts::refine)
            .def_readonly_static("equilibrate", &pyarma_solve_opts::equilibrate)
            .def_readonly_static("likely_sympd", &pyarma_solve_opts::likely_sympd)
            .def_readonly_static("allow_sympd", &pyarma_solve_opts::allow_sympd)
            .def_readonly_static("no_approx", &pyarma_solve_opts::no_approx)
            .def_readonly_static("no_band", &pyarma_solve_opts::no_band)
            .def_readonly_static("no_trimat", &pyarma_solve_opts::no_trimat)
            .def_readonly_static("no_sympd", &pyarma_solve_opts::no_sympd);

        // // Expose as attributes, so solve_opts() is unnecessary
        // m.attr("solve_opts.fast") = py::cast(arma::solve_opts::fast);
        // m.attr("solve_opts.refine") = py::cast(arma::solve_opts::refine);
        // m.attr("solve_opts.equilibrate") = py::cast(arma::solve_opts::equilibrate);
        // m.attr("solve_opts.likely_sympd") = py::cast(arma::solve_opts::likely_sympd);
        // m.attr("solve_opts.allow_ugly") = py::cast(arma::solve_opts::allow_ugly);
        // m.attr("solve_opts.no_approx") = py::cast(arma::solve_opts::no_approx);
        // m.attr("solve_opts.no_band") = py::cast(arma::solve_opts::no_band);
        // m.attr("solve_opts.no_trimat") = py::cast(arma::solve_opts::no_trimat);
        // m.attr("solve_opts.no_sympd") = py::cast(arma::solve_opts::no_sympd);
    }
}