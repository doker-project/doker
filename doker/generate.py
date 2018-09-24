# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import yaml
from collections import namedtuple

import docutils
from docutils.parsers.rst import directives

from rst2pdf.createpdf import RstToPdf, add_extensions
from rst2pdf import pygments_code_block_directive

from doker import fileutils, preprocess

def html(files, project):
    return

def pdf(files, project, output):
    generated = []
    pdf = project['pdf'] if 'pdf' in project else None

    # Stylesheet processing
    stylesheets = []
    if pdf and ('stylesheet' in pdf):
        stylesheet_file = pdf['stylesheet']
        if not os.path.isfile(stylesheet_file):
            sys.stderr.write('Error: Unable to open stylesheet file: ' + stylesheet_file + '\n')
            sys.exit(1)
        with open(stylesheet_file, 'r') as f:
            try:
                style = yaml.load(f)
            except yaml.YAMLError as err:
                sys.stderr.write('Error: Parsing YAML style file failed: ' + err + '\n')
                sys.exit(1)

        stylesheet_json = 'tmp-stylesheet.json'
        print('Generatind temporary "' + stylesheet_json + '"')
        with open(stylesheet_json, 'w') as f:
            f.write(json.dumps(style))
        generated.append(stylesheet_json)
        stylesheets.append(stylesheet_json)

    # Revisions
    if 'revisions' in project:
        revisions_text  = '.. list-table:: Revision History\n'
        revisions_text += '   :class: revisions-table\n'
        revisions_text += '\n'
        revisions_text += '   * - Version\n'
        revisions_text += '     - Date\n'
        revisions_text += '     - Description\n'
        
        revisions = project['revisions']
        for revision in revisions:
            if isinstance(revision, dict):
                key = revision.keys()[0]
                ver = key
                date = '--'
                m = re.search(r'([\w\d.-:]+)\s+(?:\(|\[)([0-9\w\s./:]+)(?:\)|\])', key)
                if m:
                    ver = m.group(1)
                    date = m.group(2)
                revisions_text += '   * - **' + str(ver) + '**\n'
                revisions_text += '     - ' + date + '\n'
                revisions_text += '     - .. class:: revision-list\n'
                revisions_text += '\n'
                changes = revision[key]
                for change in changes:
                    revisions_text += '       + ' + change + '\n'
                    revisions_text += '\n'

        if not 'fields' in project:
            project['fields'] = {}
        project['fields']['revisions'] = revisions_text

    # Text processing
    text = ''

    # Cover page
    if pdf and ('cover' in pdf):
        cover_file = pdf['cover']
        if not os.path.isfile(cover_file):
            sys.stderr.write('Error: Unable to open cover file: ' + cover_file + '\n')
            sys.exit(1)
        with open(cover_file, 'r') as f:
            text += preprocess.pdf(f.read(), os.path.dirname(cover_file), project)

    # Main contents processing
    for file in files:
        with open(file['src'], 'r') as f:
            text += preprocess.pdf(f.read(), os.path.dirname(file['src']), project)

    # Output file name processing
    if pdf and 'output' in pdf:
        output = os.path.join(pdf['output'], output) if os.path.isdir(pdf['output']) else pdf['output']
        if not output.endswith('.pdf'):
            output += '.pdf'

    print(output)

    # Generating PDF
    options = namedtuple('Namespace', 'extensions')
    options.extensions = ['inkscape_r2p', 'vectorpdf_r2p']
    if pdf and ('toc' in pdf):
        if pdf['toc'] == 'dotted':
            options.extensions.append('dotted_toc')
    add_extensions(options)
    directives.register_directive('code-block', pygments_code_block_directive.code_block_directive)
    directives.register_directive('code', pygments_code_block_directive.code_block_directive)
    doctree = docutils.core.publish_doctree(text)
    doctree = preprocess.doctree(doctree, project)
    print('Generating "' + os.path.basename(output) + '"')
    try:
        RstToPdf(
            stylesheets=stylesheets, 
            background_fit_mode='scale',
            breakside=pdf['breakside'] if pdf and ('breakside' in pdf) else 'any',
            smarty=str(pdf['smartquotes'] if pdf and ('smartquotes' in pdf) else 2),
        ).createPdf(doctree=doctree, output=output)
    except Exception as err:
        sys.stderr.write('Error: PDF generating failed\n')
        fileutils.remove(generated)
        sys.exit(1)

    print('Post-processing "' + os.path.basename(output) + '"')
    try:
        import pkg_resources
        __version__ = pkg_resources.get_distribution('doker').version
    except Exception:
        __version__ = None
    creator = 'Doker'
    if __version__:
        creator += ' v' + __version__
    creator += ' \\(doker.org\\)'
    with open(output, 'rb') as f:
        text = f.read()
    with open(output, 'wb') as f:
        f.write(re.sub(r'/Creator \(\\\(unspecified\\\)\)', '/Creator (' + creator + ')' , text))

    # Temporary files removing
    fileutils.remove(generated)
