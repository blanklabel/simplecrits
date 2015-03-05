#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
packages = ['simplecrits',
            'simplecrits.lib',
            'simplecrits.lib.core',
            ]
requires = ['requests']

setup(name='simplecrits',
      version='0.5.0a2',
      description='Crits API interaction made simple',
      author='',
      author_email='',
      url='http://www.python.org/sigs/distutils-sig/',
      packages=packages,
      package_dir={'simplecrits': 'simplecrits'},
      include_package_data=True,
      install_requires=requires,)
