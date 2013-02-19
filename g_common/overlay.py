#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, subprocess

from g_common.parsers import Command
from g_common.exceptions import OverlayError
from g_common.files import ConfigFile

class Overlay:
    def __init__(self):
        self.cmd = Command('main', arguments=[('overlay', False)], subcommands=[
            ('sync', [('method', False), ('uri', False)], self.sync),
            ('generate-tree', [], self.generate_tree),
            ])
        self.overlay = None

    def __call__(self):
        args = self.cmd.parse_args(args)
        return args.action(args)

    def run_command(self, cmd, args):
        flag = True
        if not os.path.exists(cmd):
            flag = False
            for d in os.environ['PATH'].split(os.pathsep):
                f = os.path.join(d, cmd)
                if os.path.exists(f):
                    flag = True
                    break
        if not flag:
            raise OverlayError("command " + cmd + " not found")
        cmd = [cmd,] + args
        return subprocess.check_output(cmd, universal_newlines=True)

    def sync(self, args):
        return 0

    def generate_tree(self, args):
        return 0

class GCommon(Overlay):
    def __init__(self):
        super().__init__()
        self.configdir = "/usr/share/g-common/drivers"
        self.datadir = ".g-common"
        self.cfgfile = "overlay.cfg"

    def sync(self, args):
        overlay = args.overlay
        method = args.method
        uri = args.uri
        datadir = os.path.join(overlay, self.datadir)
        m_cfg = ConfigFile(method + '.cfg', self.configdir, datadir)
        try:
            m_cfg.cached_read()
            cmd = m_cfg.src['driver']['exec']
        except Exception:
            print('Error when reading config file for overlay type ' + method)
            return -1
        try:
            output = self.run_command(cmd, [overlay, 'sync', method, uri])
            print(output)
        except Exception:
            print('Error when executing: ' + " ".join([cmd, overlay, 'sync', method, uri]))
            return -1
        o_cfg = ConfigFile(self.cfgfile, datadir, datadir)
        o_cfg['overlay'] = {'method' : method, 'uri' : uri, 'exec' : cmd}
        try:
            o_cfg.cached_write()
        except Exception:
            print ('Error when writing overlay config')
            return -1
        return 0

    def generate_tree(self, args):
        overlay = args.overlay
        datadir = os.path.join(overlay, self.datadir)
        o_cfg = ConfigFile(self.cfgfile, datadir, datadir)
        try:
            o_cfg.cached_read()
            cmd = m_cfg.src['overlay']['exec']
        except Exception:
            print('Error when writing overlay config')
            return -1
        try:
            output = self.run_command(cmd, [overlay, 'generate-tree'])
            print(output)
        except Exception:
            print('Error when executing: ' + " ".join([cmd, overlay, 'generate-tree']))
            return -1
        return 0

class Driver(Overlay):
    def __init__(self):
        super().__init__()
