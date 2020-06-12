"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/Rambatino/Kruskals
"""

import re
from os import path
from setuptools import setup, find_packages


def get_version():
    """
    Read version from __init__.py
    """
    version_regex = re.compile(
        '__version__\\s*=\\s*(?P<q>[\'"])(?P<version>\\d+(\\.\\d+)*)(?P=q)'
    )
    here = path.abspath(path.dirname(__file__))
    init_location = path.join(here, "Kruskals/__init__.py")

    with open(init_location) as init_file:
        for line in init_file:
            match = version_regex.search(line)

    if not match:
        raise Exception(
            "Couldn't read version information from '%s'" % init_location
        )

    return match.group('version')

setup(
    name='Kruskals',
    version=get_version(),
    description='Calculation of Kruskals Distance Measure',
    long_description="This package provides a python implementation of Kruskals Distance measure",
    url='https://github.com/Rambatino/Kruskals',
    author='Mark Ramotowski',
    author_email='mark.tint.ramotowski@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>3.5',
    keywords='Kruskals pandas numpy scipy statistics statistical analysis',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['numpy>1.17', 'scipy', 'pandas'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['codecov', 'pytest', 'pytest-cov'],
    }
)
