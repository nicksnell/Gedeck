from setuptools import setup, find_packages
from gedeck import __version__

setup(
	name='Gedeck',
	version=__version__,
	description='Simple Django app for managing RSVP\'s and Menu Selections',
	author='Nick Snell',
	author_email='nick@orpo.co.uk',
	license='BSD',
	platforms=['Linux',],
	zip_safe=False,
	packages=find_packages(exclude=['tests',]),
	install_requires=[
		'django==1.5.5',
	]
)