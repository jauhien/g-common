#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, subprocess

from g_common.files import MethodConfig, OverlayConfig, RepoNameFile, TreeFile
from g_common.parsers import Command

class Overlay:
    def __init__(self, overlay, method=None):
        self.overlay = overlay
        self.name = os.path.split(overlay)[1]
        o_cfg = OverlayConfig(overlay)
        if method is not None:
            m_cfg = MethodConfig(method)
            m_cfg.read()
            self.exec = m_cfg.cfg['driver']['exec']
            try:
                o_cfg.read()
            except IOError as e:
                o_cfg.initialize(m_cfg.cfg)
            else:
                o_cfg.cfg['driver'] = m_cfg.cfg['driver']
                o_cfg.write()
            self.method = method
        else:
            o_cfg.read()
            self.exec = o_cfg.cfg['driver']['exec']
            self.method = o_cfg.cfg['driver']['method']

    def exec_command(self, args):
        return subprocess.check_output([self.exec, self.overlay] + args, universal_newlines=True)
            
    def sync(self, uri):
        print("g-common: syncing overlay " + self.name)
        self.uri = uri
        print(self.exec_command(['sync', self.method, self.uri]))
        o_cfg = OverlayConfig(self.overlay)
        o_cfg.read()
        o_cfg.cfg['overlay'] = {'uri':self.uri, 'name':self.name}
        o_cfg.write()
        return 0

    def generate_tree(self):
        print("g-common: populating tree")
        repo_name = RepoNameFile(self.overlay)
        repo_name.write()
        eclasses = self.eclass_list()
        for name in eclasses:
            print("g-common: eclass " + name)
            eclass = self.eclass_src(name)
            eclfile = TreeFile(self.overlay, 'eclass', name)
            eclfile.write(eclass)
        ebuilds = self.ebuild_list()
        for name in ebuilds:
            print("g-common: ebuild " + name[0] + "-" + name[1])
            ebuild = self.ebuild_src(name[0], name[1])
            eblfile = EbuildFile(self.overlay, name[0], name[1])
            eblfile.write(ebuild)
        return 0

    def eclass_list(self):
        st = self.exec_command(['eclass', 'list'])
        st = st.split("\n")
        st = [i for i in filter(None, st)]
        return st

    def eclass_src(self, name):
        eclass = self.exec_command(['eclass', 'src', name])
        return eclass

    def ebuild_list(self):
        st = self.exec_command(['ebuild', 'list'])
        st = st.split('\n')
        st = [i for i in filter(None, st)]
        for i in range(len(st)):
             st[i] = st[i].split(' ')
        return st

    def ebuild_src(self, name, version):
        ebuild = self.exec_command(['ebuild', 'src', name])
        return ebuild
    
    def license_list(self):
        return 0

    def license_src(self, name):
        return 0


class Driver:
    def __init__(self):
        self.cmd = Command('main', arguments=[('overlay', False)], subcommands=[
            ('sync', [('method', False), ('uri', False)], self.sync),
            ('eclass', [], [
                ('list', [], self.eclass_list),
                ('src', [('name', False)], self.eclass_src),
                ]),
            ('ebuild', [], [
                ('list', [], self.ebuild_list),
                ('src', [('name', False), ('version', False)], self.ebuild_src),
                ]),
            ('license', [], [
                ('list', [], self.license_list),
                ('src', [('name', False)], self.license_src),
                ]),
            ])

    def __call__(self, args=None):
        args = self.cmd.parse_args(args)
        args.action(args)
    
    def sync(self, args):
        return 0

    def eclass_list(self, args):
        return 0

    def eclass_src(self, args):
        return 0

    def ebuild_list(self, args):
        return 0

    def ebuild_src(self, args):
        return 0
    
    def license_list(self, args):
        return 0

    def license_src(self, args):
        return 0

