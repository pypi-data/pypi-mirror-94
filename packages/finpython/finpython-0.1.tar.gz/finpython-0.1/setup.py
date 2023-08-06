from setuptools import setup

setup(
	name='finpython',
	version='0.01',
	author='Jamiel Sheikh',
	packages=['finpython'],
	install_requires=[
		'pandas',
		'matplotlib',
		'datetime',
		'requests',
		'chart_studio'
	],
	include_package_data=True,
)