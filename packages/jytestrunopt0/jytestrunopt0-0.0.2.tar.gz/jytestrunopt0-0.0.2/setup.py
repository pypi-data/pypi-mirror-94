#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='jytestrunopt0',
    version='0.0.2',
    author='zjy',
    author_email='unknown@bgsn.com',
    url='https://www.cnblogs.com/zhangjialu2015/p/5173313.html',
    description='opt0',
    py_modules = ['jytest0'],
    install_requires=[],
    extras_require={
        'a':['jytestrunopt1==0.0.1'],
        'b':['jytestrunopt2==0.0.1']
    }
)
