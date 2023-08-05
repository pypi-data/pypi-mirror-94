#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


readme = open('README.md').read()

requirements = [
    "petl==1.7.1",
    "xlwt==1.3.0",
    "xlrd==2.0.1",
]

setup(
    name='libtabular',
    version='0.0.3',
    license='MIT',
    description='Utility functions for reading and writing CSV files with metadata headers.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ivan Savov',
    author_email='ivan.savov@gmail.com',
    url='https://github.com/rocdata/libtabular',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://github.com/rocdata/libtabular/tree/main/docs',
        'Issue Tracker': 'https://github.com/rocdata/libtabular/issues',
    },
    keywords=[
        "CSV",
        "Excel",
        "spreadhseets",
        "metadata",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={},
)
