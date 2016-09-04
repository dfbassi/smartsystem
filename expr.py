# -*- coding: utf-8 -*-
"""
    Created on Thu Aug 18 22:13:00 2016
    
    @author: danilobassi
"""

"""
    SMARTS
    
    Symbolic Expression Classes
    
"""
import parseregex as pre

class Expr(object):
    re = pre.regex(r"$\[($(,$)*)?\]")
    def __init__(self,value):
        self.val = value
    def show(self):
        return self.val
    def rexpr(rexp):
        Expr.re = pre.regex(rexp)
    def isCompound(self):
        return self.typ == "Compound"

class Number(Expr):
    def __init__(self,value):
        if '.' in value :               # test for float
            self.val = float(value)
            self.typ = "Real"
        else:
            self.val = int(value)
            self.typ = "Integer"
    def show(self):
        return str(self.val)

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
    def insert(self,value,pos):
        self.val.insert(pos,value)
    def head(self):
        return self.val[0]
    def show(self):
        return show(Expr.re, map(lambda e: e.show(),self.val))

class String(Expr):
    typ = "String"
    def show(self):
        return '"'+self.val+'"'     # explicit display of braces for string
        
def show(relis,shwlis) :
    if relis == [] :              # nothing to do
        return None
    if type(shwlis[0]) == str:
        shwlis.insert(0,1)
#        print "show (shwlis) : ", shwlis
    res = ""
    if relis[0] in {'?','*','+'}  :
        i = 1
    else :
        i = 0
    if relis[0] in {'?','*'}  :
        nmin = 0
    else :
        nmin = 1
    n = 0
    while True:
        initial = shwlis[0]
        res1 = ""
        for item in  relis[i:] :
#            print "show, for : ", item, "\t", shwlis[0]
            res2 = showitem(item,shwlis)
            if type(res2) != str :
                shwlis[0] = initial
                break                   # ending inner loop
            res1 += res2                # result from item is added
        else :
            res += res1
            n += 1
            if relis[0] in {'*','+'}  :
                continue
        if n < nmin :
            return None                 # failure min repetitions
        else :
            return res
    
def showitem(item,shwlis):
    if type(item) == list :         
        return show(item,shwlis)
    if item == '$' :                # this represents full expression
        if shwlis[0] < len(shwlis) :
            shwlis[0] += 1
            return shwlis[shwlis[0]-1]
    else :
        return item                 # item copied to output
            