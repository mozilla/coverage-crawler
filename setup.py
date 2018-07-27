# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

setup(
    name='coverage_crawler',
    version='1.0.0',
    description='A crawler to find websites that exercise code in Firefox that is not covered by unit tests',
    install_requires=load_requirements('requirements.txt'),
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)
