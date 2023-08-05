"""
jsonasobj
====

jsonasobj is an extension to the core python json library that treats name/value pairs
as first class attributes whenever possible
"""
import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import jsonasobj


# with open('README.md') as file:
#     long_description = file.read()
long_description = """an extension to the core python json library that treats name/value pairs
as first class attributes whenever possible """

setup(
    name='jsonasobj',
    version=jsonasobj.__version__,
    description='JSON as python objects',
    long_description=long_description,
    author='Harold Solbrig',
    author_email='solbrig@jhu.edu',
    url='http://github.com/hsolbrig/jsonasobj',
    packages=['jsonasobj'],
    tests_require=['yadict-compare'],
    package_dir={'': 'src'},
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
