# - Config file for the Armadillo package
# It defines the following variables
#  ARMADILLO_INCLUDE_DIRS - include directories for Armadillo
#  ARMADILLO_LIBRARY_DIRS - library directories for Armadillo (normally not used!)
#  ARMADILLO_LIBRARIES    - libraries to link against

# Tell the user project where to find our headers and libraries
set(ARMADILLO_INCLUDE_DIRS "/private/var/folders/zc/w54y8dpx71z33yjn8gmrlq3w0000gn/T/pip-req-build-mnu0wvaq/_skbuild/macosx-10.9-x86_64-3.7/cmake-install/src/pyarma/include")
set(ARMADILLO_LIBRARY_DIRS "/private/var/folders/zc/w54y8dpx71z33yjn8gmrlq3w0000gn/T/pip-req-build-mnu0wvaq/_skbuild/macosx-10.9-x86_64-3.7/cmake-install/src/pyarma/lib")

# Our library dependencies (contains definitions for IMPORTED targets)
include("/private/var/folders/zc/w54y8dpx71z33yjn8gmrlq3w0000gn/T/pip-req-build-mnu0wvaq/_skbuild/macosx-10.9-x86_64-3.7/cmake-install/src/pyarma/share/Armadillo/CMake/ArmadilloLibraryDepends.cmake")

# These are IMPORTED targets created by ArmadilloLibraryDepends.cmake
set(ARMADILLO_LIBRARIES armadillo)

