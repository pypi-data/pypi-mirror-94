cmake_minimum_required(VERSION 3.12...3.18)
project(pyarma LANGUAGES CXX)

# Find all PyArma source files
file(GLOB_RECURSE pyarma_SOURCES "src/*.cpp")

# Uses C++11
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Force static libraries to be built
set(BUILD_SHARED_LIBS OFF CACHE BOOL "build shared library" FORCE)

# # The user's OpenBLAS is used by default
# option(PYARMA_STATIC_OPENBLAS "Compile OpenBLAS and statically link it against PyArmadillo" OFF)

# Add Armadillo and pybind11
if($ENV{CIBUILDWHEEL})
    set(ALLOW_OPENBLAS_MACOS ON CACHE BOOL "Allow detection of OpenBLAS on macOS" FORCE)
endif()
add_subdirectory(ext/armadillo)
add_subdirectory(ext/pybind11)

# # Add OpenBLAS for compilation if needed
# if(PYARMA_STATIC_OPENBLAS)
#     add_subdirectory(ext/openblas)
# endif()

# Create PyArma module
option(PYARMA_LTO "Enable link-time optimisation" OFF)
if(PYARMA_LTO)
    message(STATUS "LTO is enabled. This reduces binary sizes at the expense of longer compile times.")
    pybind11_add_module(pyarma ${pyarma_SOURCES})
else()
    message(STATUS "LTO is disabled.")
    pybind11_add_module(pyarma ${pyarma_SOURCES} NO_EXTRAS)
    ## NOTE: pybind11 also has the OPT_SIZE option, which uses -Os optimisation.
    ## NOTE: pybind11 by default uses -O3 optimisation, which is problematic for us
    ## NOTE: (ie. slower compilation and increased memory use during compilation)
    ## NOTE: see the workaround near the end
endif()

# Add -fPIC for Armadillo (and OpenBLAS if compiled)
if(NOT MSVC)
    # clang on Windows does not support -fPIC
    if(NOT WIN32)
        target_compile_options(armadillo PRIVATE -fPIC)
    endif()
#   if(PYARMA_STATIC_OPENBLAS)
#     target_compile_options(openblas PRIVATE -fPIC)
#   endif()
endif()

if($ENV{CIBUILDWHEEL})
    message(STATUS "Building on a CI server. Precompiled libraries used.")
    # Set a flag stating that a precompiled version of OpenBLAS is used
    target_compile_definitions(pyarma PRIVATE -DPYARMA_PRECOMPILED_OPENBLAS)
    if(UNIX AND NOT APPLE)
        # Set a flag stating that a precompiled version of HDF5 is used on Linux
        target_compile_definitions(pyarma PRIVATE -DPYARMA_PRECOMPILED_HDF5)
    endif()
    # Force use of LAPACK, as OpenBLAS is always used anyway
    target_compile_definitions(armadillo PRIVATE -DARMA_USE_LAPACK)
    target_compile_definitions(pyarma PRIVATE -DARMA_USE_LAPACK)
    # # On Windows, use static OpenBLAS
    # if(WIN32)
    #     target_compile_definitions(armadillo PRIVATE -DARMA_USE_BLAS)
    #     target_compile_definitions(pyarma PRIVATE -DARMA_USE_BLAS)
    #     target_link_libraries(armadillo PRIVATE ${CMAKE_SOURCE_DIR}/lib/openblas.a)
    #     target_link_directories(armadillo PRIVATE "${CMAKE_SOURCE_DIR}/lib")
    #     target_link_directories(pyarma PRIVATE "${CMAKE_SOURCE_DIR}/lib")
    #     install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/lib/libgfortran3.dll DESTINATION .)
    # endif()
endif()

# Use precompiled OpenBLAS
if(WIN32)
    message(STATUS "Linking precompiled OpenBLAS")
    target_compile_definitions(armadillo PRIVATE -DARMA_USE_LAPACK)
    target_compile_definitions(armadillo PRIVATE -DARMA_USE_BLAS)
    target_compile_definitions(pyarma PRIVATE -DARMA_USE_LAPACK)
    target_compile_definitions(pyarma PRIVATE -DARMA_USE_BLAS)
    file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/ext/armadillo/examples/lib_win64/libopenblas.dll DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
    install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/ext/armadillo/examples/lib_win64/libopenblas.dll DESTINATION .)
    add_library(win64_openblas SHARED IMPORTED)
    set_target_properties(win64_openblas PROPERTIES
        IMPORTED_LOCATION "${CMAKE_CURRENT_BINARY_DIR}"
        IMPORTED_IMPLIB "${CMAKE_CURRENT_SOURCE_DIR}/ext/armadillo/examples/lib_win64/libopenblas.lib")
    target_include_directories(armadillo PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/ext/armadillo/examples/lib_win64/")
    target_link_libraries(armadillo PRIVATE win64_openblas)
    
    # Set a flag stating that a precompiled version of OpenBLAS is used
    target_compile_definitions(pyarma PRIVATE -DPYARMA_PRECOMPILED_OPENBLAS)
    
    ## NOTE: isn't WIN32 enabled if mingw is used? if so, can't assume that MSVC is being used
    if(MSVC)
      # MSVC cannot compile heavily templated source files
      target_compile_options(pyarma PRIVATE /bigobj)
    #   target_compile_definitions(pyarma PRIVATE -DPYARMA_NO_CX_STATS)
    endif()
endif()

# # Search for NumPy and disable NumPy conversion if not found.
# # NumPy conversion overrides type promotion for element initialisation
# # (i.e. mat([ 0, 1, 2, ... ]))
# # and will cause a ModuleNotFoundError if NumPy is not installed.
# find_package(NumPy)
# if(NOT NumPy_FOUND)
#     message(STATUS "NumPy was not found: array conversion disabled.")
#     target_compile_definitions(pyarma PRIVATE -DPYARMA_NO_NUMPY)
# else()
#     message(STATUS "NumPy was found: array conversion enabled.")
# endif()

# Show amount of jobs, if set
if($ENV{CMAKE_BUILD_PARALLEL_LEVEL})
    message(STATUS "$ENV{CMAKE_BUILD_PARALLEL_LEVEL} jobs will be run in parallel.")
endif()

# # Add versioning
# target_compile_definitions(pyarma PRIVATE -DPYARMA_VERSION_MAJOR=${PYARMA_VERSION_MAJOR})
# target_compile_definitions(pyarma PRIVATE -DPYARMA_VERSION_MINOR=${PYARMA_VERSION_MINOR})
# target_compile_definitions(pyarma PRIVATE -DPYARMA_VERSION_PATCH=${PYARMA_VERSION_PATCH})
# target_compile_definitions(pyarma PRIVATE -DPYARMA_VERSION_NAME=${PYARMA_VERSION_NAME})

# Link PyArma to Armadillo
target_link_libraries(pyarma PRIVATE armadillo)

# Configure with libraries used
configure_file(${PROJECT_SOURCE_DIR}/include/libraries.hpp.in ${PROJECT_SOURCE_DIR}/include/libraries.hpp)

# Configure versioning
configure_file(${PROJECT_SOURCE_DIR}/include/version.hpp.in ${PROJECT_SOURCE_DIR}/include/version.hpp)

# Include all directories used
target_include_directories(pyarma PRIVATE 
"${PROJECT_BINARY_DIR}"
"${PROJECT_SOURCE_DIR}/ext/armadillo"
"${PROJECT_SOURCE_DIR}/ext/pybind11"
"${PROJECT_SOURCE_DIR}/include"
)

# See this page on the problematic default use of -O3 by CMake:
# https://wiki.archlinux.org/index.php/CMake_package_guidelines
# 
# Workaround for the problematic use of "-O3" optimisation with gcc.
# Add the "-O2" flag to the command line as further back as possible,
# which causes gcc to ignore any earlier optimisation settings
# on the command line (ie. "-O3 -O2" causes "-O2" to be used).
if(NOT MSVC)
  # add_definitions("-O2")
  target_compile_options(pyarma PRIVATE "-O2")
endif()

## investigate use CMAKE_<LANG>_COMPILER_ID instead of "NOT MSVC";
## however, this approach would need to handle several variants of clang
## https://cmake.org/cmake/help/latest/variable/CMAKE_LANG_COMPILER_ID.html


# Install PyArma
install(TARGETS pyarma DESTINATION .)
