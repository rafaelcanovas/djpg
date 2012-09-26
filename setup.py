#!/usr/bin/env python

from setuptools import setup

setup(name='djpg',
      version='0.1.0',
      author='Rafael Canovas',
      author_email='rafaelcanovas@me.com',
      url='https//github.com/rafaelcanovas/djpg',
      long_description=open('README.rst').read(),
      packages=['djpg'],
      package_data={'': ['UNLICENSE']},
      install_requires=['requests==0.14.0',
                        'furl==0.3.2',
                        'xmltodict==0.2'],
      license=open('UNLICENSE').read(),
)
