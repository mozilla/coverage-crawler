# -*- coding: utf-8 -*-

import os

from setuptools import find_packages
from setuptools import setup


def load_requirements(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read().strip().split('\n')


setup(
    name='coverage_crawler',
    version='1.0.0',
    description='A crawler to find websites that exercise code in Firefox that is not covered by unit tests',
    install_requires=load_requirements('requirements.txt'),
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)
