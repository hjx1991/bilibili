#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def outer(func):
    count = [0]
    def inner(a, b):
        count[0] += 1
        print(count[0])
        return func(a, b)
    return inner

@outer
def add(a, b):
    print("a + b value is %s" % (a + b))
    return


if __name__ == '__main__':
    add(2, 3)