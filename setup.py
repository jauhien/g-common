#!/usr/bin/env python
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

from distutils.core import setup

from g_common.version import VERSION

setup(name          = 'g-common',
      version       = VERSION,
      description   = 'g-common repository manager',
      author        = 'Jauhien Piatlicki',
      author_email  = 'piatlicki@gmail.com',
      packages      = ['g_common'],
      scripts       = ['bin/g-common'],
      license       = 'GPL',
      )
