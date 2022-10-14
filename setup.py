from setuptools import Extension, setup
from Cython.Build import cythonize
setup(
    ext_modules = cythonize([
        Extension("pyaspic", ["pyaspic.pyx"],
        extra_compile_args=['-fPIC', '-O3', '-lgfortran','-lquadmath','-std=c99'],

#        extra_compile_args=['libaspic.a']
        #library_dirs=[r'/usr/local/lib']
        extra_link_args=['libaspic.a',
        #'-L/usr/local/Cellar/gcc/6.3.0_1/lib/gcc/6',
        '-lgomp','-lgfortran','-lquadmath',]
    )],
    language_level=3)
)
