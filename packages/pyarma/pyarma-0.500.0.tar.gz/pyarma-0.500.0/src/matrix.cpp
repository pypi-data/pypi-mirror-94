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
#include "pybind11/stl.h"
#include "pybind11/numpy.h"
#include "pybind11/complex.h"
#include "armadillo"
#include "constructor.hpp"
#include "arithmetic.hpp"
#include "arithmetic_rev.hpp"
#include "arithmetic_dir.hpp"
#include "joins.hpp"
#include "functions/fn_mat.hpp"
#include "functions/real_functions.hpp"
#include "functions/element_wise.hpp"
#include "methods/md_mat.hpp"
#include "indexing.hpp"
#include "indexing_element.hpp"
#include "indexing_head_tail.hpp"
#include "functions/decomp.hpp"
#include "functions/trig.hpp"
#include "functions/kmeans.hpp"
#include "functions/stats.hpp"
#include "functions/sigproc.hpp"
#include "functions/fn_imag_real.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Exposes a matrix along with its standalone functions and methods
    // TODO: check to see if this is still a bottleneck.
    template<typename T>
    py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> declare_matrix(py::module &m, const std::string typestr) {
        using Class = arma::Mat<T>;

        // Expose standalone functions
        expose_matrix_functions<T>(m);

        // Expose imag/real
        expose_imag_real<T>(m);

        // Expose join standalone functions
        expose_joins<Class, Class>(m);
        expose_joins<Class, Class, Class>(m);
        expose_joins<Class, Class, Class, Class>(m);

        // Expose matrix class
        py::class_<Class, arma::Base<T, Class>> mat (m, typestr.c_str(), py::buffer_protocol());

        // Expose methods
        expose_matrix_methods<T>(mat);
            
        // Expose constructors
        expose_constructor<T>(mat);

        // Expose arithmetic operators
        expose_ops<Class, Class>(mat);
        expose_dir_ops<Class, T>(mat);

        // Expose getters and setters
        expose_get_set<Class>(mat);
        expose_head_tail<Class>(mat);
        expose_element_get_set<T, Class>(mat);

        // expose real and complex functions
        expose_real_funcs<Class>(m, mat);

        // Expose decompositions
        expose_decomp<Class>(m);

        // expose element-wise functions
        expose_element_wise<Class>(m);

        // expose dual-argument trigonometric functions
        expose_trig<Class>(m);

        // expose kmeans
        expose_kmeans<Class>(m);

        // expose statistics
        // #ifndef PYARMA_NO_CX_STATS
        expose_stats<Class>(m);
        // #endif
        expose_hist<Class>(m);

        // expose signal processing
        expose_conv<Class>(m);
        expose_ifft<Class>(m);
        expose_interp<Class>(m);

        return mat;
    }
    
    // Expose a matrix while adding functions and methods exclusive to certain types
    // To shave off these expose_matrix functions, I'll need to see what I can do with those reverse operators.
    template<typename T>
    void expose_matrix(py::module &m, const std::string typestr) { }

    template<>
    void expose_matrix<double>(py::module &m, const std::string typestr) {
        py::class_<arma::mat, arma::Base<double, arma::mat>> matrix_cls = declare_matrix<double>(m, typestr.c_str());
        m.def("clamp", [](const arma::mat &matrix, double min, double max) { return arma::clamp(matrix, min, max).eval(); });
        expose_rops<arma::mat, arma::cx_mat>(matrix_cls);
        // #ifdef PYARMA_NO_CX_STATS
        // expose_stats<arma::mat>(m);
        // #endif
    }

    template<>
    void expose_matrix<float>(py::module &m, const std::string typestr) {
        py::class_<arma::fmat, arma::Base<float, arma::fmat>> matrix_cls = declare_matrix<float>(m, typestr.c_str());
        m.def("clamp", [](const arma::fmat &matrix, float min, float max) { return arma::clamp(matrix, min, max).eval(); });
        expose_rops<arma::fmat, arma::cx_mat>(matrix_cls);
        expose_rops<arma::fmat, arma::cx_fmat>(matrix_cls);
        expose_rops<arma::fmat, arma::mat>(matrix_cls);
        // #ifdef PYARMA_NO_CX_STATS
        // expose_stats<arma::fmat>(m);
        // #endif
    }

    template<>
    void expose_matrix<arma::cx_double>(py::module &m, const std::string typestr) {
        py::class_<arma::cx_mat, arma::Base<arma::cx_double, arma::cx_mat>> matrix_cls = declare_matrix<arma::cx_double>(m, typestr.c_str());
        matrix_cls.def(py::init<arma::mat, arma::mat>(), "real"_a.noconvert(), "imag"_a.noconvert());
        m.def("conj", [](const arma::cx_mat &matrix) { return conj(matrix).eval(); });
    }

    template<>
    void expose_matrix<arma::cx_float>(py::module &m, const std::string typestr) {
        py::class_<arma::cx_fmat, arma::Base<arma::cx_float, arma::cx_fmat>> matrix_cls = declare_matrix<arma::cx_float>(m, typestr.c_str());
        matrix_cls.def(py::init<arma::fmat, arma::fmat>(), "real"_a.noconvert(), "imag"_a.noconvert());
        m.def("conj", [](const arma::cx_fmat &matrix) { return conj(matrix).eval(); });
    }

    template<>
    void expose_matrix<arma::uword>(py::module &m, const std::string typestr) {
        py::class_<arma::umat, arma::Base<arma::uword, arma::umat>> matrix_cls = declare_matrix<arma::uword>(m, typestr.c_str());
        m.def("clamp", [](const arma::umat &matrix, arma::uword min, arma::uword max) { return clamp(matrix, min, max).eval(); });
        expose_rops<arma::umat, arma::mat>(matrix_cls);
        expose_rops<arma::umat, arma::fmat>(matrix_cls);
    }

    template<>
    void expose_matrix<arma::sword>(py::module &m, const std::string typestr) {
        py::class_<arma::imat, arma::Base<arma::sword, arma::imat>> matrix_cls = declare_matrix<arma::sword>(m, typestr.c_str());
        m.def("clamp", [](const arma::imat &matrix, arma::sword min, arma::sword max) { return clamp(matrix, min, max).eval(); });
        expose_rops<arma::imat, arma::mat>(matrix_cls);
        expose_rops<arma::imat, arma::fmat>(matrix_cls);
    }

    template py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> declare_matrix<double>(py::module &m, const std::string typestr);
    template py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> declare_matrix<float>(py::module &m, const std::string typestr);
    template py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> declare_matrix<arma::cx_double>(py::module &m, const std::string typestr);
    template py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> declare_matrix<arma::cx_float>(py::module &m, const std::string typestr);
    template py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> declare_matrix<arma::uword>(py::module &m, const std::string typestr);
    template py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> declare_matrix<arma::sword>(py::module &m, const std::string typestr);

    template void expose_matrix<double>(py::module &m, const std::string typestr);
    template void expose_matrix<float>(py::module &m, const std::string typestr);
    template void expose_matrix<arma::cx_double>(py::module &m, const std::string typestr);
    template void expose_matrix<arma::cx_float>(py::module &m, const std::string typestr);
    template void expose_matrix<arma::uword>(py::module &m, const std::string typestr);
    template void expose_matrix<arma::sword>(py::module &m, const std::string typestr);
}