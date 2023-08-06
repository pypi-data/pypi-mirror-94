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
#include "pybind11/complex.h"
#include "pybind11/iostream.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // TODO: test implicit conversion from submatrices to actual matrices
    /* Defining functions and methods that only work on real types 
       (double, float, and their complex forms)
       This includes inverses and decompositions */
    template<typename T>
    typename std::enable_if<!(arma::is_supported_blas_type<typename T::elem_type>::value)>::type
    expose_decomp(py::module &) { }

    template<typename T>
    typename std::enable_if<arma::is_supported_blas_type<typename T::elem_type>::value>::type
    expose_decomp(py::module &m) {
        using Type = typename T::elem_type;
        using Matrix = arma::Mat<Type>;
        using PodType = typename arma::get_pod_type<Type>::result;
        using CxType = typename std::conditional<arma::is_cx<Type>::value, Type, std::complex<Type>>::type;
        // Expose decompositions
        m.def("chol", [](const T &matrix, std::string layout = "upper") {
            Matrix temp;
            chol(temp, matrix, layout.c_str());
            return temp;
        }, "matrix"_a, "layout"_a = "upper", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("chol", [](Matrix &R, const T &matrix, std::string layout = "upper") {
            return chol(R, matrix, layout.c_str());
        }, "R"_a, "matrix"_a, "layout"_a = "upper", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        .def("eig_sym", [](arma::Mat<PodType> &eigval, const T &matrix) {
            arma::Col<PodType> temp_eigval;
            bool result = eig_sym(temp_eigval, matrix);
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_sym", [](arma::Mat<PodType> &eigval, Matrix &eigvec, const T &matrix) {
            arma::Col<PodType> temp_eigval;
            bool result = eig_sym(temp_eigval, eigvec, matrix);
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "eigvec"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_sym", [](const T &matrix) { 
            arma::Col<PodType> eigval;
            Matrix eigvec;
            eig_sym(eigval, eigvec, matrix);
            return std::make_tuple(arma::Mat<PodType>(eigval), eigvec);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        .def("eig_gen", [](const T &matrix, std::string bal = "nobalance") {
            arma::Col<CxType> eigval;
            arma::Mat<CxType> leigvec, reigvec;
            eig_gen(eigval, leigvec, reigvec, matrix, bal.c_str());
            return std::make_tuple(arma::Mat<CxType>(eigval), leigvec, reigvec);
        }, "matrix"_a, "bal"_a = "nobalance", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_gen", [](arma::Mat<CxType> &eigval, const T &matrix, std::string bal = "nobalance") {
            arma::Col<CxType> temp_eigval;
            bool result = eig_gen(temp_eigval, matrix, bal.c_str());
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "matrix"_a, "bal"_a = "nobalance", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_gen", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &eigvec, const T &matrix, std::string bal = "nobalance") {
            arma::Col<CxType> temp_eigval;
            bool result = eig_gen(temp_eigval, eigvec, matrix, bal.c_str());
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "eigvec"_a, "matrix"_a, "bal"_a = "nobalance", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_gen", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &leigvec, arma::Mat<CxType> &reigvec, const T &matrix, std::string bal = "nobalance") {
            arma::Col<CxType> temp_eigval;
            bool result = eig_gen(temp_eigval, leigvec, reigvec, matrix, bal.c_str());
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "leigvec"_a, "reigvec"_a, "matrix"_a, "bal"_a = "nobalance", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        .def("eig_pair", [](const T &a, const T &b) {
            arma::Col<CxType> eigval;
            arma::Mat<CxType> leigvec, reigvec;
            eig_pair(eigval, leigvec, reigvec, a, b);
            return std::make_tuple(arma::Mat<CxType>(eigval), leigvec, reigvec);
        }, "a"_a, "b"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_pair", [](arma::Mat<CxType> &eigval, const T &a, const T &b) {
            arma::Col<CxType> temp_eigval;
            bool result = eig_pair(temp_eigval, a, b);
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "a"_a, "b"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_pair", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &eigvec, const T &a, const T &b) {
            arma::Col<CxType> temp_eigval;
            bool result = eig_pair(temp_eigval, eigvec, a, b);
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "eigvec"_a, "a"_a, "b"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("eig_pair", [](arma::Mat<CxType> &eigval, arma::Mat<CxType> &leigvec, arma::Mat<CxType> &reigvec, const T &a, const T &b) {
            arma::Col<CxType> temp_eigval;
            bool result = eig_pair(temp_eigval, leigvec, reigvec, a, b);
            eigval = temp_eigval;
            return result;
        }, "eigval"_a, "leigvec"_a, "reigvec"_a, "a"_a, "b"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        .def("hess", [](const T &matrix) {
            Matrix hess_vec, hess_mat;
            hess(hess_vec, hess_mat, matrix);
            return std::make_tuple(hess_vec, hess_mat);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("hess", [](Matrix &hess_mat, const T &matrix) { 
            return hess(hess_mat, matrix); 
        }, "hess_mat"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("hess", [](Matrix &hess_vec, Matrix &hess_mat, const T &matrix) { 
            return hess(hess_vec, hess_mat, matrix); 
        }, "hess_vec"_a, "hess_mat"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("inv", [](const T &matrix) { 
            Matrix inverse;
            inv(inverse, matrix);
            return inverse;     
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("inv", [](Matrix &inverse, const T &matrix) { 
            return inv(inverse, matrix); 
        }, "inverse"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("inv_sympd", [](const T &matrix) {
            Matrix inverse;
            inv_sympd(inverse, matrix);
            return inverse;
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("inv_sympd", [](Matrix &inverse, const T &matrix) { 
            return inv_sympd(inverse, matrix); 
        }, "inverse"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("lu", [](const T &matrix) { 
            Matrix l, u, p;
            lu(l, u, p, matrix); 
            return std::make_tuple(l, u, p);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("lu", [](Matrix &l, Matrix &u, Matrix &p, const T &matrix) { 
            return lu(l, u, p, matrix); 
        }, "l"_a, "u"_a, "p"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("lu", [](Matrix &l, Matrix &u, const T &matrix) { 
            return lu(l, u, matrix); 
        }, "l"_a, "u"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("null", [](const T &matrix) {
            Matrix result;
            null(result, matrix);
            return result;
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("null", [](Matrix &result, const T &matrix) { 
            return null(result, matrix); 
        }, "result"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("null", [](const T &matrix, const PodType &tolerance) {
            Matrix result;
            null(result, matrix, tolerance);
            return result;
        }, "matrix"_a, "tolerance"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("null", [](Matrix &result, const T &matrix, const PodType &tolerance) { 
            return null(result, matrix, tolerance); 
        }, "result"_a, "matrix"_a, "tolerance"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("orth", [](const T &matrix) {
            Matrix result;
            orth(result, matrix);
            return result;
        }, "matrix"_a)
        .def("orth", [](Matrix &result, const T &matrix) { 
            return orth(result, matrix); 
        }, "result"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("orth", [](const T &matrix, const PodType &tolerance) {
            Matrix result;
            orth(result, matrix, tolerance);
            return result;
        }, "matrix"_a, "tolerance"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("orth", [](Matrix &result, const T &matrix, const PodType &tolerance) { 
            return orth(result, matrix, tolerance); 
        }, "result"_a, "matrix"_a, "tolerance"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("pinv", [](const T &matrix) {
            Matrix result;
            pinv(result, matrix);
            return result;
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("pinv", [](Matrix &result, const T &matrix) { 
            return pinv(result, matrix); 
        }, "result"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("pinv", [](const T &matrix, const PodType &tolerance) {
            Matrix result;
            pinv(result, matrix, tolerance);
            return result;
        }, "matrix"_a, "tolerance"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("pinv", [](Matrix &result, const T &matrix, const PodType &tolerance) { 
            return pinv(result, matrix, tolerance); 
        }, "result"_a, "matrix"_a, "tolerance"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("qr", [](const T &matrix) { 
            Matrix q, r;
            qr(q, r, matrix); 
            return std::make_tuple(q, r);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("qr", [](const T &matrix, const std::string &p_type) { 
            Matrix q, r;
            arma::Mat<arma::uword> p;
            qr(q, r, p, matrix, p_type.c_str()); 
            return std::make_tuple(q, r, p);
        }, "matrix"_a, "p_type"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("qr", [](Matrix &q, Matrix &r, const T &matrix) { 
            return qr(q, r, matrix); 
        }, "q"_a, "r"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("qr", [](Matrix &q, Matrix &r, arma::Mat<arma::uword> &p, const T &matrix, const std::string &p_type) { 
            return qr(q, r, p, matrix, p_type.c_str()); 
        }, "q"_a, "r"_a, "p"_a, "matrix"_a, "p_type"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        .def("qr_econ", [](const T &matrix) { 
            Matrix q, r;
            qr_econ(q, r, matrix); 
            return std::make_tuple(q, r);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("qr_econ", [](Matrix &q, Matrix &r, const T &matrix) { 
            return qr_econ(q, r, matrix); 
        }, "q"_a, "r"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("qz", [](const T &a, const T &b, std::string select = "none") {
            Matrix aa, bb, q, z;
            qz(aa, bb, q, z, a, b, select.c_str());
            return std::make_tuple(aa, bb, q, z);
        }, "a"_a, "b"_a, "select"_a = "none", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("qz", [](Matrix &aa, Matrix &bb, Matrix &q, Matrix &z, const T &a, const T &b, std::string select = "none") {
            return qz(aa, bb, q, z, a, b, select.c_str());
        }, "aa"_a, "bb"_a, "q"_a, "z"_a, "a"_a, "b"_a, "select"_a = "none", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("schur", [](const T &matrix) {
            Matrix schur_vec, schur_form;
            schur(schur_vec, schur_form, matrix);
            return std::make_tuple(schur_vec, schur_form);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("schur", [](Matrix &s, const T &matrix) { 
            return schur(s, matrix); 
        }, "s"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("schur", [](Matrix &u, Matrix &s, const T &matrix) { 
            return schur(u, s, matrix); 
        }, "u"_a, "s"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("solve", [](const T &a, const T &b, arma::solve_opts::opts settings = arma::solve_opts::none) {
            Matrix result;
            solve(result, a, b, settings);
            return result;
        }, "a"_a, "b"_a, "settings"_a = arma::solve_opts::none, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("solve", [](Matrix &result, const T &a, const T &b, arma::solve_opts::opts settings = arma::solve_opts::none) {
            return solve(result, a, b, settings);
        }, "result"_a, "a"_a, "b"_a, "settings"_a = arma::solve_opts::none, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        .def("svd", [](const T &matrix) {
            Matrix U, V;
            arma::Col<PodType> s;
            svd(U, s, V, matrix);
            return std::make_tuple(U, arma::Mat<PodType>(s), V);
        }, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("svd", [](arma::Mat<PodType> &s, const T &matrix) { 
            arma::Col<PodType> temp_s;
            bool result = svd(temp_s, matrix);
            s = temp_s; 
            return result;
        }, "s"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("svd", [](Matrix &U, arma::Mat<PodType> &s, Matrix &V, const T &matrix) { 
            arma::Col<PodType> temp_s;
            bool result = svd(U, temp_s, V, matrix); 
            s = temp_s;
            return result;
        }, "U"_a, "s"_a, "V"_a, "matrix"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        
        .def("svd_econ", [](const T &matrix, std::string mode = "both") {
            Matrix U, V;
            arma::Col<PodType> s;
            svd_econ(U, s, V, matrix, mode.c_str());
            return std::make_tuple(U, arma::Mat<PodType>(s), V);
        }, "matrix"_a, "mode"_a = "both", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("svd_econ", [](Matrix &U, arma::Mat<PodType> &s, Matrix &V, const T &matrix, std::string mode = "both") {
            arma::Col<PodType> temp_s;
            bool result = svd_econ(U, temp_s, V, matrix, mode.c_str());
            s = temp_s;
            return result;
        }, "U"_a, "s"_a, "V"_a, "matrix"_a, "mode"_a = "both", py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())

        .def("syl", [](const T &a, const T &b, const T &c) {
            Matrix X;
            syl(X, a, b, c);
            return X;
        }, "a"_a, "b"_a, "c"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
        .def("syl", [](Matrix &X, const T &a, const T &b, const T &c) { 
            return syl(X, a, b, c); 
        }, "X"_a, "a"_a, "b"_a, "c"_a, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>());
    }

    template void expose_decomp<arma::mat>(py::module &m);
    // template void expose_decomp<arma::subview<double>>(py::module &m);
    // template void expose_decomp<arma::diagview<double>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<double, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<double, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<float>>(py::module &m);
    // template void expose_decomp<arma::subview<float>>(py::module &m);
    // template void expose_decomp<arma::diagview<float>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<float, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<float, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<arma::cx_double>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::cx_double>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::cx_double>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::cx_double, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::cx_double, arma::umat, arma::umat>>(py::module &m);
 
    template void expose_decomp<arma::Mat<arma::cx_float>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::cx_float>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::cx_float>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::cx_float, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::cx_float, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<arma::uword>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::uword>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::uword>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::uword, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::uword, arma::umat, arma::umat>>(py::module &m);

    template void expose_decomp<arma::Mat<arma::sword>>(py::module &m);
    // template void expose_decomp<arma::subview<arma::sword>>(py::module &m);
    // template void expose_decomp<arma::diagview<arma::sword>>(py::module &m);
    // template void expose_decomp<arma::subview_elem1<arma::sword, arma::umat>>(py::module &m);
    // template void expose_decomp<arma::subview_elem2<arma::sword, arma::umat, arma::umat>>(py::module &m);
}