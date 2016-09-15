# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 23:29:55 2016

@author: danilobassi
"""

"""
    SMARTS
    
    System Class
    Symbol Class
    Flag   Class
    
"""

import sysfunc as sys
import re

title="SMARTS 2.0\nSymbolic Manipulation and Replacement Transformation System"+\
      "\n\tby Danilo Bassi"

class Context(object):
    def __init__(self,names=["System`"]): # default context is System
        self.ctxcnt = 0         # counter for contexts
        self.symcnt = 0         # counter for symbols
        self.inpnum = 0         # counter for inputs (for a session)
        self.ctxnam = {}        # table of context names
        self.ctxcod = {}        # table of context codes
        self.symtab = {}        # table for symbol object: symtab[cod] -> sym
        self.symcod = {}        # table for symbol codes: symcod[name] -> [cods]
        self.infxcod= {}        # table for infix codes: infix[symbol] -> cod
        self.prfxcod= {}        # table for prefix codes: prefix[symbol] -> cod
        if type(names) == str:
            names = [names]
        for n in names:         # add context(s)
            self.context(n)
        self.setCur(names[0])
        self.ctxlis = [self.currnum]
              
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
        s.append("Context Search : "+",".join([self.ctxnam[i] for i in self.ctxlis]))
        s.append("Context Table  : "+",".join([self.ctxnam[i+1] for i in range(self.ctxcnt)]))
        if q>=1:
            s.append("Number of symbols : "+str(self.symcnt))
        if q>=2:
            s += [str(n)+" : "+self.symtab[n].show(q) for n in range(1,self.symcnt+1)]
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
        self.symtab[num].flg.on(delete) # set delete flag
    
    def infix(self,name,oper,pre) :     # add infix operator to symbol
        num = self.numsym(name)
        self.infxcod[oper] = num
        self.symtab[num].operator(oper,pre,prefix)
        
    def prefix(self,name,oper,pre) :    # add prefix operator to symbol
        num = self.numsym(name)
        self.prfxcod[num] = oper
        self.symtab[num].operator(oper,pre,infix)
      
    def inpLoop(self,init=title):
        print init
        while True :                    # infinite loop
            self.inpnum += 1            # input counter increased
            instr = raw_input("In["+str(self.inpnum)+"]:= ")
            if re.match(r'Quit',instr) :
                break
            inexp = sys.ToExpr(instr,1) # input is parsed into expression
            ouexp = sys.Eval(inexp)     # evaluation
            print "Out["+str(self.inpnum)+"]= "+ouexp.show()

class Symbol(object):
    def __init__(self,nam,ct,f=0):  # new symbol: name, context, flags
        self.name = nam             # symbol name
        self.ctx  = ct              # context number
        self.flg  = Flag(f)         # flag (default value)
        
    def operator(self,op,pr,f):     # symbol with op., precedence, type
        self.opr = op
        self.pre = pr
        self.flg.on(f|preced)

    def show(self,t=0):
        s = self.name
        if t>= 1 :
            s += " "*(10 -len(self.name))+"("+str(self.ctx)+")"
            if self.flg.bit(preced):
                s += " op: "+self.opr+","+str(self.pre)
                if self.flg.bit(infix):
                    s +=",infix "
                else :
                    s +=",prefix"
        if t == 2:
            s += " flags: "+self.flg.binary()
        if t == 3:
            s += " flags: "+", ".join(self.flg.lis())    
        return s

# variables defined as mask for flag variable
[delete,lock,prot,temp,val,num,nnum1,nnumr,nev1,nevr,idem,comm,assoc,lista,\
 infix,prefix,preced]= [2**i for i in range(17)]

class Flag(object):
    names = ["del","loc","prot","temp","val","num","nnum1","nnumr","nev1","nevr",\
             "idem","comm","assoc","listable","infix","prefix","precedence"]
    num = len(names)
    def __init__(self,f=0):
        self.flag = f
    def on(self,f):                             # set flag
        self.flag |= f  
    def off(self,f):                            # clear flag
        self.flag &= ~f
    def bit(self,f):                            # test flag
        return self.flag & f 
    def lis(self):
        return [self.names[i] for i in range(self.num) if 2**i & self.flag]
    def binary(self):
        return bin(self.flag)
    def name(self,i):
        return self.names[i]

precedence = {";":1, "=":3, ":=":3, "+=":7, "-=":7, "*=":7, "/=":7,"~~":11,\
          "||":21,"&&":23,"!":24,"==":28,"!=":28,"<":28,"<=":28,">":28,\
          ">=":28, "+":31,"-":31, "*":38, "" :38, "/":39,"^":45,"<>":46}
   
def prior(v):
    if v not in precedence:
        return 100              # default value
    return precedence[v]
    
prefixtab = {"-":"Minus","!":"Not"}
infixtab  = {";":"CompoundExpr", "|":"Altern", "=":"Set", ":=":"SetAfter",\
          "+=":"AddTo", "-=":"SubFrom", "*=":"TimesTo", "/=":"DivideBy",\
          "~~":"StringExpr", "||":"Or", "&&":"And", "==":"Equal", "===":"SameQ",\
          "!=":"Unequal","<":"Less","<=":"LessEq",">":"Greater",">=":"GreaterEq",\
          "+":"Add", "-":"Sub", "*":"Times", "/":"Divide", "^":"Power",\
          ".":"Dot","<>":"StringJoin"}
postfixtab = {"!":"Factorial","&":"Function"}
 
        
        
        
       
 