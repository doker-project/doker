#!/usr/bin/env python

from os import path 
from setuptools import find_packages, setup

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'CHANGELOG.rst'), 'r') as f:
    __version__ = f.readline().strip()

setup(
    name='doker',
    version=__version__,
    packages=find_packages(),
    author='Doker Authors',
    description="Rich PDF documents creating tool",
    url='https://github.com/doker-project/doker',
    long_description=open('README.rst').read(),
    entry_points={
        'console_scripts': [
            'doker = doker.main:main',
        ]},
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        '': ['CHANGELOG.rst', 'LICENSE']
    },
    install_requires = [
        'pyyaml',
        'rst2pdf',
    ],
)

