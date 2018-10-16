# -*- coding: utf-8 -*-

import os
import re
from collections import namedtuple

import docutils
from docutils.parsers.rst import directives

from rst2pdf.createpdf import RstToPdf, add_extensions
from rst2pdf import pygments_code_block_directive

from doker import fileutils, preprocess, log

def html(files, project):
    return

def pdf(files, project, output):
    generated = []
    pdf = project['pdf'] if 'pdf' in project else None

    # Stylesheet processing
    stylesheets = []
    try:
        if pdf and ('stylesheet' in pdf):
            stylesheet_json = fileutils.stylesheet_to_json(pdf['stylesheet'])
            generated.append(stylesheet_json)
            stylesheets.append(stylesheet_json)
        if pdf and ('stylesheets' in pdf):
            for stylesheet_file in pdf['stylesheets']:
                stylesheet_json = fileutils.stylesheet_to_json(stylesheet_file)
                generated.append(stylesheet_json)
                stylesheets.append(stylesheet_json)
    except Exception:
        fileutils.remove(generated)
        raise

    # Revisions
    if 'revisions' in project:
        revisions_text  = '.. _unnumbered_revisions:\n'
        revisions_text += '.. list-table:: Revision History\n'
        revisions_text += '   :class: revisions-table\n'
        revisions_text += '   :header-rows: 1\n'
        revisions_text += '\n'
        revisions_text += '   * - Version\n'
        revisions_text += '     - Date\n'
        revisions_text += '     - Description\n'
        
        last_version = None
        last_date = None
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
                if not last_version:
                    last_version = ver
                if not last_date:
                    last_date = date
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
        if (not 'version' in project['fields']) and last_version:
            project['fields']['version'] = last_version
        if (not 'date' in project['fields']) and last_date:
            project['fields']['date'] = last_date

    # Text processing
    text = ''

    # Cover page
    if pdf and ('cover' in pdf):
        cover_file = pdf['cover']
        if not os.path.isfile(cover_file):
            log.error("Unable to open cover file: '%s'", cover_file)
            fileutils.remove(generated)
            raise IOError('Cover file error')
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
    if pdf:
        doctree = preprocess.doctree_pdf(doctree, pdf)
    log.info("Generating '%s'", os.path.basename(output))
    try:
        RstToPdf(
            background_fit_mode='scale',
            breaklevel=pdf['break-level'] if pdf and ('break-level' in pdf) else 1,
            breakside=pdf['break-side'] if pdf and ('break-side' in pdf) else 'any',
            repeat_table_rows=pdf['repeate-table-rows'] if pdf and ('repeate-table-rows' in pdf) else True,
            smarty=str(pdf['smartquotes'] if pdf and ('smartquotes' in pdf) else 1),
            stylesheets=stylesheets, 
        ).createPdf(doctree=doctree, output=output)
    except Exception as err:
        log.error('PDF generating failed')
        fileutils.remove(generated)
        raise

    log.info("Post-processing '%s'", os.path.basename(output))
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
