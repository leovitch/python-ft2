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
    version = '0.1',
    url = '',
    author = 'Ryan Coyner',
    author_email = 'rcoyner@gmail.com',
    description = 'A cross-platform implementation of description.',
    packages = packages,
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: X11 Applications',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                  ],
)
