import os
import sys


def find_gits(dir):
    """returns a list of .git dirs relative to dir.
    These dirs may be below (if dir is a workspace) or above dir (if dir is within a git project)."""
    found = False
    while True:
        git_dir = os.path.join(dir, '.git')
        if os.path.isdir(git_dir):
            found = True
            break

        dir = os.path.abspath(os.path.join(dir, '..'))
        if len(dir) < 5: # TODO: Fix this, should be :is_root(dir)
            break

    if found:
        print '.git dir found:', git_dir
    else:
        # now check any subdirectories for .git folders. If any are found, assume cwd is a workspace
        files = os.listdir(dir)
        for f in files:
            p = os.path.join(dir, f)
            if os.path.isdir(p) and os.path.isdir(os.path.join(p, '.git')):
                print 'This is a workspace!!'
                sys.exit(0)

        print 'No git dir found! Please run flow in a valid workspace'


dir = r"D:\zhaochang\example_project\bp\bp\pylib\bp"
print 'program is running in {}'.format(dir)

find_gits(dir)