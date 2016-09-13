# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 23:29:55 2016

@author: danilobassi
"""

"""
    SMARTS
    
    Symbol Class
    
"""
class Context(object):
    def __init__(self,names=["System`"]):
        self.ctxcnt = 0         # counter for contexts
        self.symcnt = 0         # counter for symbols
        self.ctxcod = {}        # table of codes for context
        self.symtab = {}        # table for symbol object: symtab[cod] -> sym
        self.symcod = {}        # table for symbol cods: symcod[name] -> [cods]
        if type(names) == str:
            names = [names]
        for n in names:         # add context(s)
            self.context(n)
        self.setCur(names[0])
        self.ctxlis = []
              
    def context(self,nam):
        if nam not in self.ctxcod:
            self.ctxcnt +=1
            self.ctxcod[nam] = self.ctxcnt
        return self.ctxcod[nam]
   
    def setCur(self,nam):
        self.current = nam
        self.currnum = self.context(nam)
        
    def setPath(self,names):
        self.ctxlis = [self.context(n) for n in names]
       
    def numsym(self,fullname):                  # find symbol number
        names = fullname.rsplit('`',1)
        if len(names) == 2:
            ctx = [self.context(names[0]+'`')]  # first part is the context
        else:
            ctx = [self.current]+self.ctxlis   # no context given: current & list
        print "ctx search index : ", ctx
        if names[-1] in self.symcod:            # name in lookup table
            cod = self.symcod[names[-1]]        # find symbol codes
            cct = [self.symtab[c].ctxnum for c in cod] # find context(s)
            for c in ctx:                       # searching in the same order
                if c in cct:                    # found !
                    return cod[ cct.index(c) ]  # returning code of symbols
        else:
            cod = None
        self.symcnt += 1                        # code for new symbol
        self.symtab[self.symcnt] = Symbol(names[-1],ctx[0])   # new symbol
        if cod :
            self.symcod[names[-1]].append(self.symcnt)
        else:
            self.symcod[names[-1]] = [self.symcnt]
        return self.symcnt
       
    def delsym(self,num):           # remove symbol
        nam = self.symtab[num].name
        self.symcod[nam].remove(num)
        
class Symbol(object):
    def __init__(self,nam,ct):
        self.name = nam             # symbol name
        self.ctxnum = ct            # context number
        self.flg = 0                # flag
        
        
       
 