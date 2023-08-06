#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='no_error_python_shell',
    version='0.0.1',
    author='William Ma',
    author_email='3327821469@qq.com',
    url='https://github.com/theCoder-WM',
    description=u'no error python shell',
    packages=['no_error_python_shell'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'nepython=no_error_python_shell:start_shell'
        ]
    }
)
