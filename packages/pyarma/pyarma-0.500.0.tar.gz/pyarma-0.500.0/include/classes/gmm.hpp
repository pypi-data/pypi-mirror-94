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

#pragma once
#include "pybind11/pybind11.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose gmm functions shared by both classes
    template<typename T, typename U>
    inline void expose_gmm_funcs(py::class_<T> &py_class) {
        using Matrix = arma::Mat<U>;

        // log_p exhibits different behaviour depending on what's passed in...
        // Hang on, log_p doesn't take T (fellow GMMs), it takes matrices and the like.
        // this thing only takes floats and doubles.
        // GMMs are split into two bsaed on that fact too.
        // This can take any arma type...
        // I can start with matrices, to be honest.
        // An issue I see here is that without a clear distinction between what's a vector and what's a matrix,
        // we'll run into a conflicting return value problem
        // unless we write our own lambda functions again...
        // Maybe we should just do that now instead of wasting time on normal binds?

        py_class.def("log_p", [](const T &gmm, const Matrix &matrix) {
            Matrix output;

            if (matrix.is_empty()) {
                output = matrix;
            } else if (matrix.is_colvec()) {
                output.set_size(1, 1);
                arma::Col<U> tmp(matrix);
                output[0] = gmm.log_p(tmp);
            } else {
                output = gmm.log_p(matrix);
            }
            return output;
        })
        .def("log_p", [](const T &gmm, const Matrix &matrix, const arma::uword &g) {
            Matrix output;

            if (matrix.is_empty()) {
                output = matrix;
            } else if (matrix.is_colvec()) {
                output.set_size(1, 1);
                arma::Col<U> tmp(matrix);
                output[0] = gmm.log_p(tmp, g);
            } else {
                output = gmm.log_p(matrix, g);
            }
            return output;
        })
        .def("sum_log_p", [](T &gmm, const Matrix &matrix) { return gmm.sum_log_p(matrix); })
        .def("sum_log_p", [](T &gmm, const Matrix &matrix, const arma::uword &g) { return gmm.sum_log_p(matrix, g); })
        .def("avg_log_p", [](T &gmm, const Matrix &matrix) { return gmm.avg_log_p(matrix); })
        .def("avg_log_p", [](T &gmm, const Matrix &matrix, const arma::uword &g) { return gmm.avg_log_p(matrix, g); })
        .def("assign", [](T &gmm, const Matrix &matrix, const arma::gmm_dist_mode &dist) {
            arma::umat output;

            if (matrix.is_empty()) {
            } else if (matrix.is_colvec()) {
                output.set_size(1, 1);
                arma::Col<U> tmp(matrix);
                output[0] = gmm.assign(tmp, dist);
            } else {
                output = gmm.assign(matrix, dist);
            }
            return output;
        })
        .def("raw_hist", [](T &gmm, const Matrix &matrix, const arma::gmm_dist_mode &dist) { return gmm.raw_hist(matrix, dist); })
        .def("norm_hist", [](T &gmm, const Matrix &matrix, const arma::gmm_dist_mode &dist) { return gmm.norm_hist(matrix, dist); })
        .def("generate", [](T &gmm) { return gmm.generate(); })
        .def("generate", [](T &gmm, const arma::uword &N) { return gmm.generate(N); })
        .def("save", &T::save)
        .def("load", &T::load)
        .def("n_gaus", &T::n_gaus)
        .def("n_dims", &T::n_dims)
        .def("reset", &T::reset);
        .def_property_readonly("hefts", [](const T &gmm) { return gmm.hefts; })
        .def_property_readonly("means", [](const T &gmm) { return gmm.means; })
        .def("set_hefts", [](T &gmm, const Matrix &hefts) { gmm.set_hefts<Matrix>(hefts); })
        .def("set_means", [](T &gmm, const Matrix &means) { gmm.set_means<Matrix>(means); })
        .def("learn", [](T &gmm,
                         const Matrix &data,
                         const arma::uword &n_gaus,
                         const arma::gmm_dist_mode &dist_mode,
                         const arma::gmm_seed_mode &seed_mode,
                         const arma::uword &km_iter,
                         const arma::uword &em_iter,
                         const U &var_floor,
                         const bool &print_mode) {
            return gmm.learn(data, n_gaus, dist_mode, seed_mode, km_iter, em_iter, var_floor, print_mode);
        });
    }

    // Expose gmm classes
    inline void expose_gmm(py::module &m) {
        py::class_<arma::gmm_diag> gmm_diag(m, "gmm_diag");
        gmm_diag.def(py::init())
            // .def("dcovs")
            .def("set_params", [](arma::gmm_diag &gmm, const arma::mat &means, const arma::mat &covs, const arma::mat &hefts) {
                gmm.set_params(means, covs, hefts);
            });

        py::class_<arma::fgmm_diag> fgmm_diag(m, "fgmm_diag");
        fgmm_diag.def(py::init())
            .def("set_params", [](arma::fgmm_diag &gmm, const arma::fmat &means, const arma::fmat &covs, const arma::fmat &hefts) {
                gmm.set_params(means, covs, hefts);
            });

        py::class_<arma::gmm_full> gmm_full(m, "gmm_full");
        gmm_full.def(py::init());

        py::class_<arma::fgmm_full> fgmm_full(m, "fgmm_full");
        fgmm_full.def(py::init());

        expose_gmm_funcs<arma::gmm_diag, double>(gmm_diag);
        expose_gmm_funcs<arma::gmm_full, double>(gmm_full);
        expose_gmm_funcs<arma::fgmm_diag, float>(fgmm_diag);
        expose_gmm_funcs<arma::fgmm_full, float>(fgmm_full);
    }
}