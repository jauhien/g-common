#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse

#arguments parser

class Argument:
    def __init__(self, name, optional=False, argparser=None):
        self.name = name
        self.optional = optional
        self.argparser = argparser
        if (self.argparser == None):
            self.argparser = argparse.ArgumentParser()
        nargs = None
        if (self.optional):
            nargs = '?'
        self.argparser.add_argument(self.name, nargs=nargs)

    def parse_args(self, args=None, namespace=None):
        return self.argparser.parse_args(args, namespace)


class Command:
    def __init__(self, name, arguments=None, action=None, subcommands=None, argparser=None):
        self.name = name
        self.action = action
        self.argparser = argparser
        if (self.argparser == None):
            self.argparser = argparse.ArgumentParser()
        self.arguments = []
        for arg in arguments:
            self.arguments.append(Argument(arg[0], optional=arg[1], argparser=self.argparser))
        self.subparsers = None
        self.subcommands = []
        if (self.action == None) and (subcommands != None):
            self.subparsers = self.argparser.add_subparsers()
            for cmd in subcommands:
                nm = cmd[0]
                subparser = self.subparsers.add_parser(nm)
                args = cmd[1]
                act = None
                sub = None
                if (hasattr(cmd[2], '__call__')):
                    act = cmd[2]
                else:
                    sub = cmd[2]
                self.subcommands.append(Command(nm, arguments=args, action=act,
                                                subcommands=sub, argparser=subparser))
        elif (self.action != None):
            self.argparser.set_defaults(action=action)
        else:
            raise Exception
    
    def parse_args(self, args=None, namespace=None):
        return self.argparser.parse_args(args, namespace)

#end arguments parser
