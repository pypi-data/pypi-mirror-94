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
#include "pybind11/stl.h"
#include "pybind11/complex.h"
#include <iostream>
// // #include "force_inst.hpp"
#include "armadillo"
#include "classes/file_types.hpp"
#include "classes/fill_types.hpp"
#include "classes/solve_opts.hpp"
#include "base.hpp"
#include "basecube.hpp"
#include "diagview.hpp"
#include "subview.hpp"
#include "matrix.hpp"
#include "generators.hpp"
#include "subview_elem1.hpp"
#include "subview_elem2.hpp"
#include "subview_cube.hpp"
#include "cube.hpp"
#include "classes/sizecube.hpp"
#include "classes/sizemat.hpp"
#include "classes/datum.hpp"
#include "classes/wall_clock.hpp"
#include "classes/running_stat.hpp"
#include "classes/running_stat_vec.hpp"
#include "classes/seed_mode.hpp"
#include "classes/dist_mode.hpp"
#include "classes/index_class.hpp"
#include "classes/distr_param.hpp"
#include "libraries.hpp"
#include "version.hpp"

namespace py = pybind11;
using namespace std;
using namespace arma;
using namespace pyarma;
using namespace pybind11::literals;

/* Versions must be defined beforehand
   (see https://stackoverflow.com/a/4891102) */
const unsigned int pyarma_version::major;
const unsigned int pyarma_version::minor;
const unsigned int pyarma_version::patch;

PYBIND11_MODULE(pyarma, m) {
    // Ensure only embedded versions are used
    #ifndef ARMA_TRIPWIRE
    static_assert(false, "The embedded version of Armadillo could not be used.");
    #endif
    #ifndef PYBIND11_TRIPWIRE
    static_assert(false, "The embedded version of pybind11 could not be used.");
    #endif
    
    m.doc() = (string("Python library for linear algebra and scientific computing") + string("\n\nPyArmadillo version: ") + pyarma_version::as_string() \
    + string("\n\nArmadillo version: ") + arma::arma_version::as_string() + string("\n\npybind11 version: ") \
    + to_string(PYBIND11_VERSION_MAJOR) + "." + to_string(PYBIND11_VERSION_MINOR) + "." + to_string(PYBIND11_VERSION_PATCH)) \
    + "\n\nSee the following webpage https://pyarma.sourceforge.io for API documentation and more examples";

    // Add libraries used
    string mkl = PYARMA_MKL;
    string oblas = PYARMA_OPENBLAS;
    string atlas = PYARMA_ATLAS;
    string blas = PYARMA_BLAS;
    string lapack = PYARMA_LAPACK;
    string fblas = PYARMA_FLEXIBLAS;
    string hdf5 = PYARMA_HDF5;
    string arpack = PYARMA_ARPACK;
    string superlu = PYARMA_SUPERLU;
    string accel = PYARMA_ACCELERATE;
    string libraries = "PyArma library status on install:\n\n";
    if(mkl.empty()) {
        libraries.append("MKL is not used." "\n");
    } else {
        libraries.append("MKL is used and is located at " + mkl + "\n");
    }
    #ifndef PYARMA_PRECOMPILED_OPENBLAS
    if(oblas.empty() || !(accel.empty())) {
        libraries.append("OpenBLAS is not used." "\n");
    } else {
        libraries.append("OpenBLAS is used and is located at " + oblas + "\n");
    }
    #else
    libraries.append("A precompiled version of OpenBLAS is used.\n");
    #endif
    if(atlas.empty() || !(oblas.empty())) {
        libraries.append("ATLAS is not used." "\n");
    } else {
        libraries.append("ATLAS is used and is located at " + atlas + "\n");
    }
    if(blas.empty() || !(oblas.empty())) {
        libraries.append("BLAS is not used." "\n");
    } else {
        libraries.append("BLAS is used and is located at " + blas + "\n");
    }
    #ifndef PYARMA_PRECOMPILED_OPENBLAS
    if(lapack.empty()) {
        libraries.append("LAPACK is not used." "\n");
    } else {
        libraries.append("LAPACK is used and is located at " + lapack + "\n");
    }
    #else
    libraries.append("A precompiled version of OpenBLAS is used. The precompiled version includes LAPACK.\n");
    #endif
    if(fblas.empty()) {
        libraries.append("FlexiBLAS is not used.""\n");
    } else {
        libraries.append("FlexiBLAS is used and is located at " + fblas + "\n");
    }
    #ifndef PYARMA_PRECOMPILED_HDF5
    if(hdf5.empty() || hdf5 == "HDF5_hdf5_LIBRARY-NOTFOUND") {
        libraries.append("HDF5 is not used." "\n");
    } else {
        libraries.append("HDF5 is used and is located at " + hdf5 + "\n");
    }
    #else
    libraries.append("A precompiled version of HDF5 is used.\n");
    #endif
    if(arpack.empty() || arpack == "ARPACK_LIBRARY-NOTFOUND") {
        libraries.append("ARPACK is not used." "\n");
    } else {
        libraries.append("ARPACK is used and is located at " + arpack + "\n");
    }
    if(superlu.empty() || superlu == "SuperLU_LIBRARY-NOTFOUND") {
        libraries.append("SuperLU is not used." "\n");
    } else {
        libraries.append("SuperLU is used and is located at " + superlu + "\n");
    }
    if(accel.empty()) {
        libraries.append("Accelerate is not used." "\n");
    } else {
        libraries.append("Accelerate is used." "\n");
    }

    m.def("libraries", [libraries]() { py::print(libraries, "end"_a=""); });

    // Expose versioning
    py::class_<pyarma_version>(m, "pyarma_version")
        .def_readonly_static("major", &pyarma_version::major)
        .def_readonly_static("minor", &pyarma_version::minor)
        .def_readonly_static("patch", &pyarma_version::patch)
        .def("as_string", &pyarma_version::as_string);

    // Defining empty classes and functions    
    expose_diag(m);
    expose_single_slice(m);
    expose_fill_types(m);
    expose_filetypes(m);
    expose_solve_opts(m);
    expose_head_tail(m);
    expose_distr_param(m);
    expose_generators(m);
    expose_const(m);
    expose_size(m);
    define_size(m);
    expose_seed_mode(m);
    expose_dist_mode(m);

    // Expose the wall clock class
    expose_wall_clock(m);

    // Expose running_stat classes
    expose_running_stat<double>(m, "running_stat");
    expose_running_stat<float>(m, "frunning_stat");
    expose_running_stat<cx_double>(m, "cx_running_stat");
    expose_running_stat<cx_float>(m, "cx_frunning_stat");
    expose_running_stat_vec<mat>(m, "running_stat_vec");
    expose_running_stat_vec<fmat>(m, "frunning_stat_vec");
    expose_running_stat_vec<cx_mat>(m, "cx_running_stat_vec");
    expose_running_stat_vec<cx_fmat>(m, "cx_frunning_stat_vec");

    // Expose GMM
    // expose_gmm(m);

    // Expose seed setters
    py::class_<arma_rng>(m, "pyarma_rng").def("set_seed", &arma_rng::set_seed)
        .def("set_seed_random", &arma_rng::set_seed_random);

    // Defining mat class
    declare_base<double, mat>(m, "base_mat");
    declare_base<double, subview<double>>(m, "__base_subview_mat");
    declare_base<double, diagview<double>>(m, "__base_diagview_mat");
    declare_base<double, subview_elem1<double, umat>>(m, "__base_subview_elem1_mat");
    declare_base<double, subview_elem2<double, umat, umat>>(m, "__base_subview_elem2_mat");

    declare_subview<double>(m, "subview_mat");
    declare_diagview<double>(m, "diagview_mat");
    expose_matrix<double>(m, "mat");
    declare_subview_elem1<double>(m, "subview_elem1_mat");
    declare_subview_elem2<double>(m, "subview_elem2_mat");

    // Defining fmat class
    declare_base<float, fmat>(m, "base_fmat");
    declare_base<float, subview<float>>(m, "__base_subview_fmat");
    declare_base<float, diagview<float>>(m, "__base_diagview_fmat");
    declare_base<float, subview_elem1<float, umat>>(m, "__base_subview_elem1_fmat");
    declare_base<float, subview_elem2<float, umat, umat>>(m, "__base_subview_elem2_fmat");

    declare_subview<float>(m, "subview_fmat");
    declare_diagview<float>(m, "diagview_fmat");
    expose_matrix<float>(m, "fmat");
    declare_subview_elem1<float>(m, "subview_elem1_fmat");
    declare_subview_elem2<float>(m, "subview_elem2_fmat");

    // Defining cx_mat class
    declare_base<cx_double, cx_mat>(m, "base_cx_mat");
    declare_base<cx_double, subview<cx_double>>(m, "__base_subview_cx_mat");
    declare_base<cx_double, diagview<cx_double>>(m, "__base_diagview_cx_mat");
    declare_base<cx_double, subview_elem1<cx_double, umat>>(m, "__base_subview_elem1_cx_mat");
    declare_base<cx_double, subview_elem2<cx_double, umat, umat>>(m, "__base_subview_elem2_cx_mat");

    declare_subview<cx_double>(m, "subview_cx_mat");
    declare_diagview<cx_double>(m, "diagview_cx_mat");
    expose_matrix<cx_double>(m, "cx_mat");
    declare_subview_elem1<cx_double>(m, "subview_elem1_cx_mat");
    declare_subview_elem2<cx_double>(m, "subview_elem2_cx_mat");

    // Defining cx_fmat class
    declare_base<cx_float, cx_fmat>(m, "base_cx_fmat");
    declare_base<cx_float, subview<cx_float>>(m, "__base_subview_cx_fmat");
    declare_base<cx_float, diagview<cx_float>>(m, "__base_diagview_cx_fmat");
    declare_base<cx_float, subview_elem1<cx_float, umat>>(m, "__base_subview_elem1_cx_fmat");
    declare_base<cx_float, subview_elem2<cx_float, umat, umat>>(m, "__base_subview_elem2_cx_fmat");

    declare_subview<cx_float>(m, "subview_cx_fmat");
    declare_diagview<cx_float>(m, "diagview_cx_fmat");
    expose_matrix<cx_float>(m, "cx_fmat");
    declare_subview_elem1<cx_float>(m, "subview_elem1_cx_fmat");
    declare_subview_elem2<cx_float>(m, "subview_elem2_cx_fmat");

    // Defining umat class
    declare_base<uword, umat>(m, "base_umat");
    declare_base<uword, subview<uword>>(m, "__base_subview_umat");
    declare_base<uword, diagview<uword>>(m, "__base_diagview_umat");
    declare_base<uword, subview_elem1<uword, umat>>(m, "__base_subview_elem1_umat");
    declare_base<uword, subview_elem2<uword, umat, umat>>(m, "__base_subview_elem2_umat");

    declare_subview<uword>(m, "subview_umat");
    declare_diagview<uword>(m, "diagview_umat");
    expose_matrix<uword>(m, "umat");
    declare_subview_elem1<uword>(m, "subview_elem1_umat");
    declare_subview_elem2<uword>(m, "subview_elem2_umat");

    // Defining imat class
    declare_base<sword, imat>(m, "base_imat");
    declare_base<sword, subview<sword>>(m, "__base_subview_imat");
    declare_base<sword, diagview<sword>>(m, "__base_diagview_imat");
    declare_base<sword, subview_elem1<sword, umat>>(m, "__base_subview_elem1_imat");
    declare_base<sword, subview_elem2<sword, umat, umat>>(m, "__base_subview_elem2_imat");

    declare_subview<sword>(m, "subview_imat");
    declare_diagview<sword>(m, "diagview_imat");
    expose_matrix<sword>(m, "imat");
    declare_subview_elem1<sword>(m, "subview_elem1_imat");
    declare_subview_elem2<sword>(m, "subview_elem2_imat");

    // Defining cube class
    cube_declare_base<double, cube>(m, "base_cube");
    cube_declare_base<double, subview_cube<double>>(m, "__base_subview_cube");
    define_subview_cube<double>(m, "subview_cube");
    expose_cube<double>(m, "cube");

    // Defining cx_cube class
    cube_declare_base<cx_double, cx_cube>(m, "base_cx_cube");
    cube_declare_base<cx_double, subview_cube<cx_double>>(m, "__base_subview_cx_cube");
    define_subview_cube<cx_double>(m, "subview_cx_cube");
    expose_cube<cx_double>(m, "cx_cube");

    // Defining ucube class
    cube_declare_base<uword, ucube>(m, "base_ucube");
    cube_declare_base<uword, subview_cube<uword>>(m, "__base_subview_ucube");
    define_subview_cube<uword>(m, "subview_ucube");
    expose_cube<uword>(m, "ucube");

    // Defining fcube class
    cube_declare_base<float, fcube>(m, "base_fcube");
    cube_declare_base<float, subview_cube<float>>(m, "__base_subview_fcube");
    define_subview_cube<float>(m, "subview_fcube");
    expose_cube<float>(m, "fcube");

    // Defining cx_fcube class
    cube_declare_base<cx_float, cx_fcube>(m, "base_cx_fcube");
    cube_declare_base<cx_float, subview_cube<cx_float>>(m, "__base_subview_cx_fcube");
    define_subview_cube<cx_float>(m, "subview_cx_fcube");
    expose_cube<cx_float>(m, "cx_fcube");

    // Defining icube class
    cube_declare_base<sword, icube>(m, "base_icube");
    cube_declare_base<sword, subview_cube<sword>>(m, "__base_subview_icube");
    define_subview_cube<sword>(m, "subview_icube");
    expose_cube<sword>(m, "icube");

    // Allowing implicit conversions/copies from subcube views to cubes
    py::implicitly_convertible<subview_cube<double>, Cube<double>>();
    py::implicitly_convertible<subview_cube<cx_double>, Cube<cx_double>>();
    py::implicitly_convertible<subview_cube<uword>, Cube<uword>>();
    py::implicitly_convertible<subview_cube<float>, Cube<float>>();
    py::implicitly_convertible<subview_cube<cx_float>, Cube<cx_float>>();
    py::implicitly_convertible<subview_cube<sword>, Cube<sword>>();

    // py::class_<vec> vec = declare_col<double>(m, "vec");
    // py::class_<fvec> fvec = declare_col<float>(m, "fvec");
    // py::class_<cx_vec> cx_vec = declare_col<cx_double>(m, "cx_vec");
    // py::class_<cx_fvec> cx_fvec = declare_col<cx_float>(m, "cx_fvec");
    // py::class_<uword> uvec = declare_col<uword>(m, "uvec");
    // py::class_<sword> ivec = declare_col<sword>(m, "ivec");
    // py::class_<rowvec> rowvec = declare_row<double>(m, "rowvec");
    // py::class_<frowvec> frowvec = declare_row<float>(m, "frowvec");
    // py::class_<cx_rowvec> cx_rowvec = declare_row<cx_double>(m, "cx_rowvec");
    // py::class_<cx_fvec> cx_frowvec = declare_row<cx_float>(m, "cx_frowvec");
    // py::class_<uword> urowvec = declare_row<uword>(m, "urowvec");
    // py::class_<sword> irowvec = declare_row<sword>(m, "irowvec");

    // Allowing implicit conversions/copies from submatrix views to matrices
    py::implicitly_convertible<subview<double>, mat>();
    py::implicitly_convertible<diagview<double>, mat>();
    py::implicitly_convertible<subview_elem1<double, umat>, mat>();
    py::implicitly_convertible<subview_elem2<double, umat, umat>, mat>();
    
    py::implicitly_convertible<subview<cx_double>, cx_mat>();
    py::implicitly_convertible<diagview<cx_double>, cx_mat>();
    py::implicitly_convertible<subview_elem1<cx_double, umat>, cx_mat>();
    py::implicitly_convertible<subview_elem2<cx_double, umat, umat>, cx_mat>();
    
    py::implicitly_convertible<subview<uword>, umat>();
    py::implicitly_convertible<diagview<uword>, umat>();
    py::implicitly_convertible<subview_elem1<uword, umat>, umat>();
    py::implicitly_convertible<subview_elem2<uword, umat, umat>, umat>();
    
    py::implicitly_convertible<subview<float>, fmat>();
    py::implicitly_convertible<diagview<float>, fmat>();
    py::implicitly_convertible<subview_elem1<float, umat>, fmat>();
    py::implicitly_convertible<subview_elem2<float, umat, umat>, fmat>();
    
    py::implicitly_convertible<subview<cx_float>, cx_fmat>();
    py::implicitly_convertible<diagview<cx_float>, cx_fmat>();
    py::implicitly_convertible<subview_elem1<cx_float, umat>, cx_fmat>();
    py::implicitly_convertible<subview_elem2<cx_float, umat, umat>, cx_fmat>();
    
    py::implicitly_convertible<subview<sword>, imat>();
    py::implicitly_convertible<diagview<sword>, imat>();
    py::implicitly_convertible<subview_elem1<sword, umat>, imat>();
    py::implicitly_convertible<subview_elem2<sword, umat, umat>, imat>();
    
    /* Allowing implicit conversions 
       from integers to floating-point numbers,
       from real numbers to complex numbers,
       and from single-precision floating-point to double-precision */
    py::implicitly_convertible<umat, mat>();
    py::implicitly_convertible<umat, fmat>();
    py::implicitly_convertible<imat, mat>();
    py::implicitly_convertible<imat, fmat>();
    py::implicitly_convertible<fmat, mat>();
    py::implicitly_convertible<mat, cx_mat>();
    py::implicitly_convertible<fmat, cx_mat>();
    py::implicitly_convertible<fmat, cx_fmat>();

    // /* Allowing implicit conversions from scalars to matrices and cubes,
    //    useful for setting 1x1 submatrices/cubes using scalars */
    // py::implicitly_convertible<double, mat>();
    // py::implicitly_convertible<float, fmat>();
    // py::implicitly_convertible<cx_double, cx_mat>();
    // py::implicitly_convertible<cx_float, cx_fmat>();
    // py::implicitly_convertible<uword, umat>();
    // py::implicitly_convertible<sword, imat>();

    // py::implicitly_convertible<double, cube>();
    // py::implicitly_convertible<float, fcube>();
    // py::implicitly_convertible<cx_double, cx_cube>();
    // py::implicitly_convertible<cx_float, cx_fcube>();
    // py::implicitly_convertible<uword, ucube>();
    // py::implicitly_convertible<sword, icube>();
}
