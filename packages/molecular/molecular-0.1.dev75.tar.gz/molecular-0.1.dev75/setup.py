"""
setup.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from numpy.distutils.command.sdist import sdist
from numpy.distutils.core import Extension, setup

cmdclass = {'sdist': sdist}

# Read version
with open('version.yml', 'r') as f:
    data = f.read().splitlines()
version_dict = dict([element.split(': ') for element in data])

# Convert the version_data to a string
version = '.'.join([str(version_dict[key]) for key in ['major', 'minor']])
if version_dict['micro'] != 0:
    version += '.' + version_dict['micro']
print(version)

# Read in requirements.txt
with open('requirements.txt', 'r') as stream:
    requirements = stream.read().splitlines()

# Long description
with open('README.rst', 'r') as stream:
    long_description = stream.read()

# Setup
setup(
    name='molecular',
    version=version,
    author='C. Lockhart',
    author_email='chris@lockhartlab.org',
    description='A toolkit for molecular dynamics simulations',
    long_description=long_description,
    url="https://www.lockhartlab.org",
    packages=[
        'molecular',
        'molecular.analysis',
        'molecular.analysis.protein',
        'molecular.bioinformatics',
        'molecular.core',
        'molecular.external',
        'molecular.geometry',
        'molecular.io',
        'molecular.misc',
        'molecular.simulations',
        'molecular.statistics',
        'molecular.transform',
        'molecular.viz'
    ],
    install_requires=[
        'glovebox',
        'numpy',
        'pandas',
        'privatize',
        'typelike', 'hypothesis', 'numba'
    ],
    include_package_data=True,
    zip_safe=True,
    ext_modules=[
        Extension('molecular.io.fortran.read_dcd', ['molecular/io/src/read_dcd.f90'])
    ]
)
