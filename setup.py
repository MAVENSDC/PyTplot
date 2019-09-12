#Uploading new versions to pypi:
#
#python setup.py sdist
#twine upload dist/*
#Username MAVENSDC



#Uploading new versions to conda:
#
#conda-build pytplot
#conda-build --python 3.6 pytplot
#conda-build --python 3.5 pytplot
#conda convert -f --platform all /path/to/created/bundles/file.tar.bz2 -o /path/to/place/converted/files
#anaconda upload /path/to/created/or/converted/bundles/file.tar.bz2
#Username MAVENSDC

from setuptools import setup
setup()
