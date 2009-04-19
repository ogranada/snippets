#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.


"""
    flatten_nested_lists
    ====================

    How to flatten nested lists.

    .. moduleauthor::  Sebastian Wiesner  <basti.wiesner@gmx.net>
"""


def flatten(nested):
    """
    Flattens descending nested lists like ``[a, [b, [c, d]]]``.

    :returns: a flattened list
    """
    flattened = []
    while len(nested) > 1:
        head, tail = nested
        flattened.append(head)
        nested = tail
    if nested:
        flattened.append(nested[0])
    return flattened


def main():
    from pprint import pprint
    nested = ['a', ['b', ['c', ['d']]]]
    pprint(nested)
    pprint(flatten(nested))


if __name__ == '__main__':
    main()

