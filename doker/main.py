#!/usr/bin/env python

import argparse
import os
import re
import sys
import yaml
from rst2pdf.createpdf import RstToPdf

def file_tree(dir, tree=None):
    files = os.listdir(dir)
    if not tree:
        tree = {}
    for file in files:
        file_path = dir + '/' + file
        if os.path.isfile(file_path) and not file.endswith('.rst'):
            continue

        key = re.sub(r'^\d+-', '', file) # Remove number at the beginning
        key = re.sub(r'\..*$', '', key)  # Remove suffix

        if os.path.isdir(file_path):
            tree[key] = {}
            file_tree(file_path, tree)
        else:
            tree[key] = file_path

    return tree

def get_title(src):
    with open(src, 'r') as f:
        title = f.readline().strip()
    return title
    
def file_tree_branch(tree, dir, level, obj_list):
    children = []
    for k in tree.keys():
        v = tree[k]
        obj = {'path' : (dir + '/' + k) if dir else k, 'level': level + 1 }
        if isinstance(v, dict):
            obj['src'] = v['index']
            obj['title'] = get_title(obj['src'])
            obj_list.append(obj)
            obj.children = file_tree_branch(v, obj['path'], obj['level'], obj_list)
        elif k != 'index':
            obj['src'] = v
            obj['title'] = get_title(obj['src'])
            obj_list.append(obj)
            children.append(obj)

    return children

def file_list(tree):
  obj_list = []
  file_tree_branch(tree, None, 0, obj_list)
  return obj_list

def preprocess(text, project):
    return text

def generate_html(files, project):
    return

def generate_pdf(files, project, output):
    text = ''
    for file in files:
        with open(file['src'], 'r') as f:
            text += preprocess(f.read(), project)
    print('Generating "' + os.path.basename(output) + '"')
    RstToPdf().createPdf(text=text, output=output)

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
    parser.add_argument('--pdf', action="store_true", help='Generate documentation in PDF format')
    parser.add_argument('--html', action="store_true", help='Generate documentation in HTML format')

    args = parser.parse_args()
    project_file = args.project

    if not os.path.isfile(project_file):
        project_file += '.yaml'
        if not os.path.isfile(project_file):
            sys.stderr.write('Error: Unable to open project file: ' + project_file + '\n')
            sys.exit(1)
    
    with open(project_file, 'r') as stream:
        try:
            project = yaml.load(stream)
        except yaml.YAMLError as err:
            sys.stderr.write('Error: Parsing YAML project file failed: ' + err + '\n')
            sys.exit(1)
    current_dir = os.getcwd()
    os.chdir(os.path.abspath(os.path.dirname(project_file)))
    if not 'entry' in project:
        project['entry'] = '.'
    entry_dir = os.path.abspath(project['entry'])

    tree = file_tree(entry_dir)
    files = []
    if 'index' in tree:
        files.append({ 'src': tree['index'] })
    files = files + file_list(tree)

    if args.pdf:
        output_pdf = os.path.splitext(os.path.basename(project_file))[0] + '.pdf'
        generate_pdf(files, project, os.path.join(current_dir, output_pdf))
    elif args.html:
        generate_html(files, project)
    #elif 'script' in project:
        # TODO: Exec the script
    else:
        sys.stderr.write('Error: Either PDF (--pdf) or HTML (--html) format should be chosen\n\n')
        parser.print_help()
        sys.exit(1)

# Start
if __name__ == '__main__':
    main()
