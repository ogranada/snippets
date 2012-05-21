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
from itertools import groupby
from collections import namedtuple

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.domains import Domain, ObjType, Index
from sphinx.directives import ObjectDescription
from sphinx.util.compat import Directive
from sphinx.util.nodes import make_refnode


SnippetEntry = namedtuple('SnippetEntry', 'docname synopsis')

DirectoryEntry = namedtuple('DirectoryEntry', 'docname')


def normalized_snippet_name(name, directory=None):
    """
    Return the normalized snippet ``name``, prepending ``directory``, if given.
    """
    if directory:
        snippet = posixpath.join(directory, name)
    else:
        snippet = name
    snippet = snippet.lstrip('/')
    return posixpath.normpath(snippet)


def normalized_directory_name(directory):
    """
    Return the normalized ``directory`` name.

    Normalized directory names always end with a slash.
    """
    return posixpath.normpath(directory) + posixpath.sep


def is_directory_name(name):
    """
    Check, if ``name`` is a directory name, meaning that it ends with a slash.

    Return ``True``, if ``name`` is a directory name, ``False`` otherwise.
    """
    return name.endswith(posixpath.sep)


class SnippetDirectory(Directive):
    """
    A directive for snippet directories.
    """

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
            # create an index entry
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
        'synopsis': directives.unchanged,
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
        snippets[snippet] = SnippetEntry(
            self.env.docname, self.options.get('synopsis', ''))

        directory, basename = posixpath.split(snippet)
        if directory:
            indextext = '{0} (snippet in {1})'.format(basename, directory)
        else:
            indextext = '{0} (snippet)'.format(basename)
        self.indexnode['entries'].append(('single', indextext, snippet, ''))


class SnippetXRefRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):

        if not has_explicit_title:
            target = target.lstrip('~')
            if title.startswith('~'):
                _, title = posixpath.split(title)

        if not target.startswith('/'):
            refnode['snip:directory'] = env.temp_data.get('snip:directory')

        return title.lstrip('/'), target


class DirectoryXRefRole(XRefRole):

    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            target = target.lstrip('~')
            if title.startswith('~'):
                # remove all directory parts execpt the last one.  Need to
                # normalize first to remove any trailing slash
                _, title = posixpath.split(
                    posixpath.normpath(title.lstrip('~')))
            title = normalized_directory_name(title)
        return title, target


class IndexEntry(namedtuple(
    'IndexEntry', 'name docname anchor extra description subentries')):

    def to_index_tuple(self, toplevel=False):
        if self.subentries:
            index_type = 1
        else:
            index_type = 0 if toplevel else 2
        return (self.name, index_type, self.docname,
                self.anchor, self.extra, '', self.description)


def group_by_first_letter(item):
    return item.lower()[0]


class SnippetIndex(Index):

    name = 'index'
    localname = 'Snippets index'
    shortname = 'snippets'

    def make_directory_entry(self, directory, name=None):
        name = normalized_directory_name(name or directory)
        try:
            docname, anchor = self.domain.get_directory_location(directory)
        except KeyError:
            docname = anchor = ''
        return IndexEntry(name, docname, anchor, 'directory', '', {})

    def make_snippet_entry(self, snippet, name=None):
        name = name or snippet
        docname, anchor = self.domain.get_snippet_location(snippet)
        synopsis = self.domain.get_snippet_synopsis(snippet)
        return IndexEntry(name, docname, anchor, '', synopsis, None)

    def make_entry(self, target, name=None):
        if is_directory_name(target):
            return self.make_directory_entry(target, name)
        else:
            return self.make_snippet_entry(target, name)

    def add_entry(self, index_tree, target):
        parts = target.split(posixpath.sep, 1)
        if len(parts) > 1 and parts[1]:
            directory, name = parts
            directory = normalized_directory_name(directory)
            entry = index_tree.setdefault(
                directory, self.make_directory_entry(directory))
            target_tree = entry.subentries
        else:
            name = target
            target_tree = index_tree

        entry = self.make_entry(target, name)
        target_tree.setdefault(target, entry)

    def generate_index_tree(self):
        index_tree = {}
        # add all snippets
        for snippet in self.domain.data['snippets']:
            self.add_entry(index_tree, snippet)
        # add directories
        for directory in self.domain.data['directories']:
            self.add_entry(index_tree, directory)
        return index_tree

    def generate(self, docnames=None):
        index_tree = self.generate_index_tree()
        index_names = sorted(index_tree, key=lambda x: x.lower())
        content = []
        for letter, names in groupby(index_names, group_by_first_letter):
            letter_entries = []
            for name in names:
                entry = index_tree[name]
                letter_entries.append(entry.to_index_tuple(toplevel=True))
                if entry.subentries:
                    sub_names = sorted(entry.subentries,
                                       key=lambda x: x.lower())
                    for sub_name in sub_names:
                        letter_entries.append(
                            entry.subentries[sub_name].to_index_tuple())
            content.append((letter, letter_entries))
        return content, False


class SnippetDomain(Domain):

    name = 'snip'
    label = 'Snippet'

    data_version = 2

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

    indices = [SnippetIndex]

    def get_snippet_location(self, snippet):
        snippet = normalized_snippet_name(snippet)
        docname = self.data['snippets'][snippet].docname
        return (docname, snippet)

    def get_snippet_synopsis(self, snippet):
        return self.data['snippets'][snippet].synopsis

    def get_directory_location(self, directory):
        directory = normalized_directory_name(directory)
        docname = self.data['directories'][directory].docname
        return (docname, directory)

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
