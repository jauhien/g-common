#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, subprocess

from g_common.files import MethodConfig, OverlayConfig

class Overlay:
    def __init__(self, overlay, method=None):
        self.overlay = overlay
        self.name = os.path.split(overlay)[1]
        o_cfg = OverlayConfig(overlay)
        if method is not None:
            m_cfg = MethodConfig(method)
            m_cfg.read()
            self.exec = m_cfg.cfg['driver']['method']
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

    def sync(self, uri):
        print("g-common: syncing overlay " + self.name)
        self.uri = uri
        print([self.exec, self.overlay, 'sync', self.method, self.uri])
        subprocess.check_call([self.exec, self.overlay, 'sync', self.method, self.uri])
        o_cfg = OverlayConfig(self.overlay)
        o_cfg['overlay']['uri'] = self.uri
        o_cfg['overlay']['name'] = self.name

    def generate_tree():
        pass

class Driver:
    def __init__():
        pass
    
    def 
