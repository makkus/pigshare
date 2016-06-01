3#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import io
import re
init_py = io.open('pigshare/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
metadata['doc'] = re.findall('"""(.+)"""', init_py)[0]

requirements = [
    "argparse",
    "setuptools",
    "restkit",
    "booby",
    "simplejson",
    "parinx",
    "pyclist",
    "argcomplete"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pigshare',
    version=metadata['version'],
    description=metadata['doc'],
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    packages=[
        'pigshare',
    ],
    package_dir={'pigshare':
                 'pigshare'},
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords='pigshare figshare client rest api',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
          'console_scripts': [
              'pigshare = pigshare.pigshare:run'
          ],
        }
)
