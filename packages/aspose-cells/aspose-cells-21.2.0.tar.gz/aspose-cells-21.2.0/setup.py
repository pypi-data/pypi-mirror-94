# coding: utf-8

import sys
from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "aspose-cells"
VERSION = "21.2.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["JPype1 >= 1.2.1"]

setup(
    name=NAME,
    version=VERSION,
    description="Python API to read, write, manipulate & convert Microsoft Excel® files without any dependency. Create & manipulate Workbooks, Worksheets, Pivot Tables, Charts, Sparklines, Conditional Formatting & more. Convert Excel to PDF, XPS, HTML, images & metafiles.",
    author="Aspose",
    author_email="cells@aspose.com",
    url="https://products.aspose.com/cells/python-java",
    keywords=["Excel API", "Spreadsheet API", "aspose", "cells", "java"],
    install_requires=REQUIRES,
    packages=['asposecells'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'License :: Other/Proprietary License'
    ],
    platforms=[
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Operating System :: Microsoft :: Windows :: Windows Vista',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.5',
)
