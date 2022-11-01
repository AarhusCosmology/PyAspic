# PyAspic
Python wrapper for the ASPIC library

## Installation

Run

````bash
./get_get_and_build_aspic.sh
````

Here is what it does/attemps to do:
- Download the Aspic library
- Configure and build the library
- Generate Cython code for a Python module, `PyAspic`, holding all public functions from all modules by parsing the Fortran source code.
- Built the Python module

Fortran `STOP` statements are intercepted and a Python exception is raised insted.

## Issues

- ~~Functions containing complex and boolean data-types are not currently wrapped.~~
- One may need to manually add the library paths to e.g. libgfortran and libquadmath inside `setup.py`.
- ~~Only the return value of a function is returned in the wrapper, i.e. we are not yet supporting passed variables being changed. This could be fixed by reading the `intent` keywords for each variables.~~
- ~~Subroutines are currently not wrapped due to the limitation above.~~

