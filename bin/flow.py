# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
List all flow sub-commands and arguments
"""
import sys
import argparse
from local.cmds.push.core import prepare_push_parser
from local.cmds.update.core import prepare_update_parser


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='flow')
    subparsers = parser.add_subparsers()

    # create the parser for the "push" sub-command
    push_parser = subparsers.add_parser('push')
    prepare_push_parser(push_parser)

    # create the parser for the "update" sub-command
    update_parser = subparsers.add_parser('update')
    prepare_update_parser(update_parser)

    # parser.print_help()
    # parse the args and call whatever function was selected
    print sys.argv
    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == '__main__':
    main()
