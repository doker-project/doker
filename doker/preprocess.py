# -*- coding: utf-8 -*-

from docutils import nodes
import os
import re
import sys

class Enumerator(nodes.SparseNodeVisitor):
    def __init__(self, document, project):
        nodes.SparseNodeVisitor.__init__(self, document)
        self.project = project
        self.section_level = 0
        self.list_level = 0
        self.storage = {}
        self.refs = {}
        numbering = project['numbering'] if 'numbering' in project else None
        self.suffix = numbering['suffix'] if numbering and ('suffix' in numbering) else None

        self.figure_suffix = numbering['figure-suffix'] if numbering and ('figure-suffix' in numbering) else None
        if self.figure_suffix is None:
            self.figure_suffix = self.suffix

        self.table_suffix = numbering['table-suffix'] if numbering and ('table-suffix' in numbering) else None
        if self.table_suffix is None:
            self.table_suffix = self.suffix

        self.list_suffix = numbering['list-suffix'] if numbering and ('list-suffix' in numbering) else None
        if self.list_suffix is None:
            self.list_suffix = self.suffix
        self.space = numbering['space'] if numbering and ('space' in numbering) else ' '

    def __process_list_in_children(self, children):
        for child in children:
            if isinstance(child, nodes.enumerated_list):
                self.visit_enumerated_list(child)
            elif len(child.children):
                self.__process_list_in_children(child.children)

    def visit_section(self, node):
        self.section_level += 1
        n = number('heading' + str(self.section_level), self.project, self.storage)
        if n:
            for child in node.children:
                if isinstance(child, nodes.title):
                    child.children[0] = nodes.Text(n + self.space + child.astext())
                    break

    def depart_section(self, node):
        self.section_level -= 1

    def visit_figure(self, node):
        n = number('figure', self.project, self.storage)
        if n:
            numbered = True
            if node.hasattr('ids'):
                for node_id in node['ids']:
                    self.refs[node_id] = n
                    if node_id.startswith('unnumbered'):
                        numbered = False
            if numbered:
                suffix = self.figure_suffix if self.figure_suffix != None else ''
                for child in node.children:
                    if isinstance(child, nodes.caption):
                        child.children[0] = nodes.Text(n + suffix + self.space + child.astext())
                        break

    def visit_table(self, node):
        n = number('table', self.project, self.storage)
        if n:
            numbered = True
            if node.hasattr('ids'):
                for node_id in node['ids']:
                    self.refs[node_id] = n
                    if node_id.startswith('unnumbered'):
                        numbered = False
            if numbered:
                suffix = self.table_suffix if self.table_suffix != None else ''
                for child in node.children:
                    if isinstance(child, nodes.title):
                        child.children[0] = nodes.Text(n + suffix + self.space + child.astext())
                        break

    def visit_enumerated_list(self, node):
        children = []
        for child in node.children:
            if isinstance(child, nodes.list_item) and len(child.children):
                children.append(child)
        if not len(children):
            return
        suffix = self.list_suffix if self.list_suffix != None else ''
        self.list_level += 1
        n = number('list' + str(self.list_level), self.project, self.storage)
        if n:
            if node.hasattr('ids'):
                for node_id in node['ids']:
                    self.refs[node_id] = n
            newnode = nodes.table()
            newnode['classes'] = ['item-list']
            tgroup = nodes.tgroup(cols=2)
            newnode += tgroup
            tbody = nodes.tbody()
            tgroup += tbody
            i = 0
            for child in children:
                self.__process_list_in_children(child.children)
                trow = nodes.row()
                tbody += trow
                tentry1 = nodes.entry()
                trow += tentry1
                tpar = nodes.paragraph(text=n + suffix)
                tpar['classes'] = ['item-list-number']
                tentry1 += tpar
                tentry2 = nodes.entry()
                trow += tentry2
                tentry2 += child.children
                i += 1
                if i < len(children):
                    n = number('list' + str(self.list_level), self.project, self.storage)

            node.replace_self(newnode)
        self.list_level -= 1


class ReferenceUpdater(nodes.SparseNodeVisitor):
    def __init__(self, document, refs):
        nodes.SparseNodeVisitor.__init__(self, document)
        self.refs = refs

    def visit_reference(self, node):
        if node.hasattr('refid'):
            refid = node['refid']
            if refid in self.refs:
                node.children[0] = nodes.Text(self.refs[refid])


class PdfPreprocessor(nodes.SparseNodeVisitor):
    def __init__(self, document, pdf):
        nodes.SparseNodeVisitor.__init__(self, document)
        self.pdf = pdf
        self.section_level = 0
        self.list_level = 0
        self.raw_prefix = pdf['raw-prefix'] if 'raw-prefix' in pdf else None

    def visit_section(self, node):
        self.section_level += 1
        if self.raw_prefix:
            key = 'heading' + str(self.section_level)
            prefix = self.raw_prefix[key] if key in self.raw_prefix else None
            if prefix == None:
                prefix = self.raw_prefix['heading'] if 'heading' in self.raw_prefix else None
            if prefix != None:
                i = node.parent.index(node)
                raw = nodes.raw(text=prefix)
                raw['format'] = 'pdf'
                node.parent.insert(i, raw)

    def depart_section(self, node):
        self.section_level -= 1


def common(text, dir, project):
    # Substitute fields by values
    if 'fields' in project:
        for field in project['fields']:
            text = re.sub(r'\#\#\#' + field + r'\#\#\#', tostring(project['fields'][field]), text, flags=re.I)
            text = re.sub(r'\#\{' + field + r'\}', tostring(project['fields'][field]), text, flags=re.I)
    # Make path to images absolute
    if 'images-root' in project:
        dir = os.path.abspath(project['images-root'])
    dir = dir.replace('\\', '/')
    text = re.sub(r'((figure|image)::\S*\s+)([.\w\d\/\\-]+\.(jpg|jpeg|pdf|png|svg))', r'\1' + dir + r'/\3', text, flags=re.I|re.M)

    # Add extra EOL
    text += '\n\n'
    return text

def doctree(doctree, project):
    if 'numbering' in project:
        e = Enumerator(doctree, project)
        doctree.walkabout(e)
        ru = ReferenceUpdater(doctree, e.refs)
        doctree.walk(ru)
    return doctree

def doctree_pdf(doctree, pdf):
    pp = PdfPreprocessor(doctree, pdf)
    doctree.walkabout(pp)
    return doctree

def html(text, dir, project):
    return common(text, dir, project)

def number(tag, project, storage):
    result = None
    if 'numbering' in project:
        numbering = project['numbering']
        if tag in numbering:
            template = numbering[tag]
            patterns = [r'\(((\w+\d*)(?:([\+\-\=])(\d+)?)?)\)',
                r'\[((\w+\d*)(?:([\+\-\=])(\d+)?)?)\]',]
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

def odt(text, dir, project):
    return common(text, dir, project)

def pdf(text, dir, project):
    return common(text, dir, project)

def tostring(src):
    if sys.version_info[0] < 3:
        text = unicode(src)
    else:
        text = str(src)
    return text