#!/usr/bin/env python                                                                                                                               
from setuptools import setup, find_packages


setup(
  name='TRNLTK',
  version='0.0.1',
  description='Turkish Natural Language Toolkit',
  long_description='',
  author='Ali Ok',
  author_email='aliok@apache.org',
  maintainer='Ali Ok',
  maintainer_email='aliok@apache.org',
  url='https://github.com/aliok/trnltk',
  license='Apache 2',
  classifiers=[
    'License :: OSI Approved :: Python Software Foundation License',
  ],
  data_files=[],
  packages=find_packages(),
  install_requires=[],
  setup_requires=['pytest-runner'],
  tests_require=['pytest', 'pytest-sugar']
)
