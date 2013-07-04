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
		'requests',
		'furl==0.3.4',
		'xmltodict==0.5'
	],
	license=open('UNLICENSE').read(),
)
