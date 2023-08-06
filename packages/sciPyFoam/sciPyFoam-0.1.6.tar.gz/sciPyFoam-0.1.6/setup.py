#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='sciPyFoam',
    version='0.1.6',
    author='Zhikui Guo',
    author_email='zguo@geomar.de',
    url='https://www.scibyte.cn',
    description=u'Visualize simulation results of OpenFOAM to publish qulity figure',
    packages=find_packages(where='.', exclude=('docs_scipyfoam'), include=('*',)), 
    install_requires=[
        'vtk',
        'matplotlib',
        'numpy',
        'meshio'
        ],
    entry_points={
        'console_scripts': []
    },
    keywords = "OpenFOAM publication figure SCI postprocessing"
)