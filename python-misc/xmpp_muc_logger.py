#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2007 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""A muc logger"""

import os
import sys
import signal
import logging
import threading
import atexit
atexit.register(logging.shutdown)

from datetime import datetime
import xmpp


CONF = (
    ## duplicate this dictionary
    {
        ## the jid of the bot
        'jid': 'foo@example.com',
        ## the password to authenticate the bit
        'passwd': 'XXX',
        ## the muc to join
        'muc_jid': 'foo@conference.jabber.org',
        ## the password to authenticate on the muc
        'muc_passwd': '',
        ## proxy configuration
        'proxy': {
            ## uncomment for proxy configuration
            # 'host': '192.168.0.1',
            # 'port': 3128,
            # 'username': 'luchs',
            # 'password': 'secret'
            },
        ## format, which is used to log simple messages
        ## jid       - The senders JID
        ## nick      - The senders nick
        ## timestamp - Date and time formatted according to datefmt
        ##             (see below)
        ## text      - Message text (only for message_format)
        'message_format': '"%(text)s" from %(nick)s at %(timestamp)s',
        ## format, which is used to log join events
        'join_format': '%(nick)s joined at %(timestamp)s',
        ## format, which is used to log leave events
        'leave_format': '%(nick)s left at %(timestamp)s',
        ## format, which is used to log timestamps
        ## see http://docs.python.org/lib/module-time.html for a
        ## list of valid placeholders
        'datefmt': '%Y-%m-%d %H:%M:%S',
        ## the logging level
        ## set to logging.INFO to hide join and leave events
        'level': logging.DEBUG,
        ## uncomment to log to a file instead of stderr
        #'filename': 'myfilename',
        ## set to 'a' to append to exisiting files
        #'filemode': 'w',
        },
    #{
        ## Define other mucs here
        #}
    )


class Configuration(object):
    """A little class storing the logger configuration"""
    def __init__(self, **kwargs):
        self._jid = None
        self.passwd = None
        self.muc_jid = None
        self.muc_passwd = None
        self.proxy = {}
        self.logging_format = ('%(levelname)s : %(name)s : %(asctime)s - '
                               '%(message)s')
        self.message_format = u'"%(text)s" from %(nick)s at %(timestamp)s'
        self.join_format = u'%(nick)s joined at %(timestamp)s'
        self.leave_format = u'%(nick)s left at %(timestamp)s'
        self.datefmt =  '%Y-%m-%d %H:%M:%S'
        self.level = logging.DEBUG
        # if none, logging is directed to console
        self._filename = None
        self.filemode = 'w'
        # set values
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def _set_jid(self, jid):
        if isinstance(jid, basestring):
            jid = xmpp.JID(jid)
        self._jid = jid

    def _get_jid(self):
        return self._jid

    jid = property(_get_jid, _set_jid)

    def _set_filename(self, filename):
        directory = os.path.dirname(os.path.abspath(filename))
        if not os.path.isdir(directory):
            os.makedirs(directory)
        self._filename = filename

    def _get_filename(self):
        return self._filename

    def _del_filename(self):
        self.filename = None

    filename = property(_get_filename, _set_filename, _del_filename)


class Logger(threading.Thread):
    """Logs a muc

    :ivar roster: All nicks in the muc"""
    def __init__(self, conf):
        self.roster = []
        self.conf = conf
        self.logger = logging.getLogger(self.conf.muc_jid)
        if self.conf.filename:
            handler = logging.FileHandler(self.conf.filename,
                                          self.conf.filemode)
        else:
            handler = logging.StreamHandler()
        formatter = logging.Formatter(self.conf.logging_format,
                                      self.conf.datefmt)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(conf.level)

        debug = []
	## debug=['nodebuilder', 'dispatcher', 'gen_auth', 'SASL_auth',
        ##        'bind', 'socket', 'CONNECTproxy', 'TLS', 'roster',
        ##        'browser', 'ibb']
        self.client = xmpp.Client(self.conf.jid.getDomain(), debug=debug)
        super(Logger, self).__init__()

    def cb_event(self, sess, evt):
        """Handles chatting events"""
        timestamp = evt.getTimestamp()
        if not timestamp:
            evt.setTimestamp()
            timestamp = evt.getTimestamp()
        timestamp = datetime.strptime(timestamp, '%Y%m%dT%H:%M:%S')
        params = {'jid': evt.getFrom().getStripped(),
                  'nick': evt.getFrom().getResource(),
                  'timestamp': timestamp.strftime(self.conf.datefmt),
                  }

        if isinstance(evt, xmpp.Message):
            params['text'] = evt.getBody()
            self.logger.info(self.conf.message_format, params)
        elif isinstance(evt, xmpp.Presence):
            nick = params['nick']
            if evt.getType() == 'unavailable' and nick in self.roster:
                self.roster.remove(nick)
                self.logger.debug(self.conf.leave_format, params)
            elif nick not in self.roster:
                self.roster.append(nick)
                self.logger.debug(self.conf.join_format, params)


    def connect(self):
        """Etablishes a connection to the server an joins the muc.
        Returns True, if connection was etablished successfully,
        False otherwise"""
        # connect
        conres = self.client.connect(proxy=self.conf.proxy)
        self.logger.info('connecting to %s', self.conf.jid.getDomain())
        if not conres:
            self.logger.error('Unable to connect to server %s!',
                              self.conf.jid.getDomain())
            return False
        if conres != 'tls':
            self.logger.warning('unable to estabilish secure connection - '
                                'TLS failed!')

        # authenticate
        self.logger.info('authenticating as %s', self.conf.jid.getNode())
        authres = self.client.auth(self.conf.jid.getNode(),
                                   self.conf.passwd)
        if not authres:
            self.logger.error('Unable to authorize as %s - check '
                              'login/password.', self.conf.jid.getNode())
            return False
        if authres != 'sasl':
            self.logger.warning('unable to perform SASL auth on %s. Old '
                                'authentication method used!',
                                self.conf.jid.getDomain())

        ## self.client.RegisterHandler('message', self.cb_message)
        ## self.client.RegisterHandler('presence', self.cb_presence)
        self.client.RegisterDefaultHandler(self.cb_event)

        self.logger.info('joining muc %s', self.conf.muc_jid)
        # indicate presence
        pres = xmpp.Presence(to='%s/logger' % self.conf.muc_jid)
        pres.setTag('x', namespace=xmpp.NS_MUC).setTagData('password',
                                                           self.conf.muc_passwd)
        pres.getTag('x').addChild('history',
                                  {'maxchars':'0', 'maxstanzas':'0'})
        self.client.send(pres)
        return True

    def run(self):
        """Watches the muc"""
        if not self.connect():
            # exit thread, if connecting failed
            return
        while True:
            self.client.Process(1)


def main():
    for conf in CONF:
        cfg = Configuration(**conf)
        logger = Logger(cfg)
        logger.setDaemon(True)
        logger.start()

    signal.signal(signal.SIGINT, lambda *args: sys.exit('Interrupted'))
    while True:
        signal.pause()


if __name__ == '__main__':
    main()
