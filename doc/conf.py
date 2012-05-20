# -*- coding: utf-8 -*-
# Copyright (c) 2011, 2012 Sebastian Wiesner <lunaryorn@googlemail.com>

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

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_sphinx = '1.1'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx',
              'sphinx.ext.extlinks', 'snippets']

source_suffix = '.rst'
master_doc = 'index'

project = u'Snippets'
copyright = u'2011, Sebastian Wiesner'

def get_git_hash_of_head():
    command = ['git', 'describe', '--always', '--abbrev=0', 'HEAD']
    output = subprocess.check_output(command, cwd=os.path.dirname(__file__))
    return output.strip()

hash_of_head = get_git_hash_of_head()
version = hash_of_head[:7]
release = hash_of_head

exclude_patterns = ['_build/*', 'references.rst']

rst_prolog = """\
.. |changeset| replace:: :github:`{version} <commit/{release}>`
""".format(**globals())

primary_domain = 'snip'

pygments_style = 'sphinx'
html_theme = 'agogo'
html_title = 'Snippets'

intersphinx_mapping = {'python': ('http://docs.python.org/', None),
                       'pyudev': ('http://pyudev.readthedocs.org/en/latest/', None),
                       'pyside': ('http://www.pyside.org/docs/pyside/', None)}

extlinks = {
    'github': ('https://github.com/lunaryorn/snippets/%s', ''),
}

snippet_source_url = 'https://github.com/lunaryorn/snippets/blob/master/{snippet}'


def configure_github_pages(app, exc):
    if app.builder.name == 'html':
        # inhibit github pages site processor
        open(os.path.join(app.outdir, '.nojekyll'), 'w').close()
        with open(os.path.join(app.outdir, 'CNAME'), 'w') as stream:
            stream.write('snippets.lunaryorn.de\n')


def setup(app):
    app.connect('build-finished', configure_github_pages)

