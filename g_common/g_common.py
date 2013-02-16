#!/usr/bin/python
# -*- coding: utf-8 -*-

from g_common.parsers import parse_args, Argument, Arguments, Command_group, Command, \
     parse_config, write_config

def sync(args):
    print("syncing")
    return 0

def generate_tree(args):
    print("generating tree")
    return 0

def main():
    args = Arguments([Argument('overlay', 1)],
                     [Command('sync', 'sync overlay', [Argument('method', 1), Argument('url', 1)], sync),
                      Command('generate-tree', 'generate tree', [], generate_tree)])
    args = parse_args(args)
    return args.func(args)
    
if __name__ == "__main__":
    sys.exit(main())
