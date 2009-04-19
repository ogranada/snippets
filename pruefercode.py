#!/usr/bin/python
# -*- coding: utf-8 -*-


from pprint import pprint


def code2tree(code):
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
    #pprint(code2tree(code))
    pprint(code2tree_steger(code))


if __name__ == '__main__':
    main()
