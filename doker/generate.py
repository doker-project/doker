# -*- coding: utf-8 -*-

import os
import re
import yaml

from collections import namedtuple

import docutils
from docutils.parsers.rst import directives
from docutils.writers.odf_odt import Writer

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from .rst2pdf.createpdf import RstToPdf, add_extensions
from .rst2pdf import pygments_code_block_directive

from . import fileutils, preprocess, log

def rst2html(file_path, project):
    settings = {
        'stylesheet': '',
        'stylesheet_path': [],
        'xml_declaration': '',
        'doctype_declaration': 0
    }
    with open(file_path, 'r') as f:
        doctree = docutils.core.publish_doctree(preprocess.html(f.read(), os.path.dirname(file_path), project))
    doctree = preprocess.doctree(doctree, project)
    html = docutils.core.publish_from_doctree(doctree, writer_name='html', settings_overrides=settings)

    # Remove common HTML preface
    html = re.sub(r'^[\s\S]*\<body\>', '', html, re.I | re.M)
    # Remove common HTML ending
    html = re.sub(r'<\/body\>[\s\S]*\<\/html\>$', '', html, re.I | re.M)
    # Parse external links
    html = re.sub(r'(<a)(.*href="http[^>]+)>', r'\1 class="ext"\2 target="_blank">', html, re.I)

    return html

def html(files, project, output):
    html = project['html'] if 'html' in project else None

    # Output path processing
    if html and 'output' in html:
        output = os.path.join(os.getcwd(), html['output'])
        if not os.path.exists(output):
            os.makedirs(output)

    # Templates root directory
    templates_root = os.getcwd()
    if html and 'templates-root' in html:
        templates_root = os.path.join(templates_root, html['templates-root'])
    templates = Environment(loader=FileSystemLoader(templates_root))

    # Main processing
    for file in files:
        with open(file['src'], 'r') as f:
            try:
                page = yaml.full_load(f)
            except yaml.YAMLError as err:
                log.error("Parsing YAML page file failed: '%s'", err)
                raise
        if not 'template' in page:
            log.warning("No template in page '%s'", file['src'])
            continue

        # Blocks processing
        if 'blocks' in page:
            blocks = page['blocks']
            for k in blocks.keys():
                v = blocks[k]
                block_path = os.path.join(os.path.dirname(file['src']), v)
                if block_path.endswith('.rst'):
                    block = rst2html(block_path, project)
                    blocks[k] = block

        try:
            template = templates.get_template(page['template'])
        except TemplateNotFound as err:
            log.error("Template not found: '%s'", err)
            raise

        html_dir = os.path.join(output, file['path'])
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        html_path = os.path.join(html_dir, 'index.html')
        log.info("Generating '%s'", os.path.abspath(html_path))
        with open(html_path, 'w') as f:
            f.write(template.render(page))

    return

def odt(files, project, output):
    odt = project['odt'] if 'odt' in project else None

    # Text processing
    text = ''

    # Main contents processing
    for file in files:
        with open(file['src'], 'r') as f:
            text += preprocess.odt(f.read().decode('utf8'), os.path.dirname(file['src']), project)

    # Generating ODT
    doctree = docutils.core.publish_doctree(text)
    doctree = preprocess.doctree(doctree, project)
    log.info("Generating '%s'", os.path.basename(output))

    settings = {}
    if odt and 'stylesheet' in odt:
        settings['stylesheet'] = odt['stylesheet']

    odt_writer = Writer()
    odt_contents = docutils.core.publish_from_doctree(doctree, writer=odt_writer, settings_overrides=settings)
    with open(output, 'w') as f:
        f.write(odt_contents)

def pdf(files, project, output):
    pdf = project['pdf'] if 'pdf' in project else None

    # Stylesheet processing
    stylesheets = []
    try:
        if pdf and ('stylesheet' in pdf):
            tmp_json = fileutils.stylesheet_to_tmp_json(pdf['stylesheet'])
            stylesheets.append(tmp_json)
        if pdf and ('stylesheets' in pdf):
            for stylesheet_file in pdf['stylesheets']:
                tmp_json = fileutils.stylesheet_to_tmp_json(stylesheet_file)
                stylesheets.append(tmp_json)
    except Exception:
        raise

    # Revisions
    if 'revisions' in project:
        revisions_text  = '.. _unnumbered_revisions:\n'
        revisions_text += '.. list-table:: Revision History\n'
        revisions_text += '   :class: revisions-table\n'
        revisions_text += '   :header-rows: 1\n'
        revisions_text += '\n'
        revisions_text += '   * - Revision\n'
        revisions_text += '     - Date\n'
        revisions_text += '     - Description\n'

        last_revision = None
        last_date = None
        revisions = project['revisions']
        for revision in revisions:
            if isinstance(revision, dict):
                key = list(revision.keys())[0]
                rev = key
                date = '--'
                m = re.search(r'([\w\d.-:]+)\s+(?:\(|\[)([0-9\w\s./:]+)(?:\)|\])', key)
                if m:
                    rev = m.group(1)
                    date = m.group(2)
                if not last_revision:
                    last_revision = rev
                if not last_date:
                    last_date = date
                revisions_text += '   * - **' + str(rev) + '**\n'
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
        if (not 'revision' in project['fields']) and last_revision:
            project['fields']['revision'] = last_revision
        if (not 'version' in project['fields']) and last_revision:
            project['fields']['version'] = last_revision
        if (not 'date' in project['fields']) and last_date:
            project['fields']['date'] = last_date

    # Text processing
    text = ''

    # Cover page
    if pdf and ('cover' in pdf):
        cover_file = pdf['cover']
        if not os.path.isfile(cover_file):
            log.error("Unable to open cover file: '%s'", cover_file)
            raise IOError('Cover file error')
        text += preprocess.pdf(fileutils.readfile(cover_file), os.path.dirname(cover_file), project)

    # Main contents processing
    for file in files:
        text += preprocess.pdf(fileutils.readfile(file['src']), os.path.dirname(file['src']), project)

    # Output file name processing
    if pdf and 'output' in pdf:
        output = os.path.join(pdf['output'], output) if os.path.isdir(pdf['output']) else pdf['output']
        if not output.endswith('.pdf'):
            output += '.pdf'

    # Generating PDF
    options = namedtuple('Namespace', 'extensions')
    options.extensions = ['inkscape', 'vectorpdf']
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
        stylesheet_names = []
        for stylesheet in stylesheets:
            stylesheet_names.append(stylesheet.name)
        RstToPdf(
            background_fit_mode='scale',
            breaklevel=pdf['break-level'] if pdf and ('break-level' in pdf) else 1,
            breakside=pdf['break-side'] if pdf and ('break-side' in pdf) else 'any',
            repeat_table_rows=pdf['repeate-table-rows'] if pdf and ('repeate-table-rows' in pdf) else True,
            smarty=str(pdf['smartquotes'] if pdf and ('smartquotes' in pdf) else 1),
            stylesheets=stylesheet_names,
        ).createPdf(doctree=doctree, output=output)
    except Exception as err:
        log.error("PDF generating failed: %s", err)
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
