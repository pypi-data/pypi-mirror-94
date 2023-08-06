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
#include "pybind11/complex.h"
#include "functions/fn_extremum.hpp"
#include "functions/fn_trans.hpp"
#include "functions/fn_additive.hpp"
#include "functions/fn_find.hpp"
#include "functions/fn_rep.hpp"
#include "functions/fn_trimat.hpp"
#include "functions/fn_rev.hpp"
#include "functions/fn_sort.hpp"
#include "functions/fn_apeq.hpp"
#include "functions/fn_scalar.hpp"
#include "functions/fn_dot.hpp"
#include "functions/fn_diff.hpp"
#include "functions/fn_intersect.hpp"
#include "functions/fn_trace.hpp"
#include "functions/fn_unique.hpp"
#include "functions/fn_size.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace pyarma {
    // Expose matrix standalone functions
    template<typename T>
    void expose_matrix_functions(py::module &m) {
        using Class = arma::Mat<T>;
        using PodType = typename arma::get_pod_type<T>::result;
        expose_extremum<T>(m);
        expose_trans<T>(m);
        expose_additive<T>(m);
        expose_find<T>(m);
        expose_rep<T>(m);
        expose_trimat<T>(m);
        expose_rev<T>(m);
        expose_sort<T>(m);
        expose_apeq<T>(m);
        expose_scalar<T>(m);
        expose_dot<T>(m);
        expose_diff<T>(m);
        expose_intersect<T>(m);
        expose_trace<T>(m);
        expose_unique<T>(m);
        expose_resizing<T>(m);

        m.def("abs", [](const Class &matrix) { return abs(matrix).eval(); })

        .def("affmul", [](const Class &a, const Class &b) { return arma::affmul(a, b); })

        .def("all", [](const Class &matrix) {
            arma::umat output;

            if (matrix.n_elem == 0) {
                output.set_size(1, 1);
                output[0] = 1;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = all(tmp);
            } else {
                output = all(matrix, 0);
            }
            return output;
        }, "matrix"_a)
        .def("all", [](const Class &matrix, const arma::uword &dim) { return all(matrix, dim).eval(); })

        .def("any", [](const Class &matrix) {
            arma::umat output;

            if (matrix.n_elem == 0) {
                output.set_size(1, 1);
                output[0] = 0;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = any(tmp);
            } else {
                output = any(matrix, 0);
            }
            return output;
        })
        .def("any", [](const Class &matrix, const arma::uword &dim) { return any(matrix, dim).eval(); })

        .def("arg", [](const Class &matrix) { return arg(matrix).eval(); })

        .def("cross", [](const Class &a, const Class &b) { return cross(a, b).eval(); })

        .def("diagmat", [](const Class &matrix, arma::sword k = 0) { 
            return arma::diagmat(matrix, k).eval();
        }, "matrix"_a, "k"_a = 0)

        .def("diagvec", [](const Class &matrix, arma::sword k = 0) {
            return arma::diagvec(matrix, k).eval();
        }, "matrix"_a, "k"_a = 0)

        .def("eps", [](const T scalar) { return arma::eps(scalar); })
        .def("eps", [](const Class &matrix) { return arma::eps(matrix).eval(); })

        .def("ind2sub", [](const arma::SizeMat &size, arma::uword index) { return arma::umat(ind2sub(size, index)); })
        .def("ind2sub", [](const arma::SizeMat &size, arma::umat indices) { return ind2sub(size, indices); })

        .def("kron", [](const Class &a, const Class &b) { return kron(a, b).eval(); })

        .def("nonzeros", [](const Class &matrix) { return nonzeros(matrix).eval(); })

        .def("prod", [](const Class &matrix, const arma::uword &dim) { return prod(matrix, dim).eval(); }, "matrix"_a, "dim"_a)
        .def("prod", [](const Class &matrix) { 
            Class output;

            if (matrix.n_elem == 0) {
                output.set_size(1, 1);
                output[0] = 1;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = prod(tmp);
            } else {
                output = prod(matrix, 0);
            }
            return output;
        })

        .def("shift", [](const Class &matrix, arma::sword positions, const arma::uword &dim) {
            return shift(matrix, positions, dim).eval();
        }, "matrix"_a, "positions"_a, "dim"_a)
        .def("shift", [](const Class &matrix, arma::sword positions) {
            Class output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = shift(tmp, positions);
                if (matrix.is_rowvec()) {
                    output = output.t();
                }
            } else {
                output = arma::shift(matrix, positions, 0);
            }
            return output;
        })

        .def("shuffle", [](const Class &matrix, const arma::uword &dim) {
            return shuffle(matrix, dim).eval();
        }, "matrix"_a, "dim"_a)
        .def("shuffle", [](const Class &matrix) {
            Class output;

            if (matrix.n_elem == 0) {
                output = matrix;
            } else if (matrix.is_vec()) {
                Class tmp(const_cast<T*>(matrix.memptr()), matrix.n_elem, 1, false, true);
                output = shuffle(tmp);
                if (matrix.is_rowvec()) {
                    output = output.t();
                }
            } else {
                output = arma::shuffle(matrix, 0);
            }
            return output;
        })

        .def("size", [](const Class &matrix) { return arma::size(matrix); })
        .def("size", [](const arma::uword &rows, const arma::uword &cols) { return arma::size(rows, cols); })

        .def("sub2ind", [](const arma::SizeMat &size, const arma::uword &row, const arma::uword &col) { return sub2ind(size, row, col); })
        .def("sub2ind", [](const arma::SizeMat &size, arma::umat indices) { return arma::umat(sub2ind(size, indices)); })

        .def("trapz", [](const Class &x, const Class &y) {
            Class output;

            if (y.is_rowvec()) {
                output = trapz(x, y, 1);
            } else {
                output = trapz(x, y, 0);
            }
            return output;
        }, "x"_a, "y"_a)
        .def("trapz", [](const Class &x, const Class &y, const arma::uword &dim) {
            return trapz(x, y, dim).eval();
        }, "x"_a, "y"_a, "dim"_a)
        .def("trapz", [](const Class &y) {
            Class output;

            if (y.is_rowvec()) {
                output = trapz(y, 1);
            } else {
                output = trapz(y, 0);
            }
            return output;
        }, "y"_a)
        .def("trapz", [](const Class &y, const arma::uword &dim) {
            return trapz(y, dim).eval();
        }, "y"_a, "dim"_a)

        .def("vectorise", [](const Class &matrix, const arma::uword &dim = 0) {
            return vectorise(matrix, dim).eval();
        }, "matrix"_a, "dim"_a = 0)
        
        // Toeplitz matrix generator
        .def("toeplitz", [](const Class &a) { return toeplitz(a).eval(); })
        .def("toeplitz", [](const Class &a, const Class &b) { return toeplitz(a, b).eval(); })
        .def("circ_toeplitz", [](const Class &a) { return circ_toeplitz(a).eval(); })

        // Custom iterators
        .def("iterator", [](const Class &matrix, const arma::uword begin_elem = 0, const arma::sword end_elem = -1) {
            arma::uword true_end_elem;
            // If the user does not specify an ending index, use the last element
            if (end_elem == -1) { 
                true_end_elem = matrix.n_elem - 1; 
            } else {
                true_end_elem = arma::uword(end_elem);
            }
            if (begin_elem >= matrix.n_elem) {
                throw py::value_error("Starting element cannot be greater than or equal to the number of elements");
            }
            if (true_end_elem >= matrix.n_elem) {
                throw py::value_error("Ending element cannot be greater than or equal to the number of elements");
            }
            return py::make_iterator(matrix.begin()+begin_elem, matrix.begin()+true_end_elem+1);
        }, "matrix"_a, "begin_elem"_a = 0, "end_elem"_a = -1, py::keep_alive<0,1>())
        .def("col_iter", [](const Class &matrix, const arma::uword begin_col = 0, const arma::sword end_col = -1) {
            arma::uword true_end_col;
            // If the user does not specify an ending index, use the last column
            if (end_col == -1) { 
                true_end_col = matrix.n_cols - 1; 
            } else {
                true_end_col = arma::uword(end_col);
            }
            return py::make_iterator(matrix.begin_col(begin_col), matrix.end_col(true_end_col));
        }, "matrix"_a, "begin_col"_a = 0, "end_col"_a = -1, py::keep_alive<0,1>())
        .def("row_iter", [](Class &matrix, const arma::uword begin_row = 0, const arma::sword end_row = -1) {
            arma::uword true_end_row;
            // If the user does not specify an ending index, use the last row
            if (end_row == -1) { 
                true_end_row = matrix.n_rows - 1; 
            } else {
                true_end_row = arma::uword(end_row);
            }
            return py::make_iterator(matrix.begin_row(begin_row), matrix.end_row(true_end_row));
        }, "matrix"_a, "begin_row"_a = 0, "end_row"_a = -1, py::keep_alive<0,1>());
    }

    template void expose_matrix_functions<double>(py::module &m);
    template void expose_matrix_functions<float>(py::module &m);
    template void expose_matrix_functions<arma::uword>(py::module &m);
    template void expose_matrix_functions<arma::sword>(py::module &m);
    template void expose_matrix_functions<arma::cx_double>(py::module &m);
    template void expose_matrix_functions<arma::cx_float>(py::module &m);
}
        