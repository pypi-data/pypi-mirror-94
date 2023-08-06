// Copyright 2020-2021 Jason rumengan
// Copyright 2020-2021 Data61/CSIrO
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WArrANTIES Or CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ------------------------------------------------------------------------

#include "pybind11/pybind11.h"
#include "armadillo"

namespace py = pybind11;

namespace pyarma {
    // Expose empty filetype classes as attributes of the module
    arma_cold void expose_filetypes(py::module &m) {
        py::enum_<arma::file_type>(m, "__file_type")
            .value("__auto_detect", arma::auto_detect)
            .value("__arma_binary", arma::arma_binary)
            .value("__arma_ascii", arma::arma_ascii)
            .value("__raw_binary", arma::raw_binary)
            .value("__raw_ascii", arma::raw_ascii)
            .value("__csv_ascii", arma::csv_ascii)
            .value("__pgm_binary", arma::pgm_binary)
            .value("__hdf5_binary", arma::hdf5_binary);

        m.attr("auto_detect") = py::cast(arma::auto_detect);
        m.attr("arma_binary") = py::cast(arma::arma_binary);
        m.attr("arma_ascii") = py::cast(arma::arma_ascii);
        m.attr("raw_binary") = py::cast(arma::raw_binary);
        m.attr("raw_ascii") = py::cast(arma::raw_ascii);
        m.attr("csv_ascii") = py::cast(arma::csv_ascii);
        m.attr("pgm_binary") = py::cast(arma::pgm_binary);
        m.attr("hdf5_binary") = py::cast(arma::hdf5_binary);
    }
}