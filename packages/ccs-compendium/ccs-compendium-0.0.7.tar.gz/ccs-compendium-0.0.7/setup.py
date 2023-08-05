#! /usr/bin/env python3

"""
CCS Compendium - Commands to help create and maintain an open science compendium
"""

from __future__ import print_function
import sys

from setuptools import setup

setup(name='ccs-compendium',
      description='CCS Compendium - creating a compendium for reproducible science',
      version='0.0.7',
      license='MIT',
      author='Wouter van Atteveldt',
      author_email='wouter@vanatteveldt.com',
      url='http://github.com/ccs-amsterdam/compendium',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        ],
      packages=['compendium', 'compendium.command', 'compendium.initsegment'],
      python_requires='>=3.6',
      install_requires=["doit", "cryptography", "requests"],
      long_description=__doc__,
      entry_points={
          'console_scripts': [
              'compendium = compendium.__main__:main'
          ]
      },
      )
