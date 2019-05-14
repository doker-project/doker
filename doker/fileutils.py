# -*- coding: utf-8 -*-

import json
import re
import os
import sys
import tempfile
import yaml

from collections import OrderedDict
from . import log

def to_key(file):
    key = re.sub(r'^\d+-', '', file) # Remove number at the beginning
    key = re.sub(r'\..*$', '', key)  # Remove suffix
    return key

def get_tree(dir, file_type=''):
    file_tree = OrderedDict()
    files = os.listdir(dir)
    if files:
        files.sort()
    for file in files:
        file_path = dir + '/' + file
        if os.path.isfile(file_path) and not file.endswith(file_type):
            continue

        key = to_key(file)
        # TODO: Fix when 'key' is already exists in 'file_tree'
        if os.path.isdir(file_path):
            file_tree[key] = get_tree(file_path, file_type)
        else:
            file_tree[key] = file_path

    return file_tree

def readfile(filename):
    if sys.version_info[0] < 3:
        with open(filename, 'r') as f:
            text = f.read().decode('utf8')
    else:
        with open(filename, 'r', encoding='utf8') as f:
            text = f.read()
    return text

def stylesheet_to_tmp_json(stylesheet_file):
    if not os.path.isfile(stylesheet_file):
        log.error("Unable to open stylesheet file: '%s'", stylesheet_file)
        raise IOError('Stylesheet file error')
    with open(stylesheet_file, 'r') as f:
        try:
            style = yaml.full_load(f)
        except yaml.YAMLError as err:
            log.error("Parsing YAML style file failed: '%s'", err)
            raise

    tmp_json = tempfile.NamedTemporaryFile(mode='w+t', suffix='.json', delete=False)
    tmp_json.write(json.dumps(style))
    tmp_json.flush()

    return tmp_json

def to_list(file_tree):
  obj_list = []
  tree_branch(file_tree, None, 0, obj_list)
  return obj_list

def to_tree(file_list):
    file_tree = OrderedDict()
    for file in file_list:
        file_tree[to_key(file)] = file
    return file_tree

def tree_branch(file_tree, dir, level, obj_list):
    children = []
    for k in file_tree.keys():
        v = file_tree[k]
        obj = {'path' : (dir + '/' + k) if dir else k, 'level': level + 1 }
        if isinstance(v, OrderedDict):
            if 'index' in v:
                obj['src'] = v['index']
                obj_list.append(obj)
                obj['children'] = tree_branch(v, obj['path'], obj['level'], obj_list)
            else:
                tree_branch(v, obj['path'], obj['level'], obj_list)
        elif k != 'index':
            obj['src'] = v
            obj_list.append(obj)
            children.append(obj)

    return children