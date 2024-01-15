from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Your Cython App',
    ext_modules=cythonize("cythontest.pyx"),
    zip_safe=False,
)

# python setup.py build_ext --inplace