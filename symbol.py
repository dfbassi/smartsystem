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
import operator as op

title="SMARTS 2.0\nSymbolic Manipulation and Replacement Transformation System"+\
      "\n\tby  Danilo Bassi"

class System(object):
    def __init__(self,ctxt=["System`"]): # defines a symbolic system with context
        self.ctxcnt = 0         # counter for contexts
        self.symcnt = 0         # counter for symbols
        self.inpnum = 0         # counter for inputs (for a session)
        self.ctxnam = {}        # table of context names
        self.ctxcod = {}        # table of context codes
        self.symtab = {}        # table for symbol object: symtab[cod] -> sym
        self.symcod = {}        # table for symbol codes: symcod[name] -> [cods]
        self.infxcod= {}        # table for infix codes: infix[symbol] -> cod
        self.prfxcod= {}        # table for prefix codes: prefix[symbol] -> cod
        if type(ctxt) == str:
            ctxt = [ctxt]
        for n in ctxt:          # input context(s)
            self.context(n)
        self.setCur(ctxt[0])
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
        
    def info(self,q=0):
        s = [ "Current Context: "+ self.current]
        s.append("Context Search : "+",".join([self.ctxnam[i] for i in self.ctxlis]))
        s.append("Context Table  : "+",".join([self.ctxnam[i+1] for i in range(self.ctxcnt)]))
        s.append("Number of symbols : "+str(self.symcnt))
        if q>=1:
            s += [format(n,'3d')+" "+self.symtab[n].show(q) for n in range(1,self.symcnt+1)]
        return s

    def numsym(self,fullname):                  # find symbol number
        names = fullname.rsplit('`',1)
        if len(names) == 2:
            ctx = [self.context(names[0]+'`')]  # first part is the context
        else:
            ctx = [self.currnum]+self.ctxlis   # no context given: current & list
#        print "ctx search index : ", ctx
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
        
    def symbol(self,name) :             # finds symbol object, given name
        return self.symtab[self.numsym(name)]
    
    def inpLoop(self,init=title):
        print init
        while True :                    # infinite loop
            self.inpnum += 1            # input counter increased
            instr = raw_input("In["+str(self.inpnum)+"]:= ")
            if re.match(r'Quit',instr): # session ends with Quit[]
                break
            inexp = sys.ToExpr(instr,1) # input is parsed into expression
            ouexp = sys.Eval(inexp)     # evaluation
            print "Out["+str(self.inpnum)+"]= "+ouexp.show()

class Symbol(object):
    def __init__(self,nam,ct,f=0):      # new symbol: name, context, flags
        self.name = nam                 # symbol name
        self.ctx  = ct                  # context number
        self.flg  = Flag(f)             # flag initial value
        
    def operator(self,par):             # initilizes symbol operator (if any)
        self.pre = par[1]               # par[1] is the precedence nuber (int)
        self.opr = par[2]               # par[2] is the operator (str)
        self.on(par[0])                 # par[0] is the type (in-,pre-,post-fix)
    
    def on(self,flgnam):
        self.flg.on(self.flg.number(flgnam))
    
    def off(self,flgnam):
        self.flg.off(self.flg.number(flgnam))
        
    def select(self,par):
        fun={"Operator":self.operator,"FlagOn":self.on,"FlagOff":self.off}
        fun[par[0]](par[1:])

    def show(self,t=0):
        s = format(self.name,'10s')
        if t>= 1 :
            s += "("+str(self.ctx)+")"
            if self.flg.bit(infix | prefix):
                s += " op("+format(self.pre,'2d')+") "+format(self.opr,'4s')
                if self.flg.bit(infix):
                    s +="infix "
                else :
                    s +="prefix"
        if t == 2:
            s += " flags "+self.flg.binary()
        if t == 3:
            s += " flags "+", ".join(self.flg.lis())    
        return s

# variables defined as mask for flag value
[delete,lock, prot, rdprot, temp, stub, func, nev1, nevr, neall, necom, neseq, num,\
 nnum1, nnumr, nnuma, const, lista, assoc, comm, idem, prefix, infix, pstfix,\
 val, dval, uval, defv ] = [2**i for i in range(28)]

class Flag(object):
    names = []
    fmt = '028b'
    def __init__(self,f):
        if type(f) != int:
            f = self.number(f) # convert flag name(s) into number before
        self.flag = f
    def on(self,f):                 # set flag
        self.flag |= f  
    def off(self,f):                # clear flag
        self.flag &= ~f
    def bit(self,f):                # test flag
        return self.flag & f 
    def lis(self):
        return [self.names[i] for i in range(len(self.names)) if 2**i & self.flag]
    def binary(self):           # output in binary format
        return format(self.flag,self.fmt)   
    def index(self,n):          # find index given a flag name          
        return self.names.index(n)
    def number(self,nam):
        if type(nam) == str:
            return 2**self.names.index(nam)
        elif type(nam) == list and nam !=[]:
            return reduce(op.or_,[2**self.names.index(n) for n in nam])
        return 0
    

precedence = {";":1, "=":3, ":=":3, "+=":7, "-=":7, "*=":7, "/=":7,"~~":11,\
          "||":21,"&&":23,"!":24,"==":28,"!=":28,"<":28,"<=":28,">":28,\
          ">=":28, "+":31,"-":31, "*":38, "" :38, "/":39,"^":45,"<>":46}
   
def prior(v):
    if v not in precedence:
        return 100              # default value
    return precedence[v]

def init(fl,ctxt=["System`"]):      # initializes system structures from file
    s = System(ctxt)                # system class instantiated with context
    e = sys.Read(fl)                # list of initial expressions (native list)
    Flag.names = e[0].value()[1:]   # flag names list initialized
    for ei in  e[1:] :
        ev = ei.value()
        print ev
        sym = s.symbol(ev[1])       # gets symbol object (creating when necessary)
        for p in ev[2:] :
            sym.select(p[1:])
    return s
        
        
 