#! /usr/bin/env python
from distutils.core import setup

import os


def fullsplit(path, result=None):
    """Split a pathname into components (the opposite of os.path.join)."""
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

packages = []
root_dir = os.path.dirname(__file__).join('python-ft2')

for dirpath, dirname, filename in os.walk(root_dir):
    if '__init__.py' in filename:
        packages.append('.'.join(fullsplit(dirpath)))

setup(
    name = 'python-ft2',
    version = '0.3',
    url = '',
    author = 'Leo Hourvitz',
    author_email = 'leovitch@gmail.com',
    description = 'A ctypes-based wrapper for the libfreetype library.',
    packages = packages,
    classifiers = ['Development Status :: 2 - Beta',
                   'Environment :: cross-platform',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                  ],
)
