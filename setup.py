import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
        README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version = 0.1

setup(
    name='django-usr',
    version=version,
    packages=['usr'],
    include_package_data=True,
    license='GPL License',
    description='User profile and IR national id verification for django',
    long_description=README,
    url='',
    author='Alireza Molaee, Mohammad Haghighat',
    author_email='hosseinhg@hotmail.com',
    classifiers=[
	'Environment :: Web Environment',
	'Framework :: Django',
	'License :: OSI Approved :: GNU General Public Licence (GPL)',
	'Operating System :: OS Independent',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.4',
	'Topic :: Internet :: WWW/HTTP',
	'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires = [
	'django-user-accounts==1.2',
	'pillow>=2',
    ]
)
