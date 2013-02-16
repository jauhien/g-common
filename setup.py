#!/usr/bin/env python

from distutils.core import setup

#from g_common.version import VERSION

setup(name          = 'g-common',
      version       = '0',
      description   = 'g-common repository manager',
      author        = 'Jauhien Piatlicki',
      author_email  = 'piatlicki@gmail.com',
      packages      = ['g_common'],
      scripts       = ['bin/g-common'],
      license       = 'GPL',
      )
