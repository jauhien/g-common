#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, pickle, configparser

from g_common.exceptions import FileError

class File:
    def __init__(self, name, directory, cachedir):
        self.name = name
        self.directory = os.path.abspath(directory)
        self.path = os.path.join(self.directory, name)
        self.cachedir = os.path.abspath(cachedir)
        self.cachename = self.path.replace('/', '.')
        self.cachepath = os.path.join(self.cachedir, self.cachename)
        self.src = None
        self.mtime = 0

    def _read_src(self):
        with open(self.path, 'r') as f:
            self.src = f.read()

    def _write_src(self):
        with open(self.path, 'w') as f:
            f.write(self.src)

    def read(self):
        self._read_src()
        self.mtime = os.path.getmtime(self.path)

    def write(self):
        if self.src is None:
            raise FileError(self.path, 'nothing to write')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if os.path.exists(self.path) and \
               (self.mtime < os.path.getmtime(self.path)):
            raise FileError(self.path, 'modified on disk')
        self._write_src()
        self.mtime = os.path.getmtime(self.path)

    def read_cache(self):
        if not os.path.exists(self.cachepath):
            raise FileError(self.path, 'cache does not exist')
        if os.path.exists(self.path) and \
               (os.path.getmtime(self.cachepath) < os.path.getmtime(self.path)):
            raise FileError(self.path, 'old cache')
        with open(self.cachepath, 'br') as f:
            self.src = pickle.load(f)

    def write_cache(self):
        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)
        with open(self.cachepath, 'bw') as f:
            pickle.dump(self.src, f)

    def cached_read(self):
        try:
            self.read_cache()
        except Exception:
            self.read()
        try:
            self.write_cache()
        except Exception:
            pass

    def cached_write(self):
        self.write()
        try:
            self.write_cache()
        except Exception:
            pass

class TextFile(File):
    def _read_src(self):
        with open(self.path, 'r') as f:
            self.src = f.read().split('\n')
            if self.src[-1] == '':
                self.src = self.src[:-1]

    def _write_src(self):
        with open(self.path, 'w') as f:
            for line in self.src:
                f.write(line)
                f.write('\n')

class ConfigFile(File):
    def _read_src(self):
        if self.src is None:
            self.src = configparser.ConfigParser()
        if self.src.read(self.path) == []:
            raise FileError(self.path, 'config file does not exist')

    def _write_src(self):
        with open(self.path, 'w') as f:
            self.src.write(f)
