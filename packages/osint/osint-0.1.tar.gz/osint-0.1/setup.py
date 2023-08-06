#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='osint',
    author='QeeqBox',
    author_email='gigaqeeq@gmail.com',
    description="Collection of Open Source Intelligence (OSINT) tools",
    long_description=long_description,
    version='0.1',
    license='AGPL-3.0',
    url='https://github.com/qeeqbox/osint',
    packages=['osint'],
    include_package_data=True,
    entry_points={'console_scripts': ['osint = osint.__main__:main']},
    install_requires=['termcolor'],
    python_requires='>=3',
    )
