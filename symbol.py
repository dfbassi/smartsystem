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
        self.ctxnam = {}        # table of context names
        self.ctxcod = {}        # table of context codes
        self.symtab = {}        # table for symbol object: symtab[cod] -> sym
        self.symcod = {}        # table for symbol codes: symcod[name] -> [cods]
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
            self.ctxnam[self.ctxcnt] = nam
        return self.ctxcod[nam]
   
    def setCur(self,nam):
        self.current = nam
        self.currnum = self.context(nam)
        
    def setPath(self,names):
        self.ctxlis = [self.context(n) for n in names]
        
    def show(self):
        return self.current

    def info(self,q=0):
        s = [ "Current Context: "+ self.current]
        s.append("Context Search : "+" ".join([self.ctxnam[i] for i in self.ctxlis]))
        s.append("All Contexts   : "+" ".join([self.ctxnam[i+1] for i in range(self.ctxcnt)]))
        if q>=1:
            s.append("Symbols defined : "+str(self.symcnt))
        if q>=2:
            s += map(lambda n : str(n)+" "+self.symtab[n].name+" "+str(self.symtab[n].ctx),\
            range(1,self.symcnt+1))
        return s

    def numsym(self,fullname):                  # find symbol number
        names = fullname.rsplit('`',1)
        if len(names) == 2:
            ctx = [self.context(names[0]+'`')]  # first part is the context
        else:
            ctx = [self.currnum]+self.ctxlis   # no context given: current & list
        print "ctx search index : ", ctx
        if names[-1] in self.symcod:            # name in lookup table
            cod = self.symcod[names[-1]]        # find symbol codes
            cct = [self.symtab[c].ctx for c in cod] # find context(s)
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
       
    def delsym(self,num):               # remove symbol
        nam = self.symtab[num].name
        self.symcod[nam].remove(num)    # remove reference
        self.symtab[num].flg.on('del')  # set del flag
     
class Symbol(object):
    def __init__(self,nam,ct):
        self.name = nam             # symbol name
        self.ctx  = ct              # context number
        self.flg  = Flag()          # flag (default value)
    def show(self,t=0):
        s = self.name
        if t>= 1 :
            s += " ctx: "+str(self.ctx)
        if t == 2:
            s += " flags: "+self.flg.binary()
        if t == 3:
            s += " flags: "+", ".join(self.flg.lis())
        return s
        
class Flag(object):
    names = ["del","loc","prot","temp","val","num","nnum1","nnumr","nev1","nevr",\
             "idem","comm","assoc","list","infix","prefix"]
    code  = dict(zip(names,[2**i for i in range(len(names))]))
    num = len(names)
    def __init__(self,f=0):
        self.flag = f
    def on(self,f):                             # set named flag
        self.flag |= self.code[f]  
    def off(self,f):                            # clear named flag
        self.flag &= ~self.code[f]
    def bit(self,f):                            # test named flag
        return self.flag & self.code[f] 
    def lis(self):
        return [self.names[i] for i in range(len(self.num)) if 2**i & self.flag]
    def binary(self):
        return bin(self.flag)

    

   
        
        
        
       
 