from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
    name='pyaspic',
    version='0.3.2',
    description='Python interface to the Aspic library',
    url='http://cp3.irmp.ucl.ac.be/~ringeval/aspic.html',
    ext_modules = cythonize(
        Extension("pyaspic", ["pyaspic.pyx"],
            extra_objects=['catch.o', 'libaspic.a'],
            extra_link_args=['-lgfortran','-lquadmath',]
        ),
        language_level=3,
        annotate=False
    )
)
