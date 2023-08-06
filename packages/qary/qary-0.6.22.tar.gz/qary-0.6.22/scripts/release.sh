#!/usr/bin/env bash
# release.sh
# USAGE: source scripts/release.sh 0.5.21 'spell checker...'


# set -e
# pip install -U twine wheel setuptools
git commit -am "$2"
git push
git tag -l | cat
git tag -a "$1" -m "$2"

rm -rf build
rm -rf dist
find qary/data -type f -size +5M -exec rm -f {} \;

python setup.py sdist
python setup.py bdist_wheel

if [ -z "$(which twine)" ] ; then
    echo 'Unable to find `twine` so installing it with pip.'
    pip install --upgrade pip
    pip install --upgrade twine
fi

twine check dist/*
twine upload dist/"qary-$1-py"* --verbose
twine upload dist/"qary-$1.tar"* --verbose
git push --tag
