#!/bin/bash

set -e
cd "$(dirname "$(readlink -f "${0}")")"/..

pip install --user --upgrade setuptools wheel twine

rm -rfv build dist doker.egg-info

./setup.py sdist bdist_wheel
twine upload dist/*