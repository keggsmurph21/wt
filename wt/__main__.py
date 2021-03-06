import argparse
import os
import sys

from .WorktreeError import WorktreeError
from .Worktrees import Worktrees

def wt_use(cwd, args):
    trees = Worktrees(cwd)
    return trees.interpolate_path(args.branch, cwd)

def wt_list(cwd, args):
    trees = Worktrees(cwd)
    print(trees.pretty_print(args.all), file=sys.stderr)
    return os.getcwd()

def wt_add(cwd, args):
    trees = Worktrees(cwd)
    return trees.add(args.branch)

if __name__ == '__main__':

    try: # protect against -euo pipefail, since this file is run in a sourced command

        parser = argparse.ArgumentParser(prog='wt')
        subparsers = parser.add_subparsers(dest='cmd')

        list_parser = subparsers.add_parser('list')
        list_parser.add_argument('-a', '--all', action='store_true')
        list_parser.set_defaults(func=wt_list)

        use_parser = subparsers.add_parser('use')
        use_parser.add_argument('branch')
        use_parser.set_defaults(func=wt_use)

        add_parser = subparsers.add_parser('add')
        add_parser.add_argument('branch')
        add_parser.set_defaults(func=wt_add)

        try:
            args = parser.parse_args()
        except Exception as e:
            raise WorktreeError(str(e))

        if args.cmd is None:
            raise WorktreeError('missing required arg: cmd')

        cwd = os.getcwd()
        dest = args.func(cwd, args)

        print(dest)

    except Exception as e:
        print(str(e), file=sys.stderr)
        print(os.getcwd())


