#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

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
    version='0.4',
    description="Python client for Figshare",
    long_description=readme + '\n\n' + history,
    author="Markus Binsteiner",
    author_email='makkus@gmail.com',
    url='https://github.com/UoA-eResearch/pigshare',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
          'console_scripts': [
              'pigshare = pigshare.pigshare:run'
          ],
        }
)
