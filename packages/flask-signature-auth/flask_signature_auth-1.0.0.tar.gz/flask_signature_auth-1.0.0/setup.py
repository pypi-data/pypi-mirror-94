#!/usr/bin/env python

import os, glob
from setuptools import setup, find_packages

setup(
    name='flask_signature_auth',
    version='1.0.0',
    url='https://github.com/kunyo/flask_signature_auth',
    license='BSD 3-Clause License',
    author='Stefano Cocchi',
    author_email='',
    description='',
    long_description='',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    platforms=['MacOS X', 'Posix'],
    test_suite='test',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    dependency_links=[],
    install_requires=['Flask>=1.1.2','cryptography', 'jwcrypto']
)