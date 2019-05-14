#!/usr/bin/env python

import re
from os import path
from setuptools import find_packages, setup

__version__ = '0.0.0'
current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'CHANGELOG.rst'), 'r') as f:
    for line in f:
        m = re.search(r'`(\d+\.\d+\.\d+)`_', line)
        print(line)
        if m:
            __version__ = m.group(1)
            break;

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
        'doker': ['rst2pdf/styles/*.json', 'rst2pdf/styles/*.style', 'rst2pdf/images/*.png', 'rst2pdf/images/*.jpg', 'rst2pdf/templates/*.tmpl'],
        '': ['CHANGELOG.rst', 'LICENSE']
    },
    install_requires = [
        'docutils',
        'Jinja2',
        'pyyaml',
        'reportlab==3.5.18', # Waiting for fixing https://github.com/rst2pdf/rst2pdf/issues/773 
        'Pygments',
        'pdfrw',
        'pillow',
        'six',
    ],
)

