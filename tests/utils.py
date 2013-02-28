#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def get_pkgpath():
     root = __file__
     if os.path.islink(root):
         root = os.path.realpath(root)
     return os.path.dirname(os.path.abspath(root))

def cp_and_replace(src_path, dest_path, replace_list=[]):
    with open(src_path, 'r') as f:
        s = f.read()
    for i in replace_list:
        s = s.replace(i[0], i[1])
    with open(dest_path, 'w') as f:
        f.write(s)
