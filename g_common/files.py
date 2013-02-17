#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser

CONFIGDIR = "/usr/share/g-common/drivers"
DATADIR = ".g-common"
CFGFILE = "overlay.cfg"

class ConfigFile:
    def __init__(self, directory, name):
        self.name = name
        self.directory = directory
        self.path = os.path.join(directory, name)
        self.cfg = ConfigParser()

    def initialize(self, cfg):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.cfg = ConfigParser()
        for sec_name, sec_val in cfg.items():
            self.cfg[sec_name] = sec_val
        with open(self.path, 'w') as configfile:
            self.cfg.write(configfile)

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(self.path, 'w') as configfile:
            self.cfg.write(configfile)

    def read(self):
        if (self.cfg.read(self.path) == []): raise IOError

class MethodConfig(ConfigFile):
    def __init__(self, method):
        super().__init__(CONFIGDIR, method + ".cfg")


class OverlayConfig(ConfigFile):
    def __init__(self, overlay):
        super().__init__(os.path.join(overlay, DATADIR), CFGFILE)
