from setuptools import setup, find_packages

classifiers = [
	"Development Status :: 5 - Production/Stable",
	'License :: OSI Approved :: MIT License',
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
	'Programming Language :: Python :: 3.8',
	'Programming Language :: Python :: 3.9',
]

setup(
	name='lite3',
	version='0.0.1',
	description='Maintain sqlite3 databases easily and without MYSQL syntax',
	long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
	long_description_content_type="text/markdown",
	url="",
	author="Rogers Kabuye",
	author_email="rogerskabuye0@gmail.com",
	License='MIT',
	classifiers=classifiers,
	keywords="",
	packages=find_packages(),
	install_requires=['']
)