# !usr/bin/env python
# -*- coding: UTF-8 -*-
"""
List all commands and arguments
"""
import sys
import argparse
from local.cmds.push.core import run as push_run


def push():
    parser = argparse.ArgumentParser(prog='push', description="git helper program")
    parser.add_argument("-v", "--verbose", action='store_true')

    args = parser.parse_args(sys.argv[2:])

    print 'verbose', args.verbose
    # push_run(sys.argv[2:])
    push_run()


# print sys.argv
# if sys.argv[1] == 'push':
#     push()
push()