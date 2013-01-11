#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='mannequin',
    version='0.1',
    description='A generic library for writing class-based declarative modeling systems in Python.',
    author='Dustin Lacewell and Calvin Spealman',
    author_email='dlacewell@gmail.com and ironfroggy@gmail.com',
    url='https://github.com/ironfroggy/mannequin',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Environment :: Plugins',
    ]
)
