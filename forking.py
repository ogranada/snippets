#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# userserver.py: A sample rpc server. Shows concepts of implementing a rpc
#                server, forking into background and giving up root
#                privileges
# Copyright (c) 2007 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


import os
import sys
import signal
import commands
from SimpleXMLRPCServer import SimpleXMLRPCServer

pid_file = '/home/lunar/test/userserver.pid'
msg_file = '/home/lunar/test/messages'

def go_and_die(sig, stack):
    for k in signal.__dict__:
        if signal.__dict__[k] == sig:
            signalname = k
    print 'exiting on', signalname
    if isinstance(msg_file, file):
        msg_file.close()
    sys.exit(0)

def list_users():
    users = commands.getoutput('users')
    return users.split(' ')

def write_message(msg):
    '''blubb'''
    global msg_file
    if isinstance(msg_file, basestring):
        msg_file = open(msg_file, 'w')
    msg_file.write(msg)
    msg_file.write('\n')
    msg_file.flush()
    return 'OK'

# fork into background
if os.fork() == 0:
    # become a session leader
    os.setsid()
    if os.fork() == 0:
        # fork a second time.
        # this avoids zombie processes because it is now orphaned and so
        # init becomes responsible for cleanups.
        # This second fork also prevents the daemon from ever acquiring a
        # controlling terminal
        os.chdir('/')
        os.umask(0)
    else:
        os._exit(0)
else:
    os._exit(0)

for i in range(0,3):
    # close stdin, stdout and stderr
    os.close(i)

# redirect to null device
os.open('/dev/null', os.O_RDONLY) #0
os.open('/home/lunar/test/stdout',
        os.O_WRONLY | os.O_CREAT,
        int('0644', 8)) #1
os.open('/home/lunar/test/stderr',
        os.O_WRONLY | os.O_CREAT,
        int('0644', 8)) #2

# register signal handlers
signal.signal(signal.SIGTERM, go_and_die)
signal.signal(signal.SIGINT, go_and_die)
signal.signal(signal.SIGQUIT, go_and_die)

# save pid
## f = open(pidfile, 'w')
## f.write(str(os.getpid()))
## f.close()
# todo: remove pid at server exit

# give up any privileges, if we have some
if os.getuid() == 0:
    import pwd
    nobody = pwd.getpwnam('nobody')
    os.setgid(nobody.pw_gid)
    os.setuid(nobody.pw_uid)
    # the numeric string form is just more readable (at least to me)
    os.chmod(pidfile, int('0644', 8))

server = SimpleXMLRPCServer(('127.0.0.1', 6666))
server.register_function(list_users)
server.register_function(write_message)
server.register_introspection_functions()
server.serve_forever()
