#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse, hashlib

from pyparsing import *

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

class Manifest:
    def __init__(self, size = None, sha256 = None,
                 sha512 = None, whirlpool = None,
                 src = None):
        self.size = size
        self.sha256 = sha256
        self.sha512 = sha512
        self.whirlpool = whirlpool
        if not src is None:
            self.digest(src)

    def digest(self, src):
        h_sha256 = hashlib.new('SHA256')
        h_sha512 = hashlib.new('SHA512')
        h_whirlpool = hashlib.new('whirlpool')
        h_sha256.update(src)
        h_sha512.update(src)
        h_whirlpool.update(src)
        self.size = str(len(src))
        self.sha256 = h_sha256.hexdigest()
        self.sha512 = h_sha512.hexdigest()
        self.whirlpool = h_whirlpool.hexdigest()
        
#manifest parser

file_type = Suppress(Word(alphanums))
file_name = Word(alphanums + '_-+.')
size = Word(nums)
sha256 = Suppress(Literal('SHA256')) + Word(alphanums)
sha512 = Suppress(Literal('SHA512')) + Word(alphanums)
whirlpool = Suppress(Literal('WHIRLPOOL')) + Word(alphanums)
hashes = (size + sha256 + sha512 + whirlpool)\
         .setParseAction(lambda s, l, t: [Manifest(t[0], t[1], t[2], t[3])])
manifest = Dict(OneOrMore(Group(file_type + file_name + hashes)))

#end manifest parser
