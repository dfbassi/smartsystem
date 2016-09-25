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

def exprInit(s=None,rem=None) :         # Initialization of class parameters
    e = Expr()
    if s:                               # systen class defined (for symbol)
        e.Symbol.sys = s
    if rem :                            # optional definition of a list output format
        e.Sequence.relis = pre.regex(rem)
    return e
    
class Expr(object):

    class Expression(object):           # parent class for expressions
        def __init__(self,value):
            self.val = value
        def typ(self):                  # gives name of class (or type) expression
            return "Expression"
        def value(self):                # gives internal value (no conversion)
            return self.val
    # Functions for SMARTS
        def show(self):                 # converts expression to string
            return self.val
        def head(self):                 # gives the head of expression as expr
            return Expr.Symbol(self.typ())
        def isAtom(self):
            return True
        def copy(self):                 # returns a deep copy of expression
            return Expr.Expression(self.value())
        def length(self):               # returns length of expression (default 0)
            return 0
        def dim(self):
            return []
        def replpart(self,e,p):         # replaces pth part (only sequences)          
            pass
        def tree(self):
            return (self.show(),len(self.show()))
        def printTree(self):
            tr = self.tree()
            print level(tr,0)
            for i in range(1, depth(tr)):
                print line(tr,i)
                print level(tr,i)        
         
    class Integer(Expression):
        def typ(self):
            return "Integer"
        def show(self):
            return str(self.val)
        def copy(self):
            return Expr.Integer(self.val)
  
    class Real(Expression):       
        def typ(self):
            return "Real"
        def show(self):
            return str(self.val)
        def copy(self):
            return Expr.Real(self.val)

    class String(Expression):
        def typ(self):
            return "String"
        def show(self):
            return '"'+self.val+'"'     # explicit display of braces for string
        def copy(self):
            return Expr.String(self.val)

    class Symbol(Expression):
        sys = None
        def __init__(self,value):
            if type(value) == str and self.sys :
                self.val = self.sys.symbol(value)
            else :
                self.val = value
        def typ(self):
            return "Symbol"
        def show(self):
            if self.sys :
                return self.val.show()
            else :
                return self.val
        def copy(self):
            return Expr.Symbol(self.val)

    class Sequence(Expression):
        relis = pre.regex(r"$\[($(,$)*)?\]")    # regular expression list   
        def __init__(self,value):
            if type(value) != list:
                self.val = [value]
            else:
                self.val = value
        def typ(self):
            return "Sequence"
        def value(self) :
            return [e.value() for e in self.val]
    # Functions for SMARTS
        def show(self):
            return showList(self.relis,[e.show() for e in self.val])
        def head(self):                 # expression
            return self.val[0]
        def isAtom(self):
            return False
        def copy(self):
            return Expr.Sequence([e.copy() for e in self.val])      
        def length(self):               # returns length of expression (default 0)
            return len(self.val)-1
        def dim(self):
            if self.length() == 0:
                return [0]
            d0 = [self.length()]
            d = [e.dim() for e in self.val[1:]]
            if d.count(d[0]) == d0[0]:
                return d0+d[0]
            return d          
        def part(self,p):
            if type(p)==list:
                p1=p[1:]
                p =p[0]
            else:
                p1 = []               
            if 0 <=p<= self.length():
                if not p1:
                    return self.val[p]
                else: 
                    return self.part(self,p1)            
        def replpart(self,e,p):         # replaces pth part with copy of e             
            if type(p)==list:
                if len(p)>1 :
                    self.replpart(self.part(e,p[:-1]),p[-1])
                    return None
                else:
                    p=[0]
            if 0 <=p<= self.length():
                self.val[p]=e.copy()
        def append(self,value):
            self.val.append(value)
        def prepend(self,value):
            self.val.insert(0,value)
        def pop(self,pos=-1):
            self.val.pop(pos)        
        def tree(self):
            s = [e.tree() for e in self.val]
            w = sum(map(lambda x:x[1],s[1:])) + len(s)-2
            if w < s[0][1] and type(s[0][0])== str:
                s.append( (" "*(s[0][1]-w-1),s[0][1]-w-1) )
                w = s[0][1]
            return (s,w)          

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
