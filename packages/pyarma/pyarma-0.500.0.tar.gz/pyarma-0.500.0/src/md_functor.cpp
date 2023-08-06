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
#include "pybind11/complex.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose functor-accepting methods (i.e. imbue())
    template<typename T>
    void expose_functor(py::class_<arma::Mat<T>, arma::Base<T, arma::Mat<T>>> &py_class) {
        using Class = arma::Mat<T>;
        // Modified versions of imbue, transform and for_each that use Python function objects
        py_class.def("imbue", [](Class &matrix, py::function functor) {
                T* out_mem = matrix.memptr();
                
                const arma::uword N = matrix.n_elem;
                
                arma::uword ii, jj;
                
                for (ii=0, jj=1; jj < N; ii+=2, jj+=2) {
                    out_mem[ii] = functor().cast<T>();
                    out_mem[jj] = functor().cast<T>();
                }
                
                if (ii < N) {
                    out_mem[ii] = functor().cast<T>();
                }
            })
            .def("transform", [](Class &matrix, py::function functor) {
                T* out_mem = matrix.memptr();
  
                const arma::uword N = matrix.n_elem;
                
                arma::uword ii, jj;
                
                for (ii=0, jj=1; jj < N; ii+=2, jj+=2) {
                    // Functor return value must be stored before casting
                    py::object tmp_ii_in = functor(out_mem[ii]);
                    py::object tmp_jj_in = functor(out_mem[jj]);
                    
                    out_mem[ii] = tmp_ii_in.cast<T>();
                    out_mem[jj] = tmp_jj_in.cast<T>();
                }
                
                if(ii < N) {
                    py::object tmp_ii_in = functor(out_mem[ii]);
                    out_mem[ii] = tmp_ii_in.cast<T>();
                }
            })
            /* As Python functions aren't side-effecting by exposeault,
               the matrix's values won't change.
               .for_each() is a const version of .transform(). */
            .def("for_each", [](Class &matrix, py::function functor) {
                T* data = matrix.memptr();
  
                const arma::uword N = matrix.n_elem;
                
                arma::uword ii, jj;
                
                for(ii=0, jj=1; jj < N; ii+=2, jj+=2) {
                    functor(data[ii]);
                    functor(data[jj]);
                }
                
                if(ii < N) {
                    functor(data[ii]);
                }
            });
    }

    template void expose_functor<double>(py::class_<arma::Mat<double>, arma::Base<double, arma::Mat<double>>> &py_class);
    template void expose_functor<float>(py::class_<arma::Mat<float>, arma::Base<float, arma::Mat<float>>> &py_class);
    template void expose_functor<arma::cx_double>(py::class_<arma::Mat<arma::cx_double>, arma::Base<arma::cx_double, arma::Mat<arma::cx_double>>> &py_class);
    template void expose_functor<arma::cx_float>(py::class_<arma::Mat<arma::cx_float>, arma::Base<arma::cx_float, arma::Mat<arma::cx_float>>> &py_class);
    template void expose_functor<arma::uword>(py::class_<arma::Mat<arma::uword>, arma::Base<arma::uword, arma::Mat<arma::uword>>> &py_class);
    template void expose_functor<arma::sword>(py::class_<arma::Mat<arma::sword>, arma::Base<arma::sword, arma::Mat<arma::sword>>> &py_class);
}