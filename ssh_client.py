#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2008 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

import sys
import os
import re

from paramiko import SSHClient


server_re = re.compile('^(?:(\w*)@)?([A-Za-z0-9_.]*)(?::(\d*))?$')


def main():
    args = sys.argv[1:]
    if len(sys.argv) < 3:
        sys.exit('%s server command\nInvalid number of arguments.' %
                 os.path.basename(sys.argv[0]))
    username, server, port = server_re.match(sys.argv[1]).groups()
    command = ' '.join(sys.argv[2:])
    client = SSHClient()
    client.load_host_keys(os.path.expanduser(
        os.path.join('~', '.ssh', 'known_hosts')))
    client.connect(server, int(port or 22), username)
    stdin, stdout, stderr = client.exec_command(command)
    stderr.flush()
    stdout.flush()
    sys.stderr.write(stderr.read())
    sys.stdout.write(stdout.read())


if __name__ == '__main__':
    main()
