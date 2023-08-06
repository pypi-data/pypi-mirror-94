from setuptools import setup

with open('README.md', 'r') as desc:
	long_description = desc.read()

setup(
	name='easy_colors',
	version='0.0.1',
	description='Colored text in the console',
	py_modules=['easy_colors'],
	package_dir={'': 'src'},
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
		"Operating System :: OS Independent",
	],
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/farhadzaidi/easy_colors',
	author='Farhad Zaidi',
	author_email='zaidi.farhad03@gmail.com',

)