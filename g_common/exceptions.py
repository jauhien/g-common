#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

class CommonError(Exception):
    """Base class for exceptions."""
    pass

class FileError(CommonError):
    def __init__(self, path, message):
        self.path = path
        self.message = message
        
    def __str__(self):
        return "File error: " + self.path + " : " + self.message

class OverlayError(CommonError):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return "Overlay error: " + self.message
