from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import snp500

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

#long_description = read('README.txt', 'CHANGES.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

from _version import __version__

setup(
    name='snp500',
    version=__version__,
    url='https://github.com/yangphysics/snp500',
    license='None',
    author='Shuxiang Yang',
    tests_require=['pytest'],
    install_requires=['pandas>=0.16.0',
                      'bs4>=4.3.2',
                    ],
    cmdclass={'test': PyTest},
    author_email='yangphysics@gmail.com',
    description='Python code to get a list of S&P 500 companies upto arbitrary date (back to year 2000)',
    #long_description=long_description,
    packages=['snp500'],
    include_package_data=True,
    platforms='any',
    #test_suite='snp500.test.test_snp500',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)

