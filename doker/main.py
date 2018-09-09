#!/usr/bin/env python3

import argparse

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
    parser.add_argument('--pdf', action="store_true", help='Generate documentation in PDF format (default)')
    parser.add_argument('--html', action="store_true", help='Generate documentation in HTML format')
 
    args = parser.parse_args()
    print(args)

# Start
if __name__ == '__main__':
    main()
