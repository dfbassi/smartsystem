# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 23:29:55 2016

@author: danilobassi
"""

"""
    SMARTS
    
    System  Class
    Context Class
    Symbol  Class
    Flag    Class
    
"""

import sysfunc as sys
import re
import operator as op

title="SMARTS 2.0\nSymbolic Manipulation and Replacement Transformation System"+\
      "\n\tby  Danilo Bassi"

class System(object):
    def __init__(self,c=None):      # defines a symbolic system with context
        self.inpnum = 0                     # counter for inputs (for a session)
        self.ctxtab = {}                    # table of context with name as key
        self.symtab = {}                    # table of symbol with name as key
        self.ctxpth = []                    # initial context search path
        if self.context(c):
            c = 'Core`'                     # default context
        self.setContext(c)                  # initial context (current) is set
        
    def isSymbol(self,name):
        return re.match('[a-zA-Z$]',name)   # symbol names starts alphabetic
              
    def context(self,name):
        if type(name) == str and self.isSymbol(name):
            if name not in self.ctxtab:
                self.ctxtab[name] = Context(name)
            return self.ctxtab[name]
   
    def setContext(self,name):
        c = self.context(name)
        if c:                               # valid symbol name
            self.curctx = c
            self.contextUpdate()
            return c
        
    def setContextPath(self,names):         # defines new search path
        self.ctxpth = [self.context(n) for n in names if self.context(n)]
        self.contextUpdate()
        
    def contextUpdate(self):                # defines full search list
        self.ctxsearch = self.ctxpth[:]     # a copy
        if self.curctx in self.ctxpth:
            self.ctxpth.remove(self.curctx)
        self.ctxsearch.insert(0,self.curctx)# firts element is current
              
    def showContext(self):
        return ["Current Context: "+ self.curctx.show(),
             "Context Path   : "+",".join([self.c.show() for c in self.ctxpth]),
             "Context List   : "+",".join(self.ctxtab.keys())]
             
    def showSymbol(self,q=0):
        s = ["Number of defined symbols :"+format(len(self.symtab),'4d')]
        if q>=1:
            s += [self.symtab[k].show(2*q-2) for k in self.symtab.keys()]
        return s

    def symbol(self,name) :             # finds symbol object, given name
        if not self.isSymbol(name) :    # search for possible operator
            if name in self.symtab :
                return self.symtab[name]
        else :                          # name is valid for  symbol
            ctx = self.ctxsearch            # default search: copy
            if '`' in name :                # name with context
                names = name.rsplit('`',1)      # finding parts
                name = names[1]                 # pure symbol name (second)
                ctx = [self.context(names[0])]  # search here       
            if name in self.symtab :        # there is an entry in symbol table
                s = self.symtab[name]           # finding symbol(s)
                if type(s) != list :            # single symbol
                    if s.ctx in ctx:                # matches context
                        return s                   
                    s2 = Symbol(name,ctx[0])        # not found; new symbol
                    self.symtab[name] = [s,s2]      # symbol table updated: list
                    return s2
                else :                          # 2 or more symbols
                    symctx = [si.ctx for si in s]
                    for c in ctx:                   # searching in the same order
                        if c in symctx:                 # matches context 
                            return s[symctx.index(c)]   # returns symbol
                    sn = Symbol(name,ctx[0])        # not found; new symbol
                    self.symtab[name].append(sn)    # symbol table list updated
                    return sn
            else :                          # no entry in symbol table
                s = Symbol(name,ctx[0])         # not found: new symbol
                self.symtab[name] = s           # first entry for symbol name
                return s
    
    def delsym(self,num):               # remove symbol
        nam = self.symtab[num].name
        self.symcod[nam].remove(num)    # remove reference
        self.symtab[num].flg.on(delete) # set delete flag
        
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

class Context(object):
    def __init__(self,nam):      # new context: name
        self.name = nam                 # symbol name
    def show(self):
        return self.name
 
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
        if t % 2 == 0 :
            s = format(self.name,'10s')
        else:
            s = ' '*10
        s += "("+self.ctx.show()+")"
        t /= 2
        if t % 3 == 1:
            s += " Flags "+self.flg.binary()
        if  (t/3) % 2 and self.flg.bit(infix | prefix):
            if self.flg.bit(infix):
                s +=" Infix "
            else :
                s +=" Prefix"           
            s += "("+format(self.pre,'2d')+") "+format(self.opr,'4s')
        if t % 3 == 2:
            s += " Flags: "+", ".join(self.flg.lis())    
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

def init(fl,ctxt="Core`"):          # initializes system structures from file
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
        
        
 