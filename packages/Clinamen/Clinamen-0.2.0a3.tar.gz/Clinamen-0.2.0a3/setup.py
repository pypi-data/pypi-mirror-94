# -*- coding: utf-8 -*-
""" Copyright 2020 Marco Arrigoni

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
import os
from setuptools import Extension, setup, find_packages
from Cython.Build import cythonize
import numpy

import clinamen


with open("README.rst", "r") as fh:
    long_description = fh.read()

current_path = ''

ext_modules_desc = [
    Extension('clinamen.descriptors.finger_descriptors_cython',
              sources=[
                  os.path.join(current_path, 'clinamen',
                               'descriptors',
                               'finger_descriptors_cython.pyx'),
                  os.path.join(current_path, 'clinamen',
                               'descriptors',
                               'finger_descriptors_c.c'),
                  os.path.join(current_path, 'clinamen',
                               'descriptors',
                               'basic_operations.c')
              ],
              libraries=['m'],
              include_dirs=[numpy.get_include(),
                            os.path.join(current_path, 'clinamen',
                                         'descriptors')
                  ]
              )
]

setup(
    name='Clinamen',
    version=clinamen.__version__,
    description=clinamen.__summary__,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url=clinamen.__uri__,
    author=clinamen.__author__,
    author_email=clinamen.__email__,
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'Programming Language :: Cython'
    ],
    python_requires='>=3.8',
    setup_requires=['cython>=0.29',
                    'numpy>=1.18'],
    install_requires=['ase>=3.19',
                      'numpy>=1.18',
                      'scipy>=1.5',
                      'pandas>=1.0',
                      'scikit-learn>=0.23.1',
                      'mpi4py>=3.0',
                      'h5py>=2.10',
                      'cython>=0.29'
                      'pytorch>=1.7.0',
                      'gpytorch>=1.3.0',
                      'dscribe>=0.4.0'
    ],
    packages=find_packages(),
    package_data={
        'clinamen.descriptors':
        ['finger_descriptors_c.h', 'basic_operations.h',
         'finger_descriptors_cython.pyx']
    },
    #include_package_data=True,
    ext_pkg='descriptors',
    ext_modules=cythonize(
        ext_modules_desc, 
        compiler_directives={'language_level': sys.version_info[0]})
)

