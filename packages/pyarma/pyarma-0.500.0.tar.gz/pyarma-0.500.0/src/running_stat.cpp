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
#include "pybind11/complex.h"
#include "pybind11/iostream.h"
#include "armadillo"

namespace py = pybind11;
using namespace pybind11::literals;

template<typename... Args>
using overload_cast_ = pybind11::detail::overload_cast_impl<Args...>;

namespace pyarma {
    // Expose running_stat
    template<typename T>
    void expose_running_stat(py::module &m, const std::string typestr) {
        using PodType = typename arma::get_pod_type<T>::result;

        py::class_<arma::running_stat<T>>(m, typestr.c_str())
            .def(py::init(), py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("__call__", overload_cast_<const PodType>()(&arma::running_stat<T>::operator()), py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("__call__", overload_cast_<const std::complex<PodType> &>()(&arma::running_stat<T>::operator()), py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("min", &arma::running_stat<T>::min, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("max", &arma::running_stat<T>::max, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("spread", &arma::running_stat<T>::range, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("mean", &arma::running_stat<T>::mean, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("var", &arma::running_stat<T>::var, "norm_type"_a = 0, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("stddev", &arma::running_stat<T>::stddev, "norm_type"_a = 0, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("reset", &arma::running_stat<T>::reset, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>())
            .def("count", &arma::running_stat<T>::count, py::call_guard<py::scoped_estream_redirect, py::scoped_ostream_redirect>());
    }

    template void expose_running_stat<double>(py::module &m, const std::string typestr);
    template void expose_running_stat<float>(py::module &m, const std::string typestr);
    template void expose_running_stat<arma::cx_double>(py::module &m, const std::string typestr);
    template void expose_running_stat<arma::cx_float>(py::module &m, const std::string typestr);
}