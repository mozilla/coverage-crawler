# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from setuptools import find_packages
from setuptools import setup

here = os.path.dirname(__file__)


def read_requirements(file_):
    requires = []
    links = []
    with open(os.path.join(here, file_)) as f:
        for line in f.readlines():
            line = line.strip()

            if line.startswith('https://'):
                links.append(line + '-1.0.0')
                extras = ''
                if '[' in line:
                    extras = '[' + line.split('[')[1].split(']')[0] + ']'
                line = line.split('#')[1].split('egg=')[1] + extras
            elif line == '' or line.startswith('#') or line.startswith('-'):
                continue
            line = line.split('#')[0].strip()
            requires.append(line)

    return sorted(list(set(requires))), links


install_requires, dependency_links = read_requirements('requirements.txt')

setup(
    name='coverage_crawler',
    version='1.0.0',
    description='A crawler to find websites that exercise code in Firefox that is not covered by unit tests',
    install_requires=install_requires,
    dependency_links=dependency_links,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    license='MPL2',
)
