#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-approvaltests',
    version='0.2.3',
    author='Emily Bache',
    author_email='emily@bacheconsulting.com',
    maintainer='Emily Bache',
    maintainer_email='emily@bacheconsulting.com',
    license='MIT',
    url='https://github.com/approvals/pytest-approvaltests',
    description='A plugin to use approvaltests with pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_approvaltests'],
    python_requires='>=3.6.1',
    install_requires=['pytest>=3.5.0', 'approvaltests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'approvaltests = pytest_approvaltests',
        ],
    },
)
