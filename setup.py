#!/usr/bin/env python
from setuptools import setup

setup(name='djpg',
	version='0.1.1',
	description='djpg is a Django module that integrates with the online payment service PagSeguro.',
	long_description=open('README.rst').read(),
	author='Rafael Canovas',
	author_email='rafaelcanovas@me.com',
	url='https://github.com/rafaelcanovas/djpg',
	packages=['djpg'],
	package_data={'': ['UNLICENSE']},
	install_requires=[
		'requests==0.14.0',
		'furl==0.3.2',
		'xmltodict==0.2'
	],
	license=open('UNLICENSE').read(),
)
