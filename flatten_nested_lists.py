#!/usr/bin/python
# -*- coding: utf-8 -*-


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

