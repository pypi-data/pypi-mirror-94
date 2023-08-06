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

#pragma once
#include "armadillo"

/* This contains dummy functions that force Armadillo to instantiate certain classes.
   This is done, as some Base<T, Derived> definitions rely on uninstantiated Derived classes.
   These functions must be defined here, as these classes are only
   instantiated (for a given source file) if these functions are compiled on the same file. */
namespace pyarma_junk {
    // arma_cold inline arma::fmat ffoo() {
    //     return arma::fmat();
    // }

    // arma_cold inline arma::cx_fmat cx_ffoo() {
    //     return arma::cx_fmat();
    // }

    arma_cold inline arma::subview_elem1<double, arma::umat> se1foo() {
        arma::mat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.elem(baz);
    }

    arma_cold inline arma::subview_elem1<float, arma::umat> fse1foo() {
        arma::fmat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.elem(baz);
    }

    arma_cold inline arma::subview_elem1<arma::cx_double, arma::umat> cx_se1foo() {
        arma::cx_mat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.elem(baz);
    }

    arma_cold inline arma::subview_elem1<arma::cx_float, arma::umat> cx_fse1foo() {
        arma::cx_fmat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.elem(baz);
    }

    arma_cold inline arma::subview_elem1<arma::uword, arma::umat> use1foo() {
        arma::umat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.elem(baz);
    }

    arma_cold inline arma::subview_elem1<arma::sword, arma::umat> ise1foo() {
        arma::imat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.elem(baz);
    }

    arma_cold inline arma::subview_elem2<double, arma::umat, arma::umat> se2foo() {
        arma::mat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.cols(baz);
    }

    arma_cold inline arma::subview_elem2<float, arma::umat, arma::umat> fse2foo() {
        arma::fmat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.cols(baz);
    }

    arma_cold inline arma::subview_elem2<arma::cx_double, arma::umat, arma::umat> cx_se2foo() {
        arma::cx_mat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.cols(baz);
    }

    arma_cold inline arma::subview_elem2<arma::cx_float, arma::umat, arma::umat> cx_fse2foo() {
        arma::cx_fmat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.cols(baz);
    }

    arma_cold inline arma::subview_elem2<arma::uword, arma::umat, arma::umat> use2foo() {
        arma::umat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.cols(baz);
    }

    arma_cold inline arma::subview_elem2<arma::sword, arma::umat, arma::umat> ise2foo() {
        arma::imat bar(5,5,arma::fill::none);
        arma::uvec baz = { 0, 1, 2 };
        return bar.cols(baz);
    }
}
