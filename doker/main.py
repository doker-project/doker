#!/usr/bin/env python

import argparse
import os
import re
import sys
import yaml
from rst2pdf.createpdf import RstToPdf

def page_tree(dir, tree=None):
    pages = os.listdir(dir)
    if not tree:
        tree = {}
    for page in pages:
        page_path = dir + '/' + page
        if os.path.isfile(page_path) and not page.endswith('.rst'):
            continue

        key = re.sub(r'^\d+-', '', page) # Remove number at the beginning
        key = re.sub(r'\..*$', '', key)  # Remove suffix

        if os.path.isdir(page_path):
            tree[key] = {}
            page_tree(page_path, tree)
        else:
            tree[key] = page_path

    return tree

def get_title(src):
    with open(src, 'r') as f:
        title = f.readline().strip()
    return title
    
def page_tree_branch(tree, dir, level, obj_list):
    children = []
    for k in tree.keys():
        v = tree[k]
        obj = {'path' : (dir + '/' + k) if dir else k, 'level': level + 1 }
        if isinstance(v, dict):
            obj['src'] = v['index']
            obj['title'] = get_title(obj['src'])
            obj_list.append(obj)
            obj.children = page_tree_branch(v, obj['path'], obj['level'], obj_list)
        elif k != 'index':
            obj['src'] = v
            obj['title'] = get_title(obj['src'])
            obj_list.append(obj)
            children.append(obj)

    return children

def page_list(tree):
  obj_list = []
  page_tree_branch(tree, None, 0, obj_list)
  return obj_list

def generate_html(project):
    return

def generate_pdf(project, output):
    entry_dir = os.path.abspath(project['entry'])

    tree = page_tree(entry_dir)
    pages = []
    if 'index' in tree:
        pages.append({ 'src': tree['index'] })
    pages = pages + page_list(tree)

    text = ''
    for page in pages:
        with open(page['src'], 'r') as f:
            text += f.read()
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
    parser.add_argument('--html', action="store_true", help='Generate documentation in HTML format')

    args = parser.parse_args()
    project_file = args.project

    if not os.path.isfile(project_file):
        project_file += '.yaml'
        if not os.path.isfile(project_file):
            sys.stderr.write('Unable to open project file: ' + project_file)
            sys.exit(1)
    
    with open(project_file, 'r') as stream:
        try:
            project = yaml.load(stream)
        except yaml.YAMLError as err:
            sys.stderr.write('Error while parsing project file: ' + err)
            sys.exit(1)
    current_dir = os.getcwd()
    os.chdir(os.path.abspath(os.path.dirname(project_file)))
    if not 'entry' in project:
        project['entry'] = '.'
    if args.html:
        generate_html(project)
    else:
        output_pdf = os.path.splitext(os.path.basename(project_file))[0] + '.pdf'
        generate_pdf(project, os.path.join(current_dir, output_pdf))

# Start
if __name__ == '__main__':
    main()
