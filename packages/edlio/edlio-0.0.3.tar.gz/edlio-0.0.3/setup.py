#!/usr/bin/env python3

from edlio import __appname__, __version__
from setuptools import setup

packages = [
    'edlio',
    'edlio.dataio',
]

setup(
    name=__appname__,
    version=__version__,
    author="Matthias Klumpp",
    author_email="matthias@tenstral.net",
    description='Module to work with data in an Experiment Directory Layout (EDL) structure',
    license="LGPL-3.0+",
    url="https://edl.readthedocs.io/",
    
    install_requires=[
        'toml>=0.10',
        'numpy>=1.17',
        'xxhash>=2.0',
        'Pint>=0.10'
    ],
    python_requires='>=3.8',
    platforms=['any'],

    packages=packages
)
