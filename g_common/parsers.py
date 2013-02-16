#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections, argparse

#arguments parser

Argument = collections.namedtuple("Argument", "arg nargs")
Arguments = collections.namedtuple("Arguments", "args sub")
Command_group = collections.namedtuple("Command_group", "command help args sub")
Command = collections.namedtuple("Command", "command help args func")

def create_argsubparser(subparsers, command):
    subparser = subparsers.add_parser(command.command, help=command.help)
    for arg in command.args:
        subparser.add_argument(arg.arg, nargs=arg.nargs)

    if type(command) is Command:
        subparser.set_defaults(func=command.func)
    elif type(command) is Command_group:
        if command.sub != []:
            nextparsers = subparser.add_subparsers()
        for sub in command.sub:
            create_argsubparser(nextparsers, sub)
    else:
        raise Exception
    return subparser        

def create_argparser(arguments):
    if not type(arguments) is Arguments:
        raise Exception
    parser = argparse.ArgumentParser()
    for arg in arguments.args:
        parser.add_argument(arg.arg, nargs=arg.nargs)
    if arguments.sub != []:
        subparsers = parser.add_subparsers()
    for sub in arguments.sub:
        create_argsubparser(subparsers, sub)

    return parser

def parse_args(args):
    return create_argparser(args).parse_args()
            
#end arguments parser

#config parser

def parse_config(f):
    config = configparser.ConfigParser()
    config.read(f)
    cfg = {}
    for sn, sc in config.items():
        sec = {}
        for n, v in sc.items():
            sec[n] = v
        cfg[sn] = sec
    return cfg
    

def write_config(f, cfg):
    config = configparser.ConfigParser()
    for sect, sets in cfg.items():
        config[sect] = sets
    with open(f, 'w') as configfile:
        config.write(configfile)
    return 0

#end config parser
