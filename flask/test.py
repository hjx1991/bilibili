#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Student:
    def __init__(self, name, score):
        self.name = name
        self.__score = score
    @property
    def score(self):
        return self.__score
    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score

s=Student('hjx',25)
test=s.score()
print(test)