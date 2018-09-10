#!/usr/bin/env python3

import argparse
import os
import sys
import yaml

def main():
    try:
        import pkg_resources
        __version__ = pkg_resources.get_distribution('doker').version
    except Exception:
        __version__ = 'unknown'

    parser = argparse.ArgumentParser(prog='doker', usage='%(prog)s [options] <project>', add_help=False,
        description='Tool for creating beautiful PDF and HTML documentation.')
    parser.add_argument('project', metavar='<project>', help='Project file in YAML format')
    parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__, help='Show version and exit')
    parser.add_argument('--html', action="store_true", help='Generate documentation in HTML format')

    args = parser.parse_args()
    project_file = args.project

    if not os.path.isfile(project_file):
        project_file += '.yaml'
        if not os.path.isfile(project_file):
            print('Unable to open project file: ' + project_file, file=sys.stderr)
            sys.exit(1)
    
    with open(project_file, 'r') as stream:
        try:
            project = yaml.load(stream)
        except yaml.YAMLError as err:
            print('Error while parsing project file: ' + err, file=sys.stderr)
            sys.exit(1)

    current_dir = os.path.abspath(os.path.dirname(project_file))
    os.chdir(current_dir)
    entry_dir = os.path.abspath(project['entry'])

# Start
if __name__ == '__main__':
    main()
