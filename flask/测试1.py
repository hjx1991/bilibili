#!/usr/bin/env python3
# -*- coding: utf-8 -*-
hjx =1
def outer(func):
    hjx=0
    def inner(a,b):
        nonlocal hjx
        hjx +=1
        print(hjx)
        return func(a,b)
    return inner

@outer
def test(a,b):
    print("a+b=%d" %(a+b))
    return

test(1,2)
test(2,2)

print("global hjx:",hjx)
