#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    screenshot
    ==========

    Demonstrates how to take screenshots based on the window name on X11.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import sys
import re
import subprocess


XWININFO_ID_PATTERN = re.compile(r'xwininfo: Window id: (0x\d+)')


def take_screenshot(window_name):
    """
    Takes a screenshot from the window with `window_name` and returns it as
    PNG bytestring.

    :param window_name: X11 window name
    :type window_name: str
    :returns: Screenshot as PNG or None, if no window was found
    :returntype: str
    """
    # call xwininfo to get the window id of the window with the given name
    proc = subprocess.Popen(['xwininfo', '-name', window_name],
                            stdout=subprocess.PIPE)
    stdout = proc.communicate()[0]
    if proc.returncode != 0:
        return None
    # extract the window id
    match = XWININFO_ID_PATTERN.search(stdout)
    if not match:
        raise ValueError('Could not extract window ID')
    # use import to take a screenshot
    proc = subprocess.Popen(['import', '-window', match.group(1), 'png:-'],
                            stdout=subprocess.PIPE)
    return proc.communicate()[0]


def main():
    progname = sys.argv[0]
    args = sys.argv[1:]
    windowtitle = filename = None
    if len(args) < 1 or len(args) > 2:
        sys.exit('usage: {0} window-title [filename]'.format(progname))
    elif len(args) == 2:
        windowtitle, filename = args
    else: # len(args) == 1
        windowtitle = args[0]
    shot = take_screenshot(windowtitle)
    if filename:
        with open(filename, 'wb') as stream:
            stream.write(shot)
    else:
        sys.stdout.write(shot)


if __name__ == '__main__':
    main()

