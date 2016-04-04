#!/bin/bash

savReaderWriter=~/nfs/Public/savreaderwriter
cd $savReaderWriter
version=$(cat VERSION)

echo "***********************************************************************"
echo "Start running setup.py with bdist_wheel option"
echo "***********************************************************************"

python setup.py bdist_wheel

echo "***********************************************************************"
echo "Start running setup.py with sdist gztar,zip"
echo "***********************************************************************"

python setup.py sdist --formats=gztar,zip

echo "***********************************************************************"
echo "Start running setup.py with build_sphinx (documentation)"
echo "***********************************************************************"

python setup.py check build_sphinx --source-dir=savReaderWriter/documentation -v


