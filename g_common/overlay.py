#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Copyright:
#             (c) 2013 Jauhien Piatlicki
#             Distributed under the terms of the GNU General Public License v2
#
# Author(s):
#             Jauhien Piatlicki <piatlicki@gmail.com>

import glob, os, subprocess

from g_common.parsers import Command
from g_common.exceptions import OverlayError
from g_common.files import ConfigFile, TextFile, ManifestFile

class Overlay:
    def __init__(self):
        self.cmd = Command('main', arguments=[('overlay', False)], subcommands=[
            ('sync', [('method', False), ('uri', False)], self.sync),
            ('generate-tree', [], self.generate_tree),
            ])
        self.overlay = None

    def __call__(self, args=None):
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
        subprocess.check_call(cmd, universal_newlines=True)

    def sync(self, args):
        return 0

    def generate_tree(self, args):
        return 0

class GCommon(Overlay):
    """The main class in g-common."""
    def __init__(self):
        super().__init__()
        self.configdir = "/usr/share/g-common/drivers" #directory for drivers' configs
        #layman uses these configs to test whether overlay is supported

        self.datadir = ".g-common"   #directory in an overlay used by g-common
        self.cfgfile = "overlay.cfg" #config of an overlay

    def sync(self, args):
        """Do all the synchronization with online repo. No tree generation here.

        args should contain next fields:
        overlay -- overlay directory
        method -- type of repository (method of sync/generate tree)
        uri -- uri of repository

        This function just reads a name of executable from an appropriate config file
        and calls it with the same arguments (cmd <overlay> sync <method> <uri>).
        """
        overlay = args.overlay
        method = args.method
        uri = args.uri
        datadir = os.path.join(overlay, self.datadir)
        m_cfg = ConfigFile(method + '.cfg', self.configdir, datadir)
        try:
            m_cfg.cached_read()
            cmd = m_cfg.src['driver']['exec']
        except Exception as ex:
            print('Error when reading config file for overlay type ' + method + ': ' +
                  str(ex))
            return -1
        try:
            self.run_command(cmd, [overlay, 'sync', method, uri])
        except Exception as ex:
            print('Error when executing ' + " ".join([cmd, overlay, 'sync', method, uri]) + ': ' +
                  str(ex))
            return -1
        o_cfg = ConfigFile(self.cfgfile, datadir, datadir)
        try:
            o_cfg.cached_read()
        except Exception as ex:
            print('Info: ' + str(ex))
        o_cfg.src['overlay'] = {'method' : method, 'uri' : uri, 'exec' : cmd}
        try:
            o_cfg.cached_write()
        except Exception as ex:
            print ('Error when writing overlay config: ' + str(ex))
            return -1
        return 0

    def generate_tree(self, args):
        """Generate ebuilds and other stuff. No Internet connections here.

        args should contain next fields:
        overlay -- overlay directory

        This function just reads a name of executable from an appropriate config file
        and calls it with the same arguments (cmd <overlay> generate-tree).
        """
        overlay = args.overlay
        datadir = os.path.join(overlay, self.datadir)
        o_cfg = ConfigFile(self.cfgfile, datadir, datadir)
        try:
            o_cfg.cached_read()
            cmd = o_cfg.src['overlay']['exec']
        except Exception as ex:
            print('Error when reading overlay config: ' + str(ex))
            return -1
        try:
            self.run_command(cmd, [overlay, 'generate-tree'])
        except Exception as ex:
            print('Error when executing ' + " ".join([cmd, overlay, 'generate-tree']) + ": " +
                  str(ex))
            return -1
        return 0

class Driver(Overlay):
    """A base class for g-drivers.

    It is aimed to simplify creation of g-drivers.
    It supports only the simplest overlays now:
    only ebuilds, eclasses and repo_name in the overlay tree.
    If you want more, write your g-driver from scratch
    or improve this class )).

    To create new g-driver inherit this class and implement
    your own function:

    sync -- sync with online repo
    list_eclasses -- list eclasses in overlay
    get_eclass -- get a given eclass source code
    list_ebuilds -- list ebuilds in overlay
    get_ebuild -- get a given ebuild source code

    Then create an instance of your class and call it
    with appropriate arguments. If no arguments given,
    it will use those from the command line.

    Example:
    class GDriver(Driver):
        #usefull code here
    g_driver = GDriver()
    g_driver()
    """
    def __init__(self):
        super().__init__()

    def sync(self, args):
        """Do all the synchronization with online repo. No tree generation here.

        args will contain next fields:
        overlay -- overlay directory
        method -- type of repository (method of sync/generate tree)
        uri -- uri of repository

        To be implemented in g-driver.
        """
        return 0

    def generate_tree(self, args):
        """Generate ebuilds and other stuff. No Internet connections here.

        args will contain next fields:
        overlay -- overlay directory

        This function does all the work with the overlay tree.
        It calls list_ebuilds, get_ebuild, list_eclasses and get_eclass functions.
        """
        self.overlay = os.path.abspath(args.overlay)
        self.name = os.path.split(self.overlay)[1]
        for f in glob.glob(os.path.join(self.overlay, "*")):
            self.run_command('rm', ['-rf', f])
        repo_name = TextFile('repo_name', os.path.join(self.overlay, 'profiles'))
        repo_name.src = [self.name]
        repo_name.write()
        eclasses = self.list_eclasses()
        for eclass in eclasses:
            eclass_file = TextFile(eclass + '.eclass', os.path.join(self.overlay, 'eclass'))
            eclass_file.src = self.get_eclass(eclass)
            eclass_file.write()
        ebuilds = self.list_ebuilds()
        for ebuild in ebuilds:
            ebuilddir = os.path.join(self.overlay, ebuild[0])
            ebuilddir = os.path.join(ebuilddir, ebuild[1])
            ebuild_file = TextFile(ebuild[1] + '-' + ebuild[2] + '.ebuild',
                                   ebuilddir)
            ebuild_file.src = self.get_ebuild(ebuild)
            ebuild_file.write()
            manifest = ManifestFile(ebuilddir)
            manifest.digest()
        return 0

    def list_eclasses(self):
        """Return a list of eclass names (strings).

        To be implemented in g-driver.
        """
        return []

    def get_eclass(self, eclass):
        """Return source code of a given eclass as list of lines.

        To be implemented in g-driver.
        """
        return []

    def list_ebuilds(self):
        """Return a list of ebuilds.

        Each list entry is a tuple (category, name, version).
        To be implemented in g-driver.
        """
        return []

    def get_ebuild(self, ebuild):
        """Return source code of a given ebuild as list of lines.

        Argument is a tuple (category, name, version).
        To be implemented in g-driver.
        """
        return []
