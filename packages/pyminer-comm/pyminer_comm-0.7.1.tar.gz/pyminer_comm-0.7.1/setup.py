#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
import os
import shutil

dist_path = os.path.join(os.path.dirname(__file__), 'dist')
if os.path.exists(dist_path):
    shutil.rmtree(dist_path)
setup(
    name='pyminer_comm',
    version='0.7.1',
    description=(
        'PyMiner Extension package to transfer data'
        'with PyMiner or manipulate PyMiner by another python process.'
    ),
    author='hzy15610046011',
    author_email='1295752786@qq.com',
    license='LGPL',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/hzy15610046011/pyminer_comm',
    install_requires=[
        'cloudpickle'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
