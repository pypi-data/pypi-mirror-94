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

namespace py = pybind11;

namespace pyarma {
    class Single_Slice { };

    template<typename T>
    arma::Mat<typename T::elem_type>& get_single_slice(T &cube, std::tuple<Single_Slice, arma::uword> coord) {
        return cube.slice(std::get<1>(coord));
    }

    template<typename T>
    void set_single_slice(T &cube, std::tuple<Single_Slice, arma::uword> coord, arma::Mat<typename T::elem_type> item) {
        cube.slice(std::get<1>(coord)) = item;
    }

    template arma::Mat<double>& get_single_slice<arma::cube>(arma::cube &cube, std::tuple<Single_Slice, arma::uword> coord);
    template arma::Mat<float>& get_single_slice<arma::fcube>(arma::fcube &cube, std::tuple<Single_Slice, arma::uword> coord);
    template arma::Mat<arma::cx_double>& get_single_slice<arma::cx_cube>(arma::cx_cube &cube, std::tuple<Single_Slice, arma::uword> coord);
    template arma::Mat<arma::cx_float>& get_single_slice<arma::cx_fcube>(arma::cx_fcube &cube, std::tuple<Single_Slice, arma::uword> coord);
    template arma::Mat<arma::uword>& get_single_slice<arma::ucube>(arma::ucube &cube, std::tuple<Single_Slice, arma::uword> coord);
    template arma::Mat<arma::sword>& get_single_slice<arma::icube>(arma::icube &cube, std::tuple<Single_Slice, arma::uword> coord);

    template void set_single_slice<arma::cube>(arma::cube &cube, std::tuple<Single_Slice, arma::uword> coord, arma::Mat<double> item);
    template void set_single_slice<arma::fcube>(arma::fcube &cube, std::tuple<Single_Slice, arma::uword> coord, arma::Mat<float> item);
    template void set_single_slice<arma::cx_cube>(arma::cx_cube &cube, std::tuple<Single_Slice, arma::uword> coord, arma::Mat<arma::cx_double> item);
    template void set_single_slice<arma::cx_fcube>(arma::cx_fcube &cube, std::tuple<Single_Slice, arma::uword> coord, arma::Mat<arma::cx_float> item);
    template void set_single_slice<arma::ucube>(arma::ucube &cube, std::tuple<Single_Slice, arma::uword> coord, arma::Mat<arma::uword> item);
    template void set_single_slice<arma::icube>(arma::icube &cube, std::tuple<Single_Slice, arma::uword> coord, arma::Mat<arma::sword> item);
}