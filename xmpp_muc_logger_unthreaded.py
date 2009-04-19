#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2007 Sebastian Wiesner <basti.wiesner@gmx.net>

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
import logging
import atexit
atexit.register(logging.shutdown)

from datetime import datetime
import xmpp


## BOT = (botjid, password)
BOT = ('foo@example.com', 'XXX')
## MUC = (mucjid, password)
MUC = ('foo@conference.example.com','')
PROXY = {
    ## uncomment for proxy configuration
    # 'host': '192.168.0.1',
    # 'port': 3128,
    # 'username': 'luchs',
    # 'password': 'secret'
    }
# format for messages
# available are:
# jid       - The senders JID
# nick      - The senders nick
# timestamp - Date and time formatted according to datefmt (see below)
# text      - Message text (only for MESSAGE_FORMAT)
MESSAGE_FORMAT = u'"%(text)s" from %(nick)s at %(timestamp)s'
JOIN_FORMAT = u'%(nick)s joined at %(timestamp)s'
LEAVE_FORMAT = u'%(nick)s left at %(timestamp)s'
LOGGING_CONF = {
    ## don't touch these lines unless you know what you're doing
    'level': logging.INFO,
    'format': '%(levelname)s: %(asctime)s - %(message)s',
    ## uncomment for logging into a file
    #'filemode': 'w',
    #'filename': 'path/to/my/logfile',
    ## date format of log messages
    'datefmt':  '%Y-%m-%d %H:%M:%S',
    }


class Message(object):
    """Stores a single message received from muc"""

    def __init__(self, msg, evt='message'):
        """Creates a new message instance from jabber message `msg`.

        `evt` defines the kind of messages, valid values are

        - leave
        - join
        - message

        :ivar jid: The jid, which send the message
        :ivar nick: The nick that send the message
        :ivar timestamp: The timestamp
        :ivar text: The text of the message
        :ivar event: The kind of message"""

        self.jid = msg.getFrom().getStripped()
        self.nick = msg.getFrom().getResource()
        self.event = evt
        timestamp = msg.getTimestamp()
        if not timestamp:
            msg.setTimestamp()
            timestamp = msg.getTimestamp()
        timestamp = datetime.strptime(timestamp, '%Y%m%dT%H:%M:%S')
        self.timestamp = timestamp.strftime(LOGGING_CONF['datefmt'])
        self.text = (msg.getBody() if isinstance(msg, xmpp.Message)
                     else None)

    def __unicode__(self):
        fmt = globals()['%s_FORMAT' % self.event.upper()]
        return fmt % vars(self)

    def __str__(self):
        fmt = globals()['%s_FORMAT' % self.event.upper()]
        return fmt % vars(self)


class Logger(object):
    """Logs a muc

    :ivar roster: All nicks in the muc"""
    def __init__(self):
        self.roster = []
        self.jid, self.passwd = BOT
        self.muc, self.muc_passwd = MUC
        self.jid = xmpp.JID(self.jid)
        debug = []
        ## debug=['nodebuilder', 'dispatcher', 'gen_auth', 'SASL_auth',
        ##        'bind', 'socket', 'CONNECTproxy', 'TLS', 'roster',
        ##        'browser', 'ibb']
        self.client = xmpp.Client(self.jid.getDomain(), debug=debug)

    def cb_message(self, sess, msg):
        """Callback for normal messages"""
        logging.info(unicode(Message(msg, 'message')))

    def cb_presence(self, sess, pres):
        """Callback for presence changes"""
        msg = Message(pres)
        if pres.getType() == 'unavailable' and msg.nick in self.roster:
            msg.event = 'leave'
            self.roster.remove(msg.nick)
            logging.info(unicode(msg))
        elif msg.nick not in self.roster:
            msg.event = 'join'
            self.roster.append(msg.nick)
            logging.info(unicode(msg))

    def connect(self):
        """Etablishes a connection to the server"""
        # connect
        conres = self.client.connect(proxy=PROXY)
        logging.info('connecting to %s', self.jid.getDomain())
        if not conres:
            sys.exit('Unable to connect to server %s!' %
                     self.jid.getDomain())
        if conres != 'tls':
            logging.warning('unable to estabilish secure connection - '
                            'TLS failed!')

    def authenticate(self):
        """Authenticates the bot"""
        # authenticate
        logging.info('authenticating as %s', self.jid.getNode())
        authres = self.client.auth(self.jid.getNode(), self.passwd)
        if not authres:
            sys.exit('Unable to authorize as %s - check login/password.'
                     % self.jid.getNode())
        if authres != 'sasl':
            logging.warning('unable to perform SASL auth on %s. Old '
                            'authentication method used!',
                            self.jid.getDomain())

    def join(self):
        """Joins the muc"""
        logging.info('joining muc %s', self.muc)
        # indicate presence
        pres = xmpp.Presence(to='%s/logger' % self.muc)
        pres.setTag('x', namespace=xmpp.NS_MUC).setTagData('password',
                                                           self.muc_passwd)
        pres.getTag('x').addChild('history',
                                  {'maxchars':'0', 'maxstanzas':'0'})
        self.client.send(pres)

    def watch(self):
        """Watches the muc"""
        self.connect()
        self.client.RegisterHandler('message', self.cb_message)
        self.client.RegisterHandler('presence', self.cb_presence)
        self.authenticate()
        self.join()
        while True:
            self.client.Process(1)


def main():
    if 'filename' in LOGGING_CONF:
        directory = os.path.dirname(LOGGING_CONF['filename'])
        if not os.path.isdir(directory):
            os.makedirs(directory)
    logging.basicConfig(**LOGGING_CONF)

    Logger().watch()


if __name__ == '__main__':
    try:
        main()
    except SystemExit, e:
        logging.error(e.message)
    except KeyboardInterrupt:
        pass
