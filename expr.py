# -*- coding: utf-8 -*-
"""
    Created on Thu Aug 18 22:13:00 2016
    
    @author: danilobassi
"""

"""
    SMARTS
    
    Symbolic Expression Class and Subclasses
    
"""
import parseregex as pre
import tokenizer
import re

sys   = None
relis = pre.regex(r"$\[($(,$)*)?\]")    # regular expression list   

[lock,prot,rdprot,temp,stub,func,nev1,nevr,neall,necom,neseq,num,nnum1,nnumr,nnuma,const,lista,assoc,comm,idem,oper,rul,urul,defv]\
     = [2**i for i in range(24)]

class String(str):
    def show(self,rl=None):
        return str(self)
        
class System(object):
    def __init__(self,exp):
        self.expre = exp
        self.token = tokenizer.Token
    def symbol(self,name):              # name (as str) converted into string class
        return String(name)
    def isOperator(v,typ=None):
        print "isOperator : ", v
        return False
   
class Expr(object):
    def __init__(self,s=None,rem=None):
        global sys
        global relis
        if s:
            sys = s
        else :
            sys = System(self)
        print "sys : ",sys
        self.list = self.Symbol('List')
        self.null = self.Symbol('Null')
        self.true = self.Symbol('True')
        self.false= self.Symbol('False')
        self.part = self.Symbol('Part')
        self.rul   = self.Symbol('->')
        self.rulaft= self.Symbol(':>')
        self.asgn  = self.Symbol('=')
        self.asgaft= self.Symbol(':=')
        if rem :                            # optional definition of a list output format
            relis = pre.regex(rem)
        self.select={str:self.String,int:self.Integer,float:self.Real,bool:self.boolean}
    def toExpr(self,x,h=None):              # converts to expression
        if not x:
            return self.null
        if re.match(".*expr\..*",str(type(x))):
            return x
        if type(x) !=list:
            return self.select[type(x)](x)
        if not h:
            h = self.list
        return self.Sequence([h]+[self.toExpr(i) for i in x])
    def boolean(self,x):
        if x:
            return sys.true
        return sys.false
                              
    class Expression(object):           # parent class for expressions
        def __init__(self,value):
            self.val = value
        def typ(self):                  # gives name of class (or type) expression
            return "Expression"
        def value(self):                # gives internal value (no conversion)
            return self.val
    # Functions for SMARTS
    # Information & presentation functions
        def show(self,rl=None):         # converts expression to string
            return self.val
        def isAtom(self):
            return True
        def length(self):               # gives length of expression (default 0)
            return 0
        def dim(self):                  # givess length of expression (default [])
            return []
        def depth(self):                # gives depth 
            return 1
    # Structural functions
        def head(self):                 # gives the head of expression as expr
            return Expr.Symbol(self.typ())
        def part(self,p):
            if p==0:
                return self.head()
        def copy(self,n):               # returns itself for atom expressions
            return self
        def replpart(self,e,p):         # replaces pth part (only sequences)          
            pass
        def replace(self,rul,c):        # rul r[0] -> r[1] replaces matching lhs
            for r in rul:
                if self.match(r[1]):    # first match returns a copy of rhs of rule
                    return r[2].copy(c)
            return self
        def replev(self,rul,n,m,c):     # replev uses replace for atom expressions
            return self.replace(rul,c)
        def match(self,e):
            print "match item :", self.show()," ",e.show()
            return self.val==e.val      
        def toBase(self,hd=None) :      # converts expressions into base list & types
            return self.value()
        def evalExpr(self):             # evaluation is for symbols
            return self
        def treewid(self):
            return (self.show(),len(self.show()))
        def tree(self):
            return printTree(self.treewid())
         
    class Integer(Expression):
        def typ(self):
            return "Integer"
        def show(self,rl=None):
            return str(self.val)
  
    class Real(Expression):       
        def typ(self):
            return "Real"
        def show(self,rl=None):
            return str(self.val)

    class String(Expression):
        def typ(self):
            return "String"
        def show(self,rl=None):
            return '"'+self.val+'"'         # string enclosed on quotes

    class Symbol(Expression):
        def __init__(self,value):
            self.val = sys.symbol(value)
        def typ(self):
            return "Symbol"
        def toBase(self,hd=None) :          # converts expressions into base types
            return self.val.show()          # symbol returns name (as str)
        def show(self,rl=None):
            return self.val.show()
        def finalHead(self):                #
            return self.head()
        def evalExpr(self):
            if  self.val.flg.bit(rul):      # has rules defined
                return self.replace(self.val.rules)
            else:
                return self
      
    class Native(Expression):
        def __init__(self,value,argtype=None):
            self.val = value
            self.argt = argtype
        def typ(self):
            return "Native"
        def show(self,rl=None):
            return str(self.val)
        def evalExpr(self,e):
            if not self.argt:               # expression function (non typed)
                return self.val(e)         
            if e.length() == 1:             # typed function 1 argument
                res = self.val(e[1].toBase())
            elif e.length() == 2:           # typed function 2 arguments
                res = self.val(e[1].toBase(),e[2].toBase())
            else :                          # typed function 3 or more arguments
                res = reduce(self.val,[ei.toBase() for ei in e[1:]])
            return sys.expre.toExpr(res)

    class Sequence(list):
        def typ(self):
            return "Sequence"
        def value(self) :
            return [e.value() for e in self]
    # Functions for SMARTS
    # Information & presentation functions
        def show(self,rl=relis):        # converts into string
            return showList(rl,[e.show(rl) for e in self])
        def toBase(self,hd='List') :    # converts expressions into base list & types
            v = [e.toBase(hd) for e in self]
            if v[0] == hd:
                v.pop(0)
            return v
        def isAtom(self):
            return False
        def depth(self):
            return max([e.depth() for e in  self])+1
        def length(self):               # returns length of expression (default 0)
            return len(self)-1
    # Structural functions
        def head(self):                 # head of expression: v[0]
            return self[0]
        def finalHead(self):            # searches for symbol head in compound heads
            h = self[0]
            while h.typ()=="Sequence":
                h = h[0]
            return h
        def copy(self,n=0):             # copy, structural up to level n
            if n:
                return Expr.Sequence([e.copy(n-1) for e in self])
            else:
                return self
        def dim(self):
            if self.length() == 0:
                return [0]
            d0 = [self.length()]
            d = [e.dim() for e in self[1:]]
            if d.count(d[0]) == d0[0]:
                return d0+d[0]
            return d0          
        def part(self,p):
            if type(p)!=list:
                if 0 <=p<= self.length():
                    return self[p]
                else:
                    return None
            if len(p)==1:
                return self.part(p[0])
            return self.part(p[0]).part(p[1:])
        def replpart(self,e,p,c=-1):        # replaces pth part with copy of e             
            if type(p)==list:
                if len(p)>1 :
                    self.replpart(self.part(e,p[:-1]),p[-1],c)
                    return None
                else:
                    p=p[0]
            if 0 <= p <= self.length():
                self[p]=e.copy(c)       #copy up to n depth
        def replev(self,r,n,m=1,c=-1):      # replaces using rule list r at level n
            if n==0 :
                return self.replace(r,c)
            if not self.isAtom():            
                if m==1:
                    self = [self[0]]+[e.replev(r,n-1,m,c) for e in self[1:]]
                else:
                    self = [e.replev(r,n-1,m,c) for e in self]
            return self
        def replace(self,rul,c=-1):
            for r in rul:
                if self.match(r[1]):        # first match returns a copy of rhs of rule
                    return r[2].copy(c)     # changes full expression
            for i in range(len(self)):
                self[i] = self[i].replace(rul,c)
            return self
        def match(self,e) :
            if self == e:                   # identical
                return True
            if e.isAtom() or self.length() != e.length():  
                return False                # length must be the same
            for i in range(len(self)):
                if not self[i].match(e.val[i]):
                    return False
            return True
        def evalExpr(self):
            h = self.finalHead()            # final head is atom
            if h.typ() == "Native":         # using eval for native functions
                return h.evalExpr(self)
            if h.typ() != "Symbol":
                return self                 # nothing to do 
            for i in range(len(self)):
                if h.val.evalcond(i):
                    self[i] = self[i].evalExpr()
            h = self.finalHead()
            if  h.val.flg.bit(rul):         # has a rule
                return self.replace(self.val.rules)
            else:
                return self
               
        def pop(self,pos=-1):
            self.pop(pos)
        def prepend(self,value):
            self.insert(0,value)
        def treewid(self):
            s = [e.treewid() for e in self]
            w = sum(map(lambda x:x[1],s[1:])) + len(s)-2
            if w < s[0][1] and type(s[0][0])== str:
                s.append( (" "*(s[0][1]-w-1),s[0][1]-w-1) )
                w = s[0][1]
            return (s,w)          
        def tree(self):
            return printTree(self.treewid())
            


# Functions definitions for show and tree

def showList(relis,shwlis) :
            if relis == [] :                # nothing to do
                return None
            if type(shwlis[0]) == str:
                shwlis.insert(0,1)
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
                    res2 = showItem(item,shwlis)
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
                    
def showItem(item,shwlis):
            if type(item) == list :         
                return showList(item,shwlis)
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
                s = level(lis[0], lev)+" " # head values to the left
                if lev == 0:                    # this level is head
                    return s + " "*tr[1]        # left side and padding to the right
            else:                           # head is symbol
                s = ""      
                if lev == 0:                   # this level is head
                    return lis[0][0]+" "*(tr[1]-len(lis[0][0]))# head + padding
                                        # this level is below head
            return s + " ".join([level(x,lev-1) for x in lis[1:]])
            
def line(tr,lev):
            if type(tr[0]) == str:      # single node: leaf 
                if lev == 0:                    # current level
                    return '_'*tr[1]            # lines here
                return ' '*tr[1]                # this is below leaf: space
            lis = tr[0]                 # list of nodes
            if type(lis[0][0]) != str:      # head is composite
                s = line(lis[0],lev)+" "   # head values to the left
                if lev == 0:
                    return s[:-1]+"_"*(tr[1]+1) # spaces to the right
            else:                           # head is symbol
                s = ""      
                if lev == 0:                    # this level is head
                    return '_'*tr[1]            # lines here
            t = [line(x,lev-1) for x in lis[1:]] 
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
    
def printTree(tre):
    print level(tre,0)
    for i in range(1, depth(tre)):
        print line(tre,i)
        print level(tre,i)        

