#!/usr/bin/env python

import argparse
import os
import sys
import yaml

from . import fileutils, generate, log

def merge_dicts(a, b):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key])
            elif a[key] == b[key]:
                pass
        else:
            a[key] = b[key]
    return a

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
    parser.add_argument('--pdf', action="store_true", help='Generate documentation in  Portable Document Format (PDF)')
    parser.add_argument('--html', action="store_true", help='Generate documentation in Hypertext Markup Language (HTML) format')
    parser.add_argument('--odt', action="store_true", help='Generate documentation in Open Document Text (ODT) format')

    args = parser.parse_args()
    project_file = args.project

    if not os.path.isfile(project_file):
        project_file += '.yaml'
        if not os.path.isfile(project_file):
            log.error("Unable to open project file: '%s'", project_file)
            sys.exit(1)

    with open(project_file, 'r') as f:
        try:
            project = yaml.full_load(f)
        except yaml.YAMLError as err:
            log.error("Parsing YAML project file failed: '%s'", err)
            sys.exit(1)
    current_dir = os.getcwd()
    os.chdir(os.path.abspath(os.path.dirname(project_file)))
    if not project:
        project = {}
    if not 'root' in project:
        project['root'] = '.'
    root_dir = os.path.abspath(project['root'])

    if 'parent' in project and os.path.isfile(project['parent']):
        with open(project['parent'], 'r') as f:
            try:
                parent = yaml.full_load(f)
            except yaml.YAMLError as err:
                log.error("Parsing YAML parent file failed: '%s'", err)
                sys.exit(1)
        merge_dicts(project, parent)

    file_type = '.rst' if (args.pdf or args.odt)  else ('.yaml' if args.html else '')
    file_tree = fileutils.to_tree(project['files']) if 'files' in project else fileutils.get_tree(root_dir, file_type)

    files = []
    if 'index' in file_tree:
        files.append({ 'path': '', 'src': file_tree['index'] })
    files = files + fileutils.to_list(file_tree)

    try:
        if args.pdf:
            default_pdf_name = os.path.splitext(os.path.basename(project_file))[0] + '.pdf'
            generate.pdf(files, project, os.path.join(current_dir, default_pdf_name))
        elif args.html:
            generate.html(files, project, current_dir)
        elif args.odt:
            default_odt_name = os.path.splitext(os.path.basename(project_file))[0] + '.odt'
            generate.odt(files, project, os.path.join(current_dir, default_odt_name))
        #elif 'script' in project:
            # TODO: Exec the script
        else:
            log.error('Either PDF (--pdf) or HTML (--html) format should be chosen\n')
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        if e:
            log.critical(e)
        sys.exit(1)

# Start
if __name__ == '__main__':
    main()
