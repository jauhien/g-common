#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

CONFIGDIR = "/usr/share/g-common/drivers"

def get_cfgdir():
    return CONFIGDIR

def get_cfgfile(driver):
    return os.path.join(get_cfgdir(), driver + ".cfg")
