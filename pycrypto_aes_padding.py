#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# pycrypt AES extended with random bit padding
# Copyright (c) 2007 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


import os
from Crypto.Cipher import AES


def encrypt(key, iv, data):
    blocksize = len(iv)
    # calculate the number random bits to be added
    # len(data) + 1: the length of the data with the length prefix included
    padval = blocksize - ((len(data) + 1) % blocksize)
    # prepend the length prefix and append random bits
    data = ''.join([chr(padval), data, os.urandom(padval)])
    a = AES.new(key, AES.MODE_CBC, iv)
    encrypted = a.encrypt(data)
    # remove unencrypted stuff and hope, that it really vanishes from memory
    return encrypted

def decrypt(key, iv, data):
    a = AES.new(key, AES.MODE_CBC, iv)
    decrypted = a.decrypt(data)
    # read and remove the length prefix from data
    padval = ord(decrypted[0])
    data = decrypted[1:]
    # remove trailing random garbage, if there is some
    if padval > 0:
        data = data[:-padval]
    return data

def test_encrypt():
    blocksize = 16
    key = os.urandom(32)
    iv = os.urandom(blocksize)
    f = open('key', mode='wb')
    f.write(key)
    f.close()
    f = open('iv', mode='wb')
    f.write(iv)
    f.close()
    data = 'Hello world, how are you?'
    print data
    encrypted = encrypt(key, iv, data)
    f = open('encrypted', 'wb')
    f.write(encrypted)
    f.close()
    print 'encrypted'

def test_decrypt():
    block_size = 16
    f = open('key', 'rb')
    key = f.read()
    f.close()
    f = open('iv', 'rb')
    iv = f.read()
    f.close()
    f = open('encrypted', 'rb')
    encrypted = f.read()
    f.close()
    print 'decrypted'
    print decrypt(key,iv,encrypted)


if __name__ == '__main__':
    test_encrypt()
