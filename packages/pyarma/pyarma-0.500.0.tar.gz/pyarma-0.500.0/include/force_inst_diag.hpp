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
#include "armadillo"

/* This contains dummy functions that force Armadillo to instantiate certain classes.
   This is done, as some Base<T, Derived> definitions rely on uninstantiated Derived classes.
   These functions must be defined here, as these classes are only
   instantiated (for a given source file) if these functions are compiled on the same file. */
namespace pyarma_junk {
    arma_cold inline arma::diagview<double> dfoo() { 
        arma::mat bar(5,5,arma::fill::none);
        return bar.diag();
    }
    
    arma_cold inline arma::diagview<arma::uword> dufoo() { 
        arma::umat bar(5,5,arma::fill::none);
        return bar.diag();
    }

    arma_cold inline arma::diagview<arma::sword> difoo() { 
        arma::imat bar(5,5,arma::fill::none);
        return bar.diag();
    }
    
    arma_cold inline arma::diagview<float> fdfoo() { 
        arma::fmat bar(5,5,arma::fill::none);
        return bar.diag();
    }
    
    arma_cold inline arma::diagview<arma::cx_double> dcxfoo() { 
        arma::cx_mat bar(5,5,arma::fill::none);
        return bar.diag();
    }
    
    arma_cold inline arma::diagview<arma::cx_float> dcxffoo() { 
        arma::cx_fmat bar(5,5,arma::fill::none);
        return bar.diag();
    }
}
