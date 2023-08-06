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
#include "armadillo"
#include <type_traits>
#include "functions/noisy_stats.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose histograms, which can only be used with non-complex types (including integral types)
    template<typename T>
    typename std::enable_if<(arma::is_cx_float<typename T::elem_type>::yes ||
                             arma::is_cx_double<typename T::elem_type>::yes)>::type
    expose_hist(py::module &) { }

    template<typename T>
    typename std::enable_if<!(arma::is_cx_float<typename T::elem_type>::yes ||
                             arma::is_cx_double<typename T::elem_type>::yes)>::type
    expose_hist(py::module &m) {
        // TODO: do this
        // Check what happens if a rowvec is used and if a matrix (non-vec) is used:
        // will this throw a RuntimeError or...?
        // Check if rowvecs return urowvecs as they should. If not, then transpose the result.
        // Alternatively, on detection of a rowvec, just cast it into a vector.
        m.def("hist", [](const T &matrix, const arma::uword &n_bins = 10) { 
            arma::umat output;
            if (matrix.is_rowvec()) {
                output = arma::hist(vectorise(matrix, 1), n_bins); 
            } else if (matrix.is_colvec()) {
                output = arma::hist(vectorise(matrix, 0), n_bins); 
            } else {
                throw py::value_error("Given matrix must be a vector.");
            }
            return output;
        }, "matrix"_a, "n_bins"_a = 10)
        .def("hist", [](const T &matrix, const T &centers) {
            arma::umat output;

            if (matrix.is_rowvec()) {
                output = arma::hist(matrix, centers, 1).eval();
            } else {
                output = arma::hist(matrix, centers, 0).eval();
            }
            return output;
        })
        .def("hist", [](const T &matrix, const T &centers, const arma::uword &dim) {
            return arma::hist(matrix, centers, dim).eval();
        })
        
        .def("histc", [](const T &matrix, const T &edges) {
            arma::umat output;

            if (matrix.is_rowvec()) {
                output = arma::histc(matrix, edges, 1).eval();
            } else {
                output = arma::histc(matrix, edges, 0).eval();
            }
            return output;
        })
        .def("histc", [](const T &matrix, const T &edges, const arma::uword &dim) {
            return arma::histc(matrix, edges, dim).eval();
        });
    }

    template<typename T>
    typename std::enable_if<!(arma::is_real<typename T::elem_type>::value)>::type 
    expose_stats_real(py::module &) { }

    template<typename T>
    typename std::enable_if<arma::is_real<typename T::elem_type>::value>::type 
    expose_stats_real(py::module &m) { 
        using Type = typename T::elem_type;
        expose_noisy_stats<T>(m);
        m.def("quantile", [](const T &matrix, const T &P) {
            arma::Mat<Type> output;

            if (matrix.is_rowvec()) {
                output = arma::quantile(matrix, P, 1).eval();
            } else {
                output = arma::quantile(matrix, P, 0).eval();
            }
            return output;
        })
        .def("quantile", [](const T &matrix, const T &P, const arma::uword &dim) {
            return arma::quantile(matrix, P, dim).eval();
        })

        .def("normpdf", [](const T &X, 
                           const Type &M = 0, 
                           const Type &S = 1) { 
            return arma::normpdf(X).eval(); 
        }, "X"_a, "M"_a = 0, "S"_a = 1)
        .def("normpdf", [](const T &X, const T &M, const T &S) {
            return arma::normpdf(X, M, S).eval();
        })
        .def("normpdf", [](const Type &X, const T &M, const T &S) {
            return arma::normpdf(X, M, S).eval();
        })
        .def("normpdf", [](const Type &X, 
                           const Type &M = 0, 
                           const Type &S = 1) { 
            return arma::normpdf(X); 
        }, "X"_a, "M"_a = 0, "S"_a = 1)

        .def("log_normpdf", [](const T &X, 
                           const Type &M = 0, 
                           const Type &S = 1) { 
            return arma::log_normpdf(X).eval(); 
        }, "X"_a, "M"_a = 0, "S"_a = 1)
        .def("log_normpdf", [](const T &X, const T &M, const T &S) {
            return arma::log_normpdf(X, M, S).eval();
        })
        .def("log_normpdf", [](const Type &X, const T &M, const T &S) {
            return arma::log_normpdf(X, M, S).eval();
        })
        .def("log_normpdf", [](const Type &X, 
                               const Type &M = 0, 
                               const Type &S = 1) { 
            return arma::log_normpdf(X); 
        }, "X"_a, "M"_a = 0, "S"_a = 1)

        .def("normcdf", [](const T &X, 
                           const Type &M = 0, 
                           const Type &S = 1) { 
            return arma::normcdf(X).eval(); 
        }, "X"_a, "M"_a = 0, "S"_a = 1)
        .def("normcdf", [](const T &X, const T &M, const T &S) {
            return arma::normcdf(X, M, S).eval();
        })
        .def("normcdf", [](const Type &X, const T &M, const T &S) {
            return arma::normcdf(X, M, S).eval();
        })
        .def("normcdf", [](const Type &X, 
                           const Type &M = 0, 
                           const Type &S = 1) { 
            return arma::normcdf(X); 
        }, "X"_a, "M"_a = 0, "S"_a = 1)
        
        .def("mvnrnd", [](const arma::Mat<Type> &M, const arma::Mat<Type>  &C, const arma::uword &N = 1) {
            arma::Mat<Type> X;
            arma::mvnrnd(X, M, C, N);
            return X;
        }, "M"_a, "C"_a, "N"_a = 1)
        .def("mvnrnd", [](arma::Mat<Type> &X, const arma::Mat<Type> &M, const arma::Mat<Type> &C, const arma::uword &N = 1) {
            return arma::mvnrnd(X, M, C, N);
        }, "X"_a, "M"_a, "C"_a, "N"_a = 1)
        
        .def("chi2rnd", [](const T &DF) { return arma::chi2rnd(DF).eval(); })
        .def("chi2rnd", [](const Type &DF) {
            return arma::chi2rnd<Type>(DF); 
        })
        .def("chi2rnd", [](const Type &DF, const arma::uword &n_elem) {
            return arma::chi2rnd<arma::Mat<Type>>(DF, n_elem).eval(); 
        })
        .def("chi2rnd", [](const Type &DF, 
                           const arma::uword &n_rows, 
                           const arma::uword &n_cols) {
            return arma::chi2rnd<arma::Mat<Type>>(DF, n_rows, n_cols).eval(); 
        })
        .def("chi2rnd", [](const Type &DF, const arma::SizeMat &size) {
            return arma::chi2rnd<arma::Mat<Type>>(DF, size).eval(); 
        })
        
        .def("wishrnd", [](const arma::Mat<Type> &S, const Type &df) {
            arma::Mat<Type> W;
            arma::wishrnd(W, S, df);
            return W;
        })
        .def("wishrnd", [](const arma::Mat<Type> &S, const Type &df, const arma::Mat<Type> &D) {
            arma::Mat<Type> W;
            arma::wishrnd(W, S, df, D);
            return W;
        })
        .def("wishrnd", [](arma::Mat<Type> &W, const arma::Mat<Type> &S, const Type &df) {
            return arma::wishrnd(W, S, df);
        })
        .def("wishrnd", [](arma::Mat<Type> &W, const arma::Mat<Type> &S, const Type &df, const arma::Mat<Type> &D) {
            return arma::wishrnd(W, S, df, D);
        })
        
        .def("iwishrnd", [](const arma::Mat<Type> &Tm, const Type &df) {
            arma::Mat<Type> W;
            arma::iwishrnd(W, Tm, df);
            return W;
        })
        .def("iwishrnd", [](const arma::Mat<Type> &Tm, const Type &df, const arma::Mat<Type> &Dinv) {
            arma::Mat<Type> W;
            arma::iwishrnd(W, Tm, df, Dinv);
            return W;
        })
        .def("iwishrnd", [](arma::Mat<Type> &W, const arma::Mat<Type> &Tm, const Type &df) {
            return arma::iwishrnd(W, Tm, df);
        })
        .def("iwishrnd", [](arma::Mat<Type> &W, const arma::Mat<Type> &Tm, const Type &df, const arma::Mat<Type> &Dinv) {
            return arma::iwishrnd(W, Tm, df, Dinv);
        });
    }

    /* Expose stats functions
       (only available for real types) */
    template<typename T>
    typename std::enable_if<!(arma::is_supported_blas_type<typename T::elem_type>::value)>::type 
    expose_stats(py::module &) { }

    template<typename T>
    typename std::enable_if<(arma::is_supported_blas_type<typename T::elem_type>::value && !(arma::is_arma_cube_type<T>::value))>::type 
    expose_stats(py::module &m) {
        using Type = typename T::elem_type;
        using PodType = typename arma::get_pod_type<Type>::result;

        m.def("mean", [](const T &matrix) {
            arma::Mat<Type> output;

            if (matrix.is_rowvec()) {
                output = arma::mean(matrix, 1).eval();
            } else {
                output = arma::mean(matrix, 0).eval();
            }
            return output;
        }, "matrix"_a)
        .def("mean", [](const T &matrix, const arma::uword &dim) {
            return arma::mean(matrix, dim).eval();
        }, "matrix"_a, "dim"_a)

        .def("median", [](const T &matrix) {
            arma::Mat<Type> output;

            if (matrix.is_rowvec()) {
                output = arma::median(matrix, 1).eval();
            } else {
                output = arma::median(matrix, 0).eval();
            }
            return output;
        }, "matrix"_a)
        .def("median", [](const T &matrix, arma::uword dim = 0) {
            return arma::median(matrix, dim).eval();
        }, "matrix"_a, "dim"_a = 0)

        .def("stddev", [](const T &matrix, arma::uword norm_type = 0) {
            arma::Mat<PodType> output;

            if (matrix.is_rowvec()) {
                output = arma::stddev(matrix, norm_type, 1).eval();
            } else {
                output = arma::stddev(matrix, norm_type, 0).eval();
            }
            return output;
        }, "matrix"_a, "norm_type"_a = 0)
        .def("stddev", [](const T &matrix, const arma::uword &norm_type, const arma::uword &dim) {
            return arma::stddev(matrix, norm_type, dim).eval();
        }, "matrix"_a, "norm_type"_a, "dim"_a)
        .def("stddev", [](const T &matrix, const arma::uword &dim) {
            return arma::stddev(matrix, 0, dim).eval();
        }, "matrix"_a, "dim"_a)

        .def("var", [](const T &matrix, arma::uword norm_type = 0) {
            arma::Mat<PodType> output;

            if (matrix.is_rowvec()) {
                output = arma::var(matrix, norm_type, 1).eval();
            } else {
                output = arma::var(matrix, norm_type, 0).eval();
            }
            return output;
        }, "matrix"_a, "norm_type"_a = 0)
        .def("var", [](const T &matrix, const arma::uword &norm_type, const arma::uword &dim) {
            return arma::var(matrix, norm_type, dim).eval();
        }, "matrix"_a, "norm_type"_a, "dim"_a)
        .def("var", [](const T &matrix, const arma::uword &dim) {
            return arma::var(matrix, 0, dim).eval();
        }, "matrix"_a, "dim"_a)
        
        .def("spread", [](const T &matrix) {
            arma::Mat<Type> output;

            if (matrix.is_rowvec()) {
                output = arma::range(matrix, 1).eval();
            } else {
                output = arma::range(matrix, 0).eval();
            }
            return output;
        }, "matrix"_a)
        .def("spread", [](const T &matrix, arma::uword dim = 0) {
            return arma::range(matrix, dim).eval();
        }, "matrix"_a, "dim"_a = 0)
        
        .def("cov", [](const T &matrix, arma::uword norm_type = 0) {
            return arma::cov(matrix, norm_type).eval();
        }, "matrix"_a, "norm_type"_a = 0)
        .def("cov", [](const T &l, const arma::Mat<Type> &r, arma::uword norm_type = 0) {
            return arma::cov(l, r, norm_type).eval();
        }, "l"_a, "r"_a, "norm_type"_a = 0)
        // .def("cov", [](const T &l, const arma::subview<Type> &r, arma::uword norm_type = 0) {
        //     return arma::cov(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0)
        // .def("cov", [](const T &l, const arma::diagview<Type> &r, arma::uword norm_type = 0) {
        //     return arma::cov(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0)
        // .def("cov", [](const T &l, const arma::subview_elem1<Type, arma::umat> &r, arma::uword norm_type = 0) {
        //     return arma::cov(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0)
        // .def("cov", [](const T &l, const arma::subview_elem2<Type, arma::umat, arma::umat> &r, arma::uword norm_type = 0) {
        //     return arma::cov(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0)
        
        .def("cor", [](const T &matrix, arma::uword norm_type = 0) {
            return arma::cor(matrix, norm_type).eval();
        }, "matrix"_a, "norm_type"_a = 0)
        .def("cor", [](const T &l, const arma::Mat<Type> &r, arma::uword norm_type = 0) {
            return arma::cor(l, r, norm_type).eval();
        }, "l"_a, "r"_a, "norm_type"_a = 0);
        // .def("cor", [](const T &l, const arma::subview<Type> &r, arma::uword norm_type = 0) {
        //     return arma::cor(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0)
        // .def("cor", [](const T &l, const arma::diagview<Type> &r, arma::uword norm_type = 0) {
        //     return arma::cor(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0)
        // .def("cor", [](const T &l, const arma::subview_elem1<Type, arma::umat> &r, arma::uword norm_type = 0) {
        //     return arma::cor(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0)
        // .def("cor", [](const T &l, const arma::subview_elem2<Type, arma::umat, arma::umat> &r, arma::uword norm_type = 0) {
        //     return arma::cor(l, r, norm_type).eval();
        // }, "l"_a, "r"_a, "norm_type"_a = 0);

        expose_stats_real<T>(m);
    }

    template<typename T>
    typename std::enable_if<(arma::is_supported_blas_type<typename T::elem_type>::value && arma::is_arma_cube_type<T>::value)>::type 
    expose_stats(py::module &m) {
        m.def("mean", [](const T &cube) {
            arma::Cube<typename T::elem_type> output;

            if (cube.n_slices == cube.n_elem) {
                output = mean(cube, 2);
            } else if (cube.n_rows == 1) {
                output = mean(cube, 1);
            } else {
                output = mean(cube, 0);
            }
            return output;
        }, "cube"_a)
        .def("mean", [](const T &cube, arma::uword dim) {
            return arma::mean(cube, dim).eval();
        }, "cube"_a, "dim"_a);
    }

    template void expose_stats<arma::mat>(py::module &m);
    template void expose_stats_real<arma::mat>(py::module &m);
    // template void expose_stats<arma::subview<double>>(py::module &m);
    // template void expose_stats<arma::diagview<double>>(py::module &m);
    // template void expose_stats<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_stats<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_stats<arma::fmat>(py::module &m);
    template void expose_stats_real<arma::fmat>(py::module &m);
    // template void expose_stats<arma::subview<float>>(py::module &m);
    // template void expose_stats<arma::diagview<float>>(py::module &m);
    // template void expose_stats<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_stats<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    // #ifndef PYARMA_NO_CX_STATS
    template void expose_stats<arma::cx_mat>(py::module &m);
    template void expose_stats_real<arma::cx_mat>(py::module &m);
    // #endif
    // template void expose_stats<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_stats<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_stats<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_stats<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);

    // #ifndef PYARMA_NO_CX_STATS
    template void expose_stats<arma::cx_fmat>(py::module &m);
    template void expose_stats_real<arma::cx_fmat>(py::module &m);
    // #endif
    // template void expose_stats<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_stats<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_stats<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_stats<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_stats<arma::umat>(py::module &m);
    // template void expose_stats<arma::subview<arma::uword>>(py::module &m);
    // template void expose_stats<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_stats<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_stats<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_stats<arma::imat>(py::module &m);
    // template void expose_stats<arma::subview<arma::sword>>(py::module &m);
    // template void expose_stats<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_stats<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_stats<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);

    template void expose_stats<arma::Cube<double>>(py::module &m);
    // template void expose_stats<arma::subview_cube<double>>(py::module &m);

    template void expose_stats<arma::Cube<float>>(py::module &m);
    // template void expose_stats<arma::subview_cube<float>>(py::module &m);

    template void expose_stats<arma::Cube<arma::cx_double>>(py::module &m);
    // template void expose_stats<arma::subview_cube<arma::cx_double>>(py::module &m);

    template void expose_stats<arma::Cube<arma::cx_float>>(py::module &m);
    // template void expose_stats<arma::subview_cube<arma::cx_float>>(py::module &m);

    template void expose_stats<arma::Cube<arma::uword>>(py::module &m);
    // template void expose_stats<arma::subview_cube<arma::uword>>(py::module &m);

    template void expose_stats<arma::Cube<arma::sword>>(py::module &m);
    // template void expose_stats<arma::subview_cube<arma::sword>>(py::module &m);

    template void expose_hist<arma::mat>(py::module &m);
    // template void expose_hist<arma::subview<double>>(py::module &m);
    // template void expose_hist<arma::diagview<double>>(py::module &m);
    // template void expose_hist<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_hist<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_hist<arma::fmat>(py::module &m);
    // template void expose_hist<arma::subview<float>>(py::module &m);
    // template void expose_hist<arma::diagview<float>>(py::module &m);
    // template void expose_hist<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_hist<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_hist<arma::cx_mat>(py::module &m);
    // template void expose_hist<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_hist<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_hist<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_hist<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);

    template void expose_hist<arma::cx_fmat>(py::module &m);
    // template void expose_hist<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_hist<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_hist<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_hist<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_hist<arma::umat>(py::module &m);
    // template void expose_hist<arma::subview<arma::uword>>(py::module &m);
    // template void expose_hist<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_hist<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_hist<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_hist<arma::imat>(py::module &m);
    // template void expose_hist<arma::subview<arma::sword>>(py::module &m);
    // template void expose_hist<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_hist<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_hist<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);
}
