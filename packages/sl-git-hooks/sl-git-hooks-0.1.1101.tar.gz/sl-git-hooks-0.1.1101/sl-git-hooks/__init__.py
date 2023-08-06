#!/usr/bin/python

import argparse
import sys
import pygit2
import os

import hooks

import config


def main():
    argparser = argparse.ArgumentParser()

    subparsers = argparser.add_subparsers(dest="command", help='Command to run')

    run_parser = subparsers.add_parser('run', help='Run git hook')
    run_parser.add_argument('hook_type', help="Git hook type", choices=['commit-msg', 'pre-commit'])
    run_parser.add_argument('git_args', nargs='*')

    init_parser = subparsers.add_parser('init', help='Init project configuration for current git repository')
    init_parser.add_argument('-y', '--not-interactive', dest="not_interactive", action='store_true', help="Perform init not interactively (all default fields)")

    args = argparser.parse_args()

    if args.command == 'run':
        hook_type = args.hook_type

        if hook_type == 'pre-commit':
            sys.exit(hooks.precommitHandler())

    if args.command == 'init':
        try:
            repository = pygit2.Repository(os.getcwd())
        except Exception:
            print('Current path is not a repository')
            return sys.exit(1)

        config.generate_project_config(repository, not args.not_interactive)

    return sys.exit(0)


main()
