#!/usr/bin/env python

import re
from os import path 
from setuptools import find_packages, setup

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'CHANGELOG.rst'), 'r') as f:
    version_string = f.readline().strip()
m = re.search(r'(\d+\.\d+\.\d+)', version_string)
__version__ = m.group(1) if m else '0.0.0'

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
        'docutils',
        'pyyaml',
        'rst2pdf',
    ],
)

