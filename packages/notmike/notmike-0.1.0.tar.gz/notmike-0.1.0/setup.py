#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='notmike',
    version='0.1.0',
    author='Mihir Singh (@citruspi)',
    author_email='pypi.service@mihirsingh.com',
    scripts=['bin/notmike'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['peche']
)
