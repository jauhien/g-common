#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, subprocess
from configparser import ConfigParser

CONFIGDIR = "/usr/share/g-common/drivers"
DATADIR = ".g-common"
CFGFILE = "overlay.cfg"
PROFILESDIR = "profiles"
REPONAMEFILE = "repo_name"

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

class RepoNameFile:
    def __init__(self, overlay):
        self.name = REPONAMEFILE
        self.directory = os.path.join(overlay, PROFILESDIR)
        self.path = os.path.join(directory, name)
        self.repo_name = os.path.split(overlay)[1]

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(self.path, 'w') as repo_name:
            repo_name.write(self.repo_name)
        return 0

class TreeFile:
    def __init__(self, overlay, directory, name):
        self.name = name
        self.directory = os.path.join(overlay, directory)
        self.path = os.path.join(self.directory, name)

    def write(self, src):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(self.path, 'w') as f:
            f.write(src)
        return 0

class EbuildFile(TreeFile):
    def __init__(self, overlay, name, version):
        super().__init__(overlay, name, name + '-' + version)

    def write(self, src):
        super().write(src)
        subprocess.check_call(['ebuild', self.path, 'manifest'])
        return 0
