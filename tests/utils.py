#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

import os, subprocess

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

def test_file(path, src):
     with open(path, 'r') as f:
            s = f.read()
     return (s.replace('\n','') == "".join(src))

def test_manifest(directory):
     with open(os.path.join(directory, 'Manifest'), 'r') as f:
          s = f.read()
     s = s.split('\n')
     cd = os.getcwd()
     os.chdir(directory)
     subprocess.check_call(['repoman', 'manifest'])
     with open(os.path.join(directory, 'Manifest'), 'r') as f:
          c = f.read()
     c = c.split('\n')
     os.chdir(cd)
     flag = True
     for i in s:
          flag = flag and (i in c)
     return flag
