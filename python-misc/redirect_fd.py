# -*- coding: utf-8 -*-
# Copyright (c) 2012 Sebastian Wiesner <lunaryorn@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
from contextlib import contextmanager


@contextmanager
def suppress_output(fd):
    """
    Suppress output to the given ``fd``::

       with suppress_fd(sys.stderr):
           # in this block any output to standard error is suppressed

    ``fd`` is an integral file descriptor, or any object with a ``fileno()``
    method.
    """
    if hasattr(fd, 'fileno'):
        # we were given a file-like object with an underlying fd
        if hasattr(fd, 'flush'):
            # flush Python-side buffers before redirecting
            fd.flush()
        # get the fd to redirect
        fd = fd.fileno()

    # duplicate the file descriptor to restore it eventually
    oldfd = os.dup(fd)
    try:
        # open the trash can
        devnull = os.open(os.devnull, os.O_WRONLY)
        try:
            # point the file descriptor to the trash can
            os.dup2(devnull, fd)
        finally:
            # close the old trash can descriptor, we don't need it anymore
            # since the fd now points to the trash can
            os.close(devnull)
        # enter the callers block
        yield
        # restore the file descriptor
        os.dup2(oldfd, fd)
    finally:
        # close the duplicated copy of the original fd, we don't need it
        # anymore now that fd is restored
        os.close(oldfd)
