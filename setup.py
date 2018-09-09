#!/usr/bin/env python3

from os import path 
from setuptools import find_packages, setup

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, 'CHANGELOG.rst'), encoding='utf-8') as f:
    version = f.readline().strip()

setup(
    name='doker',
    version=version,
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
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        '': ['CHANGELOG.rst', 'LICENSE']
    },
)

