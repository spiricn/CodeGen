#!/usr/bin/env python

from distutils.core import setup

setup(name='CodeGen',
      version='1.0',
      description='Code generator tool',
      author='Nikola Spiric',
      author_email='nikola.spiric.ns@gmail.com',
      package_dir={'codegen' : 'src'},
      packages=['codegen'],
)