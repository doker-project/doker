#!/usr/bin/env python3
 
from setuptools import setup

setup(
    name='doker',
    version='0.0.1',
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
)