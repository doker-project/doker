# -*- coding: utf-8 -*-

import docutils
import os
import re

class Emumerator(docutils.nodes.SparseNodeVisitor):
    def __init__(self, document, project):
        docutils.nodes.SparseNodeVisitor.__init__(self, document)
        self.project = project
        self.section_level = 0
        self.storage = {}
        self.refs = {}
        numbering = project['numbering'] if 'numbering' in project else None
        self.delimiter = numbering['delimiter'].decode('unicode-escape') if numbering and ('delimiter' in numbering) else ''
        self.space = numbering['space'].decode('unicode-escape') if numbering and ('space' in numbering) else ' '

    def visit_section(self, node):
        self.section_level += 1
        n = number('heading' + str(self.section_level), self.project, self.storage)
        if n:
            for child in node.children:
                if isinstance(child, docutils.nodes.title):                    
                    child.children[0] = docutils.nodes.Text(n + self.space + child.astext())
                    break

    def depart_section(self, node):
        self.section_level -= 1

    def visit_figure(self, node):
        n = number('figure', self.project, self.storage)
        if n:
            numbered = True
            if node.hasattr('ids'):
                for id in node['ids']:
                    self.refs[id] = n
                    if id.startswith('unnumbered'):
                        numbered = False
            if numbered:
                for child in node.children:
                    if isinstance(child, docutils.nodes.caption):                    
                        child.children[0] = docutils.nodes.Text(n + self.delimiter + self.space + child.astext())
                        break

    def visit_table(self, node):
        n = number('table', self.project, self.storage)
        if n:
            numbered = True
            if node.hasattr('ids'):
                for id in node['ids']:
                    self.refs[id] = n
                    if id.startswith('unnumbered'):
                        numbered = False
            if numbered:
                for child in node.children:
                    if isinstance(child, docutils.nodes.title):                    
                        child.children[0] = docutils.nodes.Text(n + self.delimiter + self.space + child.astext())
                        break

class ReferenceUpdater(docutils.nodes.SparseNodeVisitor):
    def __init__(self, document, refs):
        docutils.nodes.SparseNodeVisitor.__init__(self, document)
        self.refs = refs

    def visit_reference(self, node):
        if node.hasattr('refid'):
            refid = node['refid']
            if refid in self.refs:
                node.children[0] = docutils.nodes.Text(self.refs[refid])


def common(text, dir, project):
    # Substitute fields by values
    if 'fields' in project:
        for field in project['fields']:
            text = re.sub(r'\#\#\#' + field + r'\#\#\#', str(project['fields'][field]), text, flags=re.I)
            text = re.sub(r'\#\{' + field + r'\}', str(project['fields'][field]), text, flags=re.I)
    # Make path to images absolute
    if 'images-root' in project:
        dir = os.path.abspath(project['images-root'])
    dir = dir.replace('\\', '/')
    text = re.sub(r'((figure|image)::\S*\s+)([\w\d\/\\-]+\.(jpg|jpeg|pdf|png|svg))', r'\1' + dir + r'/\3', text, flags=re.I|re.M)

    # Add extra EOL
    text += '\n\n'
    return text

def doctree(doctree, project):
    if 'numbering' in project:
        e = Emumerator(doctree, project)
        doctree.walkabout(e)
        ru = ReferenceUpdater(doctree, e.refs)
        doctree.walk(ru)
    return doctree

def html(text, dir, project):
    return common(text, dir, project)

def number(tag, project, storage):
    result = None
    if 'numbering' in project:
        numbering = project['numbering']
        if tag in numbering:
            template = numbering[tag]
            patterns = [r'\(((\w+)(?:([\+\-\=])(\d+)?)?)\)',
                r'\[((\w+)(?:([\+\-\=])(\d+)?)?)\]',]
            for pattern in patterns:
                m = re.search(pattern, template, re.I)
                while m:
                    var = m.group(2)
                    operation = m.group(3)
                    operand = m.group(4)
                    value = storage[var] if var in storage else 0
                    if operation == '+':
                        value += int(operand) if operand else 1
                    if operation == '-':
                        value -= int(operand) if operand else 1
                    elif operation == '=':
                        value = int(operand) if operand else 0
                    storage[var] = value
                    number = str(value) if pattern.startswith('\(') else ''
                    template = re.sub(pattern, number, template, 1)                
                    m = re.search(pattern, template, re.I)

            result = template

    return result

def pdf(text, dir, project):
    return common(text, dir, project)