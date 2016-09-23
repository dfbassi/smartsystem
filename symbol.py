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
import tokenizer
import parser
import expr

title="SMARTS 2.0\nSymbolic Manipulation and Replacement Transformation System"+\
      "\n\tby  Danilo Bassi"

class System(object):
    def __init__(self):      # defines symbolic system
        self.inpnum = 0             # counter for inputs (for a session)
        self.ctxtab = {}            # table of context with name as key
        self.symtab = {}            # table of symbol with name as key
        self.ctxpth = []            # context list search
        self.token = tokenizer.Token
        self.parse = parser.Parse(self)
        self.expre = expr.exprInit()# safe mode (symbols kept as strings)
        
    def config(self,st):            # initializes system structures from string   
        e = self.ToExpr(st)             # list of initial expressions (native list)
        self.setContext(e[0].value())   # initial context (e[0] a string)
        self.setContextPath([e[0].value()])
        Flag.names = e[1].value()[1:]   # flag names list initialized
        for ei in  e[2:] :              # initial configuration for symbols
            self.configSym(ei.value()[1:])
        self.expre = expr.exprInit(self)

    def ToExpr(self,st,h=None) :        # ToExpr converts string into an expression
        tok = self.token(st)
        if h == 1 :                     # looking for single expression
            return self.parse.parse(tok)
        elif type(h) == str :           # looking for all expressions
            exp = self.expre.Sequence(self.expre.Symbol(h)) # sequence with head h
        else :
            exp = []                    # native list of expressions
        while tok.size() :
            exp.append(self.parse.parseExpr(tok))
        return exp
                            
    def isSymbol(self,name):
        return re.match('[a-zA-Z$]',name)   # symbol names start alphabetic
              
    def context(self,name):                 # searches context, defining if needed
        if type(name) == str and self.isSymbol(name): # validity
            if name not in self.ctxtab:
                self.ctxtab[name] = Context(name)
            return self.ctxtab[name]
   
    def setContext(self,name):              # defines new current context
        c = self.context(name)
        if c:                               # name must be valid
            self.curctx = self.context(name)
            self.contextUpdate()
        return self.curctx
        
    def setContextPath(self,names):         # defines new search path
        self.ctxpth = [self.context(n) for n in names if self.context(n)]
        self.contextUpdate()
        
    def contextUpdate(self):                # defines full search list
        self.ctxsearch = self.ctxpth[:]     # a copy
        if self.curctx in self.ctxsearch:
            self.ctxsearch.remove(self.curctx)
        self.ctxsearch.insert(0,self.curctx)# first element is current
              
    def symbol(self,name) :             # finds symbol object, given name
        if not self.isSymbol(name) :    # search for possible operator
            return self.symtab.get(name)
        else :                          # name is valid for  symbol
            ctx = self.ctxsearch[:]     # default search: copy
            if '`' in name :                # name with context
                names = name.rsplit('`',1)      # finding parts
                name = names[1]                 # pure symbol name (second)
                ctx = [self.context(names[0]+'`')]  # context for search here       
            if name in self.symtab :        # there is an entry in symbol table
                s = self.symtab[name]           # finding symbol(s)
                if type(s) != list :            # single symbol
                    if s.ctx in ctx:                # matches context
                        return s                   
                    s2 = Symbol(name,ctx[0])        # not found; new symbol
                    self.symtab[name] = [s,s2]      # symbol table updated: list
                    return s2
                else :                          # list of symbols
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
                
    def configSym(self,par) :       # config symbol data, par is a list 
        s = self.symbol(par[0])         # par[0] is symbol name
        if s:
            for pi in par[1:] :             # par[1]... list for Symbl.select
                s.select(pi)
                if pi[0]=="Operator":       # operator is used as key symtab
                    self.symtab[s.opr] = s
        else :
            print "configSym : not valid ", par[0]

    def deleteSym(self,s):              # removes symbol s from table
        if not s.flg.bit(prot) :        # not protected
            if s.flg.bit(oper) :
                self.symtab.pop(s.opr,None)
            name = s.name
            s1 = self.symtab.get(name)# looking for table entry
            if s1:
                s.name = "Deleted[\""+name+"\"]"
                if s == s1 :                        # single symbol
                    self.symtab.pop(name,None)
                elif type(s1) == list and s in s1:  # list of symbols
                    s1.remove(s)                    # symbol removed
                    print "deleteSym,len(s1): ",len(s1),s1
                    if len(s1) == 1 :               # singleton
                        self.symtab[name] = s1[0]
        else:
            print "Protected: cannot delete ",s.ctx.show(),name

    def prior(self,s):                  # finds priority number
        if type(s) != Symbol :
            s = self.symtab.get(s)
        if s and s.flg.bit(oper) :      # operator
            return s.pre                # this is operator priority
        return 100                      # default
        
    def isAssoc(self,s) :               # finds associativity
        if type(s) != Symbol :
            s = self.symtab.get(s)
        return s and s.flg.bit(assoc)

    def isOperator(self,op,typ) :       # finds if op is operator of certain type
        s = self.symtab.get(op)         # expecting op str
        return s and s.opr == op and s.opt == typ
        
    def showContext(self):
        return ["Current Context: "+ self.curctx.show(),
             "Context Path   : "+",".join([c.show() for c in self.ctxpth]),
             "Context List   : "+",".join(sorted(self.ctxtab.keys()))]
             
    def showSymbol(self,q=0):
        s = ["Number of defined symbols :"+format(len(self.symtab),'4d')]
        if q>=1:
            s += [self.symtab[k].show(2*q-2) for k in sorted(self.symtab)]
        return s
   
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
    def __init__(self,nam):     # new context: name
        self.name = nam                 # symbol name
    def show(self):             # returns context name
        return self.name
 
class Symbol(object):
    def __init__(self,nam,ct,f=0):      # new symbol: name, context, flags
        self.name = nam                 # symbol name
        self.ctx  = ct                  # context number
        self.flg  = Flag(f)             # flag initial value
        
    def operator(self,par):             # initilizes symbol operator (if any)
        self.opt = par[0]               # par[0] is the operator type
        self.pre = par[1]               # par[1] is the precedence number (int)
        self.opr = par[2]               # par[2] is the operator string (str)
        self.flg.on(oper)               # set flag
    
    def on(self,flgnam):
        self.flg.on(self.flg.number(flgnam))
    
    def off(self,flgnam):
        self.flg.off(self.flg.number(flgnam))
        
    def select(self,par):
        fun={"Operator":self.operator,"FlagOn":self.on,"FlagOff":self.off}
        fun[par[0]](par[1:])

    def show(self,t=None):
        if not t:
            return self.name
        if t % 2 == 0 :
            s = format(self.name,'10s')
        else:
            s = ' '*10
        s += "("+self.ctx.show()+")"
        t /= 2
        if t % 3 == 1:
            s += " Flags "+self.flg.binary()
        if  (t/3) % 2 and self.flg.bit(oper):
            s += " "+format(self.opt,'7s')+"("+format(self.pre,'2d')+") "+format(self.opr,'4s')
        if t % 3 == 2:
            s += " Flags: "+", ".join(self.flg.lis())    
        return s

# variables defined as mask for flag value
[lock, prot, rdprot, temp, stub, func, nev1, nevr, neall, necom, neseq, num, nnum1,
 nnumr, nnuma, const, lista, assoc, comm, idem, oper, val,dval,uval,defv]\
     = [2**i for i in range(25)]

class Flag(object):
    names = []
    fmt = '025b'
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
    def binary(self):               # output in binary format
        return format(self.flag,self.fmt)   
    def index(self,n):              # find index given a flag name          
        return self.names.index(n)
    def number(self,nam):
        if type(nam) == str:
            return 2**self.names.index(nam)
        elif type(nam) == list and nam !=[]:
            return reduce(op.or_,[2**self.names.index(n) for n in nam])
        return 0

def init(fl):                       # initializes system structures from file
    s = System()                    # system instatiation
    d = sys.ReadStr(fl)             # reads configuration data from file
    s.config(d)
    return s
      
        
 