import os
from setuptools import setup

if os.getenv('PUBLISHING') != '1':
    raise AssertionError('https://hackerone.com/reports/1099882')


setup(
    name='lyft-logging',
    version='9999.9999.9999',
    author='Anthony Sottile',
    author_email='asottile+lyft@umich.edu',
)
