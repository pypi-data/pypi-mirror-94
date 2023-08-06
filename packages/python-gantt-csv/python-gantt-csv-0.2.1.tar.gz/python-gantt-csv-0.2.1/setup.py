#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
from setuptools import setup

from gantt_csv import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-gantt-csv',
    version=__version__,
    author='Shota Horie',
    author_email='horie.shouta@gmail.com',
    license='gpl-3.0.txt',
    keywords="gantt, graphics, scheduling, project management",
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    platforms=[
        "Operating System :: OS Independent",
        ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Scientific/Engineering :: Visualization",
        ],
    packages=['gantt_csv'],
    description='python-gantt-csv manage gantt.Task arguments with csv format.',
    long_description=long_description,
    include_package_data=True,
    install_requires=[
        'python-gantt>=0.6.0'
        ],
    url='https://gitlab.com/shotahorie/python-gantt-csv',
    zip_safe=True,
    )
