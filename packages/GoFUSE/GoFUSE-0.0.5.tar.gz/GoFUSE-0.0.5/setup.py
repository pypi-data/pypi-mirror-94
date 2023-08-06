import os
import sys

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 0)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(f"""
==========================
Unsupported Python version
==========================
GoFUSE was written for requires Python {REQUIRED_PYTHON}, but you're trying to install it on Python {CURRENT_PYTHON}. This may also be because you are using a version of pip that doesn't understand the python_requires classifier. Make sure you have pip >= 9.0 and setuptools >= 24.2, then try again:
    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install GoFUSE
""")
    sys.exit(1)

from distutils.core import setup


setup(
    name='GoFUSE',
    version='0.0.5',
    author='Georg Gogo. BERNHARD',
    author_email='gogo@bluedynamics.com',
    packages=['GoFUSE',],
    scripts=['',],
    url='https://pypi.org/project/GoFUSE/0.0.1/',
    license='GPL',
    description='GoFUSE is a pyfuse / xmlrpc based distributed filesystem.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "fusepy >= 3.0.1",
    ],
)
