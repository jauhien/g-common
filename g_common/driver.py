#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

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

    def sync(url):
        print("g-common: syncing overlay " + name)
