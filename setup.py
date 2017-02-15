#!/usr/bin/env python3

from setuptools import setup, find_packages

exec(open('ukgeo/version.py').read())

setup(
    name='ukgeo',
    version=__version__,
    description='Utilities to work with the UKMap and UKBuilding datasets.',
    maintainer='Tim Tröndle',
    maintainer_email='tt397@cam.ac.uk',
    url='https://www.github.com/EECi/ukgeo',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering'
    ]
)
