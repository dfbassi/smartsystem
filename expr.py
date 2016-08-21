# -*- coding: utf-8 -*-
"""
    Created on Thu Aug 18 22:13:00 2016
    
    @author: danilobassi
"""

"""
    SMARTS
    Symbolic Expression Classes
    
"""


class Expr(object):
    def __init__(self,value):
        self.val = value
    def show(self):
        return self.val

class Number(Expr):
    def __init__(self,value):
        if '.' in value :     # test for float
            self.val = float(value)
            self.typ = "Real"
        else:
            self.val = int(value)
            self.typ = "Integer"

class Symbol(Expr):
    typ = "Symbol"

class Compound(Expr):
    typ = "Compound"
    def __init__(self,value):
        if value:
            self.val = [value]
        else:
            self.val = []
    def append(self,value):
        self.val.append(value)
    def prepend(self,value):
        self.val.insert(0,value)
    def show(self):
        return self.val[0].show()+repr(map(lambda e: e.show(),self.val[1:]))

class String(Expr):
    typ = "String"
    def show(self):
        return '"'+self.val+'"'
