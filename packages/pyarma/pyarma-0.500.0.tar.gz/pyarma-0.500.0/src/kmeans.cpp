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
#include "armadillo"
#include <type_traits>

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose kmeans
    template<typename T>
    typename std::enable_if<!(arma::is_real<typename T::elem_type>::value)>::type
    expose_kmeans(py::module &) { }

    template<typename T>
    typename std::enable_if<arma::is_real<typename T::elem_type>::value>::type
    expose_kmeans(py::module &m) {
        using Type = typename T::elem_type;
        m.def("kmeans", [](arma::Mat<Type> &means,
                           const T &data,
                           const arma::uword &k,
                           const arma::gmm_seed_mode &seed_mode,
                           const arma::uword &n_iter,
                           const bool &print_mode) {
            return kmeans(means, data, k, seed_mode, n_iter, print_mode);
        });
    }

    template void expose_kmeans<arma::mat>(py::module &m);
    // template void expose_kmeans<arma::subview<double>>(py::module &m);
    // template void expose_kmeans<arma::diagview<double>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_kmeans<arma::fmat>(py::module &m);
    // template void expose_kmeans<arma::subview<float>>(py::module &m);
    // template void expose_kmeans<arma::diagview<float>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_kmeans<arma::cx_mat>(py::module &m);
    // template void expose_kmeans<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_kmeans<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);

    template void expose_kmeans<arma::cx_fmat>(py::module &m);
    // template void expose_kmeans<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_kmeans<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_kmeans<arma::umat>(py::module &m);
    // template void expose_kmeans<arma::subview<arma::uword>>(py::module &m);
    // template void expose_kmeans<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_kmeans<arma::imat>(py::module &m);
    // template void expose_kmeans<arma::subview<arma::sword>>(py::module &m);
    // template void expose_kmeans<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_kmeans<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);
}