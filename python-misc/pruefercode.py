#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <lunaryorn@googlemail.com>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    pruefercode
    ===========

    Implements two different algorithms to create a graph (as sequence of
    tuples of linked nodes) from a Prüfer sequence.

    .. moduleauthor::  Sebastian Wiesner  <lunaryorn@googlemail.com>
"""

from pprint import pprint


def code2tree(code):
    """
    This algorithm comes from Wikipedia.
    """
    degree = {}
    for i in xrange(1, len(code) + 3):
        degree[i] = 1
    for a in code:
        degree[a] += 1

    tree = set()
    for a in code:
        j = min(k for k in degree if degree[k] == 1)
        tree.add((j, a))
        degree[j] -= 1
        degree[a] -= 1
    tree.add(tuple(k for k in degree if degree[k] == 1))
    return tree


def code2tree_steger(code):
    """
    This algorithm comes from a text book, dealing with discrete structure
    mathematics.
    """
    tree = set()
    s = set()
    n = set(xrange(1, len(code) + 3))
    for i, t in enumerate(code):
        s_i = min(e for e in (n - s) if e not in code[i:])
        tree.add((s_i, t))
        pprint(tree)
        s.add(s_i)
    tree.add(tuple(n - s))
    return tree


def main():
    code = [2, 3, 5, 5, 3, 7, 10, 8, 10]
    pprint(code2tree(code))
    pprint(code2tree_steger(code))


if __name__ == '__main__':
    main()
