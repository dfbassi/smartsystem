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
    def __init__(self):             # defines symbolic system
        self.inpnum = 0                 # counter for inputs (for a session)
        self.ctxtab = {}                # table of context with name as key
        self.symtab = {}                # table of symbol with name as key
        self.ctxpth = []                # context list search
        self.token = tokenizer.Token    # tokenizer function access
        self.expre = expr.Expr()        # Expr object (safe mode, no symbol table)
        self.parse = parser.Parse(self) # Parse object
        
    def config(self,st):            # initializes system structures from string   
        e = self.strToExpr(st,self.expre.list)# initial expression list
        v = e.toBase('List')            # conversion into base list and types
        self.setContext(v[0])           # initial context (v[0] a string)
        self.setContextPath([v[0]])
        Flag.names = v[1]               # flag names list initialized, list v[1]
        for vi in  v[2:] :              # initial configuration for symbols
            self.configSym(vi)
        self.expre = expr.Expr(self)    # new Expr object using symbol table
        sys.expre  = self.expre
        print self.show()

    def strToExpr(self,st,hd=None): # converts string into an expression
        tok = self.token(st)            # st: input string, hd: head expression (symbol)
        if not hd :                     # looking for single expression (no head)
            return self.parse.parse(tok) 
        exp = self.expre.Sequence([hd]) # sequence with head hd (symbol)
        while tok.size() :
            exp.append(self.parse.parse(tok))
        return exp
        
    def read(self,flname,hd=None):  # reads text from file converts into expression 
        return self.strToExpr(sys.ReadStr(flname),hd)
            
    def isSymbol(self,name):                # symbol name (including possible context)
        return re.match(r'([a-zA-Z$]\w*`)*[a-zA-Z$]\w*',name)

    def isContext(self,name):               # context name (1 or more contexts)
        return re.match(r'([a-zA-Z$]\w*`)+',name)     

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
            ctx = self.ctxsearch[:]         # default search: copy
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
                
    def configSym(self,par) :           # config symbol data, par is a list 
        s = self.symbol(par[0])             # par[0] is symbol name
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

    def symList(self):
        f = lambda e: e if type(e)==list else [e]
        s0 = [f(self.symtab[k]) for k in sorted(self.symtab) if self.isSymbol(k)]
        return [e for u in s0 for e in u]
        
    def show(self,q=0,ctx=None):
        if type(ctx) != list:           # symbol list for single context
            if type(ctx) == str:        # string converted into context symbol
                ctx = self.context(ctx)
            if not ctx:                 # default is current context
                ctx = self.curctx
            u = self.symList()
            s = ["Symbols in "+ctx.show()+" :"+format([e.ctx for e in u].count(ctx),'5d')]
            if q>=1:
                s += [e.show(2*q-2) for e in u if e.ctx == ctx]
            return s
        elif ctx == []:                 # default: full context list
            ctx = [self.ctxtab[k] for k in sorted(self.ctxtab.keys())]
        return [self.show(q,c) for c in ctx]

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
    def __init__(self,nam):             # new context: name
        self.name = nam                 # symbol name
    def show(self):                     # returns context name
        return self.name
 
class Symbol(object):
    def __init__(self,nam,ct,f=0):      # new symbol: name, context, flags
        self.name = nam                 # symbol name
        self.ctx  = ct                  # context symbol
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
        
    def evalcond(self,i) :
        if self.flg.bit(neall) :
            return False
        return i==0 or i==1 and not self.flg.bit(nev1) or i>1 and not self.flg.bit(nevr)
    
    def addrul(self,r) :                # add a rule r for symbol
        if self.flg.bit(prot) :
            print "Assign : symbol ",self.name," protected"
            return None
        if r[1].typ() == "Symbol":
            if r[1].val == self:        # own symbol assigned
                self.rule = r
                self.flg.on(rul)
        else :
            if not self.flg.bit(drul):  # no rules yet
                self.drules = [r]
                self.flg.on(drul)       
            else :                      # rules already
                self.drules.insert(0,r)
    
    def clrrul(self) :                   # clear all rules
        if not self.flg.bit(prot) :
            self.rule  = None
            self.drules= None
            self.flg.off(rul)
            self.flg.off(drul)
            
    def loadrul(self,lrul) :            # loading multiple rules onto symbol
        prot = self.flg.bit(prot)       # saves original bit
        for r in lrul:
            self.
        
        
 
    def show(self,t=None):
        if not t:                       # non formatted
            return self.name
        s = format(self.name,'10s')
        if t % 2 == 1 :
            s += "("+self.ctx.show()+")"
        t /= 2
        if t % 3 == 1:
            s += " Flags "+self.flg.binary()
        if  (t/3) % 2 and self.flg.bit(oper):
            s += " "+format(self.opt,'7s')+"("+format(self.pre,'2d')+") "+format(self.opr,'4s')
        if t % 3 == 2:
            s += " Flags: "+", ".join(self.flg.lis())    
        return s

# variables defined flags (1 bit power 2)

[lock,prot,rdprot,temp,stub,func,nev1,nevr,neall,necom,neseq,num,nnum1,nnumr,nnuma,const,lista,assoc,comm,idem,oper,rul,drul,urul,defv]\
     = [2**i for i in range(25)]

class Flag(object):
    names = []
    fmt = '025b'
    def __init__(self,f):
        if type(f) != int:
            f = self.number(f)  # convert flag name(s) into number before
        self.flag  = f
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
        return self.name.index(n)
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
      
        
 