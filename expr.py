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
    assoc = [";", "||", "&&","==","<","<=",">",">=", "+", "*","<>"]
 
    def __init__(self,value):
        self.val = value
    def typ(self):
        return "Expression"
    def show(self):
        return self.val
    def rexpr(rexp):
        Expr.re = pre.regex(rexp)
    def isCompound(self):
        return self.typ() == "Compound"
    def tree(self):
        return (self.show(),len(self.show()))
    def printTree(self):
        tr = self.tree()
        lev = depth(tr)
        print level(tr,0)
        for i in range(1,lev):
            print line(tr,i)
            print level(tr,i)        
    def isAssoc(self):
        return self.val in self.assoc
    def head(self):
        return Symbol(self.typ())
        
class Integer(Expr):
    def __init__(self,value):
        self.val = int(value)
    def typ(self):
        return "Integer"
    def show(self):
        return str(self.val)
  
class Real(Expr):
    def __init__(self,value):
        self.val = float(value)
    def typ(self):
        return "Real"
    def show(self):
        return str(self.val)

class String(Expr):
    def show(self):
        return '"'+self.val+'"'     # explicit display of braces for string
    def typ(self):
        return "String"

class Symbol(Expr):
    def typ(self):
        return "Symbol"

class Compound(Expr):
    def __init__(self,value):
        if value:
            self.val = [value]
        else:
            self.val = []
    def typ(self):
        return "Compound"   
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
        if w < s[0][1] and type(s[0][0])== str:
            s.append( (" "*(s[0][1]-w-1),s[0][1]-w-1) )
            w = s[0][1]
        return (s,w)
        
def show(relis,shwlis) :
    if relis == [] :                # nothing to do
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

def level(tr,lev):
    if type(tr[0]) == str:      # single node: leaf 
        if lev == 0:                    # current level
            return tr[0]                # value of the node
        return " "*tr[1]                # this is below leaf: empty                              
    lis = tr[0]                 # list of nodes: interior
    if type(lis[0][0]) != str:      # head is composite
        s = level(lis[0], lev)+" "      # head values to the left
        if lev == 0:                    # this level is head
            return s + " "*tr[1]        # left side and padding to the right
    else:                           # head is symbol
         s = ""      
         if lev == 0:                   # this level is head
            return lis[0][0]+" "*(tr[1]-len(lis[0][0]))# head + padding
                                        # this level is below head
    return s + " ".join(map(lambda x: level(x,lev-1), lis[1:]))        
            
def line(tr,lev):
    if type(tr[0]) == str:      # single node: leaf 
        if lev == 0:                    # current level
            return '_'*tr[1]            # lines here
        return ' '*tr[1]                # this is below leaf: space
    lis = tr[0]                 # list of nodes
    if type(lis[0][0]) != str:      # head is composite
        s = line(lis[0],lev)+" "        # head values to the left
        if lev == 0:
            return s[:-1]+"_"*(tr[1]+1)  # spaces to the right
    else:                           # head is symbol
         s = ""      
         if lev == 0:                   # this level is head
            return '_'*tr[1]            # lines here
    t = map(lambda x: line(x,lev-1), lis[1:]) 
    if t[0][0] == '_':                  # check for lines
        if t[-1] == "":
            t = t[:-1]
            t[-1] = t[-1][:-1]+" "
        else :
            t[-1]=' '*(len(t[-1])-1)    # replaces last by spaces
        return s+'|'+'_'.join(t)
    return s + " ".join(t)
     
def depth(tre):
    if type(tre[0]) == str :
        return 1
    return max(map(depth,tre[0]))+1
 
precedence = {";":1, "=":3, ":=":3, "+=":7, "-=":7, "*=":7, "/=":7,"~~":11,\
          "||":21,"&&":23,"!":24,"==":28,"!=":28,"<":28,"<=":28,">":28,\
          ">=":28, "+":31,"-":31, "*":38, "" :38, "/":39,"^":45,"<>":46}
   
def prior(v):
    if v not in precedence:
        return 100              # default value
    return precedence[v]
 