# -*- coding: utf-8 -*-

import re
import os

from doker import log

def to_key(file):
    key = re.sub(r'^\d+-', '', file) # Remove number at the beginning
    key = re.sub(r'\..*$', '', key)  # Remove suffix
    return key

def get_title(src):
    with open(src, 'r') as f:
        title = f.readline().strip()
    return title

def get_tree(dir, file_tree=None):
    files = os.listdir(dir)
    if not file_tree:
        file_tree = {}
    for file in files:
        file_path = dir + '/' + file
        if os.path.isfile(file_path) and not file.endswith('.rst'):
            continue

        key = to_key(file)
        if os.path.isdir(file_path):
            file_tree[key] = {}
            get_tree(file_path, file_tree)
            if not file_tree[key]:
                file_tree.pop(key, None)
        else:
            file_tree[key] = file_path

    return file_tree

def remove(file_list):
    for file in file_list:
        log.info("Removing temporary '%s'", os.path.basename(file))
        os.remove(file)

def to_list(file_tree):
  obj_list = []
  tree_branch(file_tree, None, 0, obj_list)
  return obj_list

def to_tree(file_list):
    file_tree = {}
    for file in file_list:
        file_tree[to_key(file)] = file
    return file_tree

def tree_branch(file_tree, dir, level, obj_list):
    children = []
    for k in file_tree.keys():
        v = file_tree[k]
        obj = {'path' : (dir + '/' + k) if dir else k, 'level': level + 1 }
        if isinstance(v, dict):
            obj['src'] = v['index']
            obj['title'] = get_title(obj['src'])
            obj_list.append(obj)
            obj.children = tree_branch(v, obj['path'], obj['level'], obj_list)
        elif k != 'index':
            obj['src'] = v
            obj['title'] = get_title(obj['src'])
            obj_list.append(obj)
            children.append(obj)

    return children