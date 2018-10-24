# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
List all commands and arguments
"""
import sys
import argparse
from local.cmds.push.core import push_prepare_parser


def update(args):
    print "update"


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='flow')
    subparsers = parser.add_subparsers()

    # create the parser for the "push" command
    parser_push = subparsers.add_parser('push')
    push_prepare_parser(parser_push)

    # create the parser for the "update" command
    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('z')
    parser_update.set_defaults(func=update)

    # parser.print_help()
    # parse the args and call whatever function was selected
    print sys.argv
    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == '__main__':
    main()