#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

import os, shutil, stat, tempfile, unittest

from g_common.overlay import GCommon

from utils import get_pkgpath, cp_and_replace

class TestGCommon(unittest.TestCase):
    """Test g_common.overlay.GCommon"""

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.overlay = os.path.join(self.workdir, "test_overlay")
        self.datadir = 'data'
        self.method = 'test'
        self.uri = 'test://test'
        self.testcfg = 'test.cfg'
        self.testsh = 'test.sh'
        self.tstargs = os.path.join(self.workdir, 'tst.args')
        os.makedirs(self.overlay)
        self.testcfg_dest = None
        self.testsh_dest = None
        self.sync_args = [self.overlay, 'sync', self.method, self.uri]
        self.generate_tree_args = [self.overlay, 'generate-tree']
        self.create_test_driver()
        self.g_common = GCommon()
        self.g_common.configdir = self.workdir

    def create_test_driver(self):
        datadir = os.path.join(get_pkgpath(), self.datadir)
        testcfg = os.path.join(datadir, self.testcfg)
        self.testcfg_dest = os.path.join(self.workdir, self.testcfg)
        self.testsh_dest = os.path.join(self.workdir, self.testsh)
        testsh = os.path.join(datadir, self.testsh)
        cp_and_replace(testcfg, self.testcfg_dest, [['<EXEC>', self.testsh_dest]])
        cp_and_replace(testsh, self.testsh_dest)
        os.chmod(self.testsh_dest, stat.S_IEXEC | stat.S_IWRITE | stat.S_IREAD)

    def remove_test_driver(self):
        os.remove(self.testcfg_dest)
        os.remove(self.testsh_dest)

    def test(self):
        self.assertEqual(self.g_common(self.sync_args), 0)
        with open(self.tstargs, 'r') as f:
            s = f.read()
        self.assertEqual(s.replace('\n',''),
                         "".join(self.sync_args))
        self.assertEqual(self.g_common(self.generate_tree_args), 0)
        with open(self.tstargs, 'r') as f:
            s = f.read()
        self.assertEqual(s.replace('\n',''),
                         "".join(self.generate_tree_args))

    def tearDown(self):
        os.remove(self.tstargs)
        shutil.rmtree(os.path.join(self.overlay, self.g_common.datadir))
        self.remove_test_driver()
        os.rmdir(self.overlay)
        os.rmdir(self.workdir)
