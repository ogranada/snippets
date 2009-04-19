# -*- encoding: utf-8 -*-
# Copyright (c) 2007 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

from __future__ import with_statement


import os.path
import shutil
import readline


ERROR_PREFIX = '### ERROR ###'


class FilenameCompleter(object):
    """Filename completer for readline.
    Supports with statement::

        with FilenameCompleter():
            print raw_input('Enter a filename: ')
    """
    def __init__(self):
        self.matches = []

    def __enter__(self):
        self.cmpl_function = readline.get_completer()
        self.delims = readline.get_completer_delims()
        readline.set_completer_delims('')
        readline.set_completer(self)
        readline.parse_and_bind('tab: complete')

    def __exit__(self, exc_type, exc_value, traceback):
        # restore old values
        readline.set_completer(self.cmpl_function)
        readline.set_completer_delims(self.delims)
        readline.parse_and_bind('tab: ')

    def calculate_matches(self, text):
        """Calculates all matches for `text`"""
        dirname = os.path.dirname(text)
        filename =  os.path.basename(text)
        completed = [os.path.join(dirname, f)
                     for f in os.listdir(os.path.expanduser(dirname) or '.')
                     if f.startswith(filename)]
        return completed

    def complete(self, text, state):
        """Invoked successivly with increasing state number until it returns
        None. If state is 0, all completions are recalculated"""
        if state == 0:
            self.matches = self.calculate_matches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

    # make instance callable
    __call__ = complete


class readline_insert(object):
    """A class which provides a facility to insert text to the command
    line. Intend for you with the ``with`` statement::

        with readline_insert('foo'):
            print raw_input('Your Name is: ')
    """
    def __init__(self, value):
        self.value = value

    def __enter__(self):
        self.old_hook = readline.set_pre_input_hook(self.input_hook)

    def __exit__(self, exc_type, exc_value, traceback):
        readline.set_pre_input_hook(self.old_hook)

    def input_hook(self):
        readline.insert_text(self.value)
        readline.redisplay()


def backup_file(filename):
    # saving backup
    backupfile = filename + "~"
    print 'Saving backup', backupfile, '...'
    if os.path.exists(backupfile):
        print 'Overwriting old backup...'
    shutil.copy(filename, backupfile)


def edit_lines(lines):
    """Edit a list of lines *inplace*. Returns a tupel containing
    the edited lines and the number of lines edited"""
    edit_counter = 0
    for ln, line in enumerate(lines):
        with readline_insert(line):
            new = raw_input('%03d > ' % (ln + 1))
            if new != line:
                edit_counter += 1
                lines[ln] = new
    return lines, edit_counter


def edit_text_file():
    """for a filename, shows the content and allows to edit the content
    line by line"""
    with FilenameCompleter():
        filename = raw_input('Please enter a file name to edit: ')

    filename = os.path.expanduser(filename)
    if not filename:
        print ERROR_PREFIX, 'No filename given'
        return

    try:
        backup_file(filename)
        with open(filename, 'r') as instream:
            content = instream.read().splitlines()
    except EnvironmentError, e:
        print ERROR_PREFIX, e
        return

    content, edit_count = edit_lines(content)

    if edit_count:
        print "You have made %d changes." % edit_count
        choice = raw_input("Do you want to save this changes (y,Y): ")
        if choice.lower() == 'y':
            try:
                with open(filename, 'w') as outstream:
                    outstream.write('\n'.join(content))
            except EnvironmentError, e:
                print ERROR_PREFIX, e
            else:
                print 'Saved'


if __name__ == '__main__':
    try:
        edit_text_file()
    except KeyboardInterrupt:
        pass
