#!/usr/bin/env python
#
# Setup script for the Natural Language Toolkit
#
# 2020 TextLytics Project
# Authors: Jorge Luiz Figueira da Silva Junior <jorgeluizfigueira@gmail.com>, 
# Fábio Lobato <lobato.fabiof@gmail.com>
# For license information, see LICENSE.TXT

from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='textlytics',
    version='1.0.1',
    description="TEXTLYTICS -- the Text Analytics Toolkit",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url="https://gitlab.com/jorgeluizfigueira/python-textlytics/",
    packages = find_packages(),
    maintainer="Jorge Luiz Figueira",
    maintainer_email="jorgeluizfigueira@gmail.com",
    author="Jorge Luiz Figueira",
    author_email="jorgeluizfigueira@gmail.com",
    license='GPLV3+',
    classifiers=[

    'Development Status :: 3 - Alpha',

    'Intended Audience :: Science/Research',

    'Topic :: Scientific/Engineering :: Information Analysis',

    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',


    'Programming Language :: Python :: 3',

    ],
    keywords=[
        "text complexity",
        "text readability",
        "natural language processing",
        "computational linguistics",
        "part of speech",
        "linguistics",
        "language",
        "natural language",
        "text analytics",
    ],

    python_requires='>=3',
    install_requires=['pandas','Pyphen','syllables','nltk','nlpnet'],

)