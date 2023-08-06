from setuptools import setup

setup(
	name='finpython',
	version='0.013',
	author='Jamiel Sheikh',
	packages=['finpython'],
	install_requires=[
		'pandas',
		'matplotlib',
		'datetime',
		'requests'
	],
	include_package_data=True,
)