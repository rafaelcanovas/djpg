#!/usr/bin/env python
# coding: utf-8

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

try:
	import pypandoc
	long_description = pypandoc.convert('README.md', 'rst')
except (ImportError, OSError, IOError):
	long_description = ''

try:
	license = open('LICENSE').read()
except IOError:
	license = ''

setup(
	name='djpg',
	version='0.1.3',
	description='djpg is a Django module that integrates with the online payment service PagSeguro.',
	long_description=long_description,
	author='Rafael Canovas',
	author_email='rafaelcanovas@me.com',
	url='https://github.com/mstrcnvs/djpg',
	license=license,
	packages=['djpg'],
	package_data={'': ['LICENSE']},
	include_package_data=True,
	install_requires=[
		'requests==2.0.0',
		'xmltodict==0.8.1'
	],
)
