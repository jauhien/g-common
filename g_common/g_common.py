#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from g_common.overlay import GCommon

def main():
    g_common = GCommon()
    return g_common()
    
if __name__ == "__main__":
    sys.exit(main())
