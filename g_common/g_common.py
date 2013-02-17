#!/usr/bin/python
# -*- coding: utf-8 -*-

from g_common.parsers import Command

def sync(args):
    print("sync")
    return 0

def generate_tree(args):
    print("generating tree")
    return 0

def main():
    cmd = Command('main', arguments=[('overlay', False)], subcommands=[
        ('sync', [('method', False), ('uri', False)], sync),
        ('generate-tree', [], generate_tree),
        ])
    args = cmd.parse_args()
    args.action(args)
    
if __name__ == "__main__":
    sys.exit(main())
