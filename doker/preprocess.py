# -*- coding: utf-8 -*-

import os
import re

def common(text, dir, project):
    # Substitute fields by values
    if 'fields' in project:
        for field in project['fields']:
            text = re.sub(r'\#\#\#' + field + r'\#\#\#', str(project['fields'][field]), text, flags=re.I)
    # Make path to images absolute
    if 'images-root' in project:
        dir = os.path.abspath(project['images-root'])
    text = re.sub(r'((figure|image)::\S*\s+)([\w\/-]+\.(jpg|jpeg|pdf|png|svg))', r'\1'+ dir + r'/\3', text, flags=re.I|re.M)
    # Add extra EOL
    text += '\n\n'
    return text

def doctree(doctree, project):
    return doctree

def pdf(text, dir, project):
    return common(text, dir, project)

def html(text, dir, project):
    return common(text, dir, project)