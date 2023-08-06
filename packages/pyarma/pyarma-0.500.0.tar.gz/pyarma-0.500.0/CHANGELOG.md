## Changelog:

### v0.500.0 (11 February 2021)  
* Size-only constructors (i.e. mat(rows, cols), mat(size(X)), cube(rows, cols, slices), cube(size(Q))) are initialised with zeros by default
* Conversion of NumPy arrays require the same data type (i.e. a NumPy array of integers cannot be converted to a PyArmadillo mat) (#10)
* Added pyarma_rng.set_seed(value)
* set_seed_random() is now pyarma_rng.set_seed_random()
* linspace(start, end, N) and logspace(start, end, N) take N as an unsigned integer (#12, #13)
* range(X) has been renamed to spread(X) to prevent conflicts with Python's built-in range() function (#14)
* Fixed bug where U, H = hess(X) returns X as well as U, H (#11)
* Added extra forms for lu(X), qr(X), qr_econ(X), qz(A, B), and svd_econ(X)
* Fixed bug where cube(subcube) threw a TypeError (#16)
* Added pyarma_version for version information (#15)
* Added randu(), randn(), zeros(), ones(), eye() generators
* Added subscripting for size objects
* Removed excess newline when printing matrices and cubes
* Removed excess newline printed by libraries() (#17)
* solve_opts_types and fill_types are now solve_opts.types and fill.types (i.e. solve_opts.fast, fill.randu)
* Internal types are hidden
* Fixed bug where clamp(ucube/icube) took wrong argument types (#18)

### v0.400.0 (1 February 2021)  
Initial public release, adapting dense matrices and cubes from Armadillo

### v0.100.0-0.300.0
Internal development releases