# -*- coding: utf-8 -*-
# Copyright (c) 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
    snippets
    ========

    A snippets domain for Sphinx.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from __future__ import (print_function, division, unicode_literals,
                        absolute_import)

import posixpath
from collections import namedtuple

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.domains import Domain, ObjType
from sphinx.directives import ObjectDescription
from sphinx.util.compat import Directive
from sphinx.util.nodes import make_refnode



SnippetEntry = namedtuple('SnippetEntry', 'docname')

DirectoryEntry = namedtuple('DirectoryEntry', 'docname')


def normalized_snippet_name(name, directory=None):
    if directory:
        snippet = posixpath.join(directory, name)
    else:
        snippet = name
    return posixpath.normpath(snippet)


def normalized_directory_name(directory):
    return posixpath.normpath(directory) + '/'


class SnippetDirectory(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'noindex': directives.flag,
    }

    def run(self):
        env = self.state.document.settings.env
        directory = normalized_directory_name(self.arguments[0].strip())
        env.temp_data['snip:directory'] = directory

        if 'noindex' not in self.options:
            directories = env.domaindata['snip']['directories']
            directories[directory] = DirectoryEntry(env.docname)
            target = nodes.target('', '', ids=[directory])
            self.state.document.note_explicit_target(target)
            indextext = '{0} (snippet directory)'.format(directory)
            index = addnodes.index(
                entries=[('single', indextext, directory, '')])
            return [target, index]
        else:
            return []


class Snippet(ObjectDescription):

    option_spec = {
        'noindex': directives.flag,
        'directory': directives.unchanged,
    }

    def handle_signature(self, sig, signode):
        directory = self.options.get(
            'directory', self.env.temp_data.get('snip:directory'))

        snippet = normalized_snippet_name(sig, directory)
        source_url = self.env.config.snippet_source_url.format(
                snippet=snippet)

        sigprefix = 'Snippet '
        signode.append(addnodes.desc_annotation(sigprefix, sigprefix))

        ref = nodes.reference(snippet, internal=False, refuri=source_url)
        signode.append(ref)

        directory, name = posixpath.split(snippet)
        if directory:
            sigdirectory = directory + '/'
            ref.append(addnodes.desc_addname(sigdirectory, sigdirectory))
        ref.append(addnodes.desc_name(name, name))

        return snippet

    def add_target_and_index(self, snippet, sig, signode):
        snippets = self.env.domaindata['snip']['snippets']
        if snippet in snippets:
            self.state_machine.reporter.warning(
                'duplicate snippet {0}, other instance in {1}'.format(
                    snippet, self.env2.doc2path(snippets[snippet].docname)),
                line=self.lineno)
        signode['first'] = not self.names
        signode['ids'].append(snippet)
        snippets[snippet] = SnippetEntry(self.env.docname)

        directory, basename = posixpath.split(snippet)
        if directory:
            indextext = '{0} (snippet in {1})'.format(basename, directory)
        else:
            indextext = '{0} (snippet)'.format(basename)
        self.indexnode['entries'].append(('single', indextext, snippet, ''))


class SnippetXRefRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['snip:directory'] = env.temp_data.get('snip:directory')

        if not has_explicit_title:
            target = target.lstrip('~')
            if title.startswith('~'):
                _, title = posixpath.split(title)

        return title, target


class DirectoryXRefRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            title = normalized_directory_name(title)
        return title, target


class SnippetDomain(Domain):

    name = 'snip'
    label = 'Snippet'

    object_types = {
        'snippet': ObjType('Snippet', 'snippet'),
        'directory': ObjType('Directory', 'dir'),
    }

    directives = {
        'directory': SnippetDirectory,
        'snippet': Snippet,
    }

    roles = {
        'dir': DirectoryXRefRole(),
        'snippet': SnippetXRefRole(),
    }

    initial_data = {
        'snippets': {},
        'directories': {},
    }

    def clear_doc(self, docname):
        for snippet, entry in self.data['snippets'].items():
            if entry.docname == docname:
                del self.data['snippets'][snippet]

    def resolve_xref(self, env, fromdocname, builder, type, target, node,
                     contnode):
        if type == 'dir':
            entry = self.data['directories'].get(
                normalized_directory_name(target))
        else:
            directory = node.get('snip:directory')
            target = normalized_snippet_name(target, directory)
            entry = self.data['snippets'].get(target)
        if not entry:
            return
        return make_refnode(builder, fromdocname, entry.docname, target,
                            contnode, target)

    def get_objects(self):
        for directory, entry in self.data['directories'].iteritems():
            yield directory, directory, 'snippet', entry.docname, directory, -1
        for snippet, entry in self.data['snippets'].iteritems():
            yield snippet, snippet, 'snippet', entry.docname, snippet, 1


def setup(app):
    app.add_config_value('snippet_source_url', None, 'env')
    app.add_domain(SnippetDomain)
