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
    def tree(self):
        return (self.show(),len(self.show()))

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
    def tree(self):
        s = map(lambda e: e.tree(),self.val)
        w = sum(map(lambda x:x[1],s[1:])) + len(s)-2
        print " w, s : ",w,s
        if w < s[0][1] and type(s[0][0])== str:
            s.append( (" "*(s[0][1]-w-1),s[0][1]-w-1) )
            w = s[0][1]
        return (s,w)

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

def printTree(tr,lev=1):
    print level(tr,0)
    for i in range(1,lev):
        print line(tr,i)
        print level(tr,i)

def level(tr,lev):
    if type(tr[0]) == str:              # single node: leaf 
        if lev == 0:                    # current level
            return tr[0]                # value of the node
        return " "*tr[1]                # this is below leaf: empty
    lis = tr[0]                         # list of nodes
    if type(lis[0][0]) == str:          # first node is head, rest are children
        if lev == 0:                    # head is simple
            return lis[0][0]+" "*(tr[1]-len(lis[0][0]))         # head + padding
        return " ".join(map(lambda x: level(x,lev-1), lis[1:])) # rest
    s = level(lis[0], lev)
    if lev == 0:
        return s + " "*(tr[1]+1)
    return s +" " + " ".join(map(lambda x: level(x,lev-1), lis[1:]))        
            
def line(tr,lev):
    if type(tr[0]) == str:              # single node: leaf 
        if lev == 0:                    # current level
            return '_'*tr[1]            # lines here
        return ' '*tr[1]                # this is below leaf: space
    lis = tr[0]                         # list of nodes
    if type(lis[0][0]) == str:          # first node is head, rest are children
        if lev == 0:                    # head is simple
            return '_'*tr[1]            # lines here
        s = map(lambda x: line(x,lev-1), lis[1:]) 
        if s[0][0] == '_':
            s[-1]=' '*(len(s[-1])-1)
            return '|'+'_'.join(s)
        return " ".join(s)
    s = line(lis[0], lev)
    if lev == 0:
        return s + " "*(tr[1]+1)
    return s +" " + '_'.join(map(lambda x: line(x,lev-1), lis[1:]))        
     