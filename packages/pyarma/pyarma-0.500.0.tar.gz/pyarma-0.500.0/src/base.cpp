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

#include "force_inst.hpp"
#include "force_inst_sub.hpp"
#include "force_inst_diag.hpp"
#include "pybind11/pybind11.h"
#include "armadillo"
#include "comparisons.hpp"
#include "indexing.hpp"
#include "properties.hpp"
#include "functions/sigproc.hpp"
#include "functions/stats.hpp"
#include "functions/real_functions.hpp"
#include "functions/element_wise.hpp"
#include "indexing/element.hpp"
#include "methods/md_base.hpp"

namespace py = pybind11;

namespace pyarma {
    // Expose a base class along with its functions and methods
    template<typename T, typename Derived>
    void declare_base(py::module &m, const std::string typestr) {
        using Class = arma::Base<T, Derived>;
        using PodType = typename arma::get_pod_type<T>::result;

        py::class_<Class> base (m, typestr.c_str());
        
        expose_base_methods<T, Derived>(base);

        // expose properties
        expose_props<T, Derived>(base);

        // expose comparisons
        expose_comparisons<Derived, arma::Mat<T>>(base);
        expose_comparisons<Derived, arma::subview<T>>(base);
        // expose_comparisons<Derived, arma::diagview<T>>(base);
        // expose_comparisons<Derived, arma::subview_elem1<T, arma::umat>>(base);
        // expose_comparisons<Derived, arma::subview_elem2<T, arma::umat, arma::umat>>(base);
        
        // // expose signal processing
        // expose_conv<Derived>(m);
        // expose_ifft<Derived>(m);
        // expose_interp<Derived>(m);

        // // expose statistics
        // expose_stats<Derived>(m);
        // expose_hist<Derived>(m);

        // // expose dual-argument trigonometric functions
        // expose_trig<Derived>(m);

        // // expose real and complex functions
        // expose_real_funcs<Derived>(m, base);

        // // expose kmeans
        // expose_kmeans<Derived>(m);

        // // expose element-wise functions
        // expose_element_wise<Derived>(m);
    }

    template void declare_base<double, arma::mat>(py::module &m, const std::string typestr);
    template void declare_base<double, arma::subview<double>>(py::module &m, const std::string typestr);
    template void declare_base<double, arma::diagview<double>>(py::module &m, const std::string typestr);
    template void declare_base<double, arma::subview_elem1<double, arma::umat>>(py::module &m, const std::string typestr);
    template void declare_base<double, arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m, const std::string typestr);

    template void declare_base<float, arma::Mat<float>>(py::module &m, const std::string typestr);
    template void declare_base<float, arma::subview<float>>(py::module &m, const std::string typestr);
    template void declare_base<float, arma::diagview<float>>(py::module &m, const std::string typestr);
    template void declare_base<float, arma::subview_elem1<float, arma::umat>>(py::module &m, const std::string typestr);
    template void declare_base<float, arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m, const std::string typestr);

    template void declare_base<arma::cx_double, arma::Mat<arma::cx_double>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_double, arma::subview<arma::cx_double>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_double, arma::diagview<arma::cx_double>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_double, arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_double, arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m, const std::string typestr);
 
    template void declare_base<arma::cx_float, arma::Mat<arma::cx_float>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_float, arma::subview<arma::cx_float>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_float, arma::diagview<arma::cx_float>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_float, arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m, const std::string typestr);
    template void declare_base<arma::cx_float, arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m, const std::string typestr);

    template void declare_base<arma::uword, arma::Mat<arma::uword>>(py::module &m, const std::string typestr);
    template void declare_base<arma::uword, arma::subview<arma::uword>>(py::module &m, const std::string typestr);
    template void declare_base<arma::uword, arma::diagview<arma::uword>>(py::module &m, const std::string typestr);
    template void declare_base<arma::uword, arma::subview_elem1<arma::uword, arma::umat>>(py::module &m, const std::string typestr);
    template void declare_base<arma::uword, arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m, const std::string typestr);

    template void declare_base<arma::sword, arma::Mat<arma::sword>>(py::module &m, const std::string typestr);
    template void declare_base<arma::sword, arma::subview<arma::sword>>(py::module &m, const std::string typestr);
    template void declare_base<arma::sword, arma::diagview<arma::sword>>(py::module &m, const std::string typestr);
    template void declare_base<arma::sword, arma::subview_elem1<arma::sword, arma::umat>>(py::module &m, const std::string typestr);
    template void declare_base<arma::sword, arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m, const std::string typestr);
}