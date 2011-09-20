#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2008, 2009, 2011 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    ssh_client
    ==========

    Implements a simple ssh client using the paramiko library.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""


import sys
import os
import re

from paramiko import SSHClient


SERVER_PATTERN = re.compile('^(?:(\w*)@)?([A-Za-z0-9_.]*)(?::(\d*))?$')


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        sys.exit('%s server command\nInvalid number of arguments.' %
                 os.path.basename(sys.argv[0]))
    # extract the username, the server and the port from command line
    # argument
    username, server, port = SERVER_PATTERN.match(args[0]).groups()
    command = ' '.join(args[1:])
    # create the client
    client = SSHClient()
    # load the keys of known hosts for host key verification
    client.load_host_keys(os.path.expanduser(
        os.path.join('~', '.ssh', 'known_hosts')))
    # etablish the connection.  A passwort is not supplied, only key-based
    # authentication works
    client.connect(server, int(port or 22), username)
    # execute the command and print its output
    stdin, stdout, stderr = client.exec_command(command)
    stderr.flush()
    stdout.flush()
    sys.stderr.write(stderr.read())
    sys.stdout.write(stdout.read())


if __name__ == '__main__':
    main()
