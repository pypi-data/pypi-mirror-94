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
#define PYARMA_VERSION_MAJOR 0
#define PYARMA_VERSION_MINOR 500
#define PYARMA_VERSION_PATCH 0
#define PYARMA_VERSION_NAME "Everyday"
#include <iostream>

namespace pyarma {
    struct pyarma_version {
        static constexpr unsigned int major = PYARMA_VERSION_MAJOR;
        static constexpr unsigned int minor = PYARMA_VERSION_MINOR;
        static constexpr unsigned int patch = PYARMA_VERSION_PATCH;
        static constexpr char const * name = PYARMA_VERSION_NAME;
    
        static inline std::string as_string() {
            std::ostringstream ss;
            ss << pyarma_version::major << '.' << pyarma_version::minor << '.' << pyarma_version::patch << " (" << name << ')';
            return ss.str();
        }
    };  
}
