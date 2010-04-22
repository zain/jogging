#!/usr/bin/env python

from setuptools import setup

setup(name='jogging',
      version='0.1',
      description='Jogging makes logging in django easier',
      author='Zain',
      author_email='zain@inzain.net',
      url='',
      packages = ['jogging',],
      package_dir = {'jogging':'jogging'},
      test_suite='tests.main',
     )

