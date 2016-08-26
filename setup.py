#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='convo',
      version='0.1.0',
      description='Medium-agnostic conversation wrangler',
      long_description=open('README.rst').read(),
      author='Benno Rice',
      author_email='benno@jeamland.net',
      url='https://github.com/jeamland/convo',
      package_data={'': ['LICENSE']},
      py_modules=['convo'],
      classifiers=(
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: Implementation :: CPython',
      ),
)
