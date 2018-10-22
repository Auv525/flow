# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
List all commands and arguments
"""
import sys
import argparse
from local.cmds.push.core import run as push_run

# parser = argparse.ArgumentParser(prog='flow', description="git workflow tool")
# parser.add_argument("-v", "--verbose", action='store_true')
# subparsers = parser.add_subparsers(help='sub-commands')
# parser_push = subparsers.add_parser('push', help='flow push')
# parser_push.add_argument("-p", type=str, help="projects")
# parser_update = subparsers.add_parser('update', help='flow update')
#
#
# parser.parse_args(['push', '--help'])
#
# parser.print_help()
# print 'verbose', args.verbose
# print sys.argv


def push(args):
    push_run()


def update(args):
    print "update"


# create the top-level parser
parser = argparse.ArgumentParser(prog='flow')
subparsers = parser.add_subparsers(dest='subparser_name')

# create the parser for the "foo" command
parser_foo = subparsers.add_parser('push')
parser_foo.add_argument('-v', "--verbose", action="store_true", default=False, dest="verbose")
parser_foo.set_defaults(func=push)

# create the parser for the "bar" command
parser_bar = subparsers.add_parser('update')
parser_bar.add_argument('z')
parser_bar.set_defaults(func=update)

# parser.print_help()
# parse the args and call whatever function was selected
print sys.argv
args = parser.parse_args(sys.argv[1:])
args.func(args)
