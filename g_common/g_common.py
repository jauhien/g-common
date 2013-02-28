#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

import sys

from g_common.overlay import GCommon

def main():
    g_common = GCommon()
    return g_common()
    
if __name__ == "__main__":
    sys.exit(main())
