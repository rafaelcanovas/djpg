#!/usr/bin/env python

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

try:
	import pypandoc
	long_description = pypandoc.convert('README.md', 'rst')
except (ImportError, OSError, IOError):
	long_description = ''


setup(name='djpg',
	version='0.1.1',
	description='djpg is a Django module that integrates with the online payment service PagSeguro.',
	long_description=long_description,
	author='Rafael Canovas',
	author_email='rafaelcanovas@me.com',
	url='https://github.com/rafaelcanovas/djpg',
	packages=['djpg'],
	package_data={'': ['UNLICENSE']},
	install_requires=[
		'requests',
		'xmltodict==0.5.1'
	],
	license=open('UNLICENSE').read(),
)
