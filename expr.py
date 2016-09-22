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
    print "Expr initialization :", s
    e = Expr()
    if s:                               # systen class defined
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
        def value(self):                # gives value in native type (no conversion)
            return self.val
        def show(self):                 # gives value contained in a string
            return self.val
        def head(self):
            return Expr.Symbol(self.typ())
        def tree(self):
            return (self.show(),len(self.show()))
        def depth(self,tre):
            if type(tre[0]) == str :
                return 1
            return max(map(self.depth,tre[0]))+1
        def printTree(self):
            tr = self.tree()
            print self.level(tr,0)
            for i in range(1, self.depth(tr)):
                print self.line(tr,i)
                print self.level(tr,i)        
        def level(self,tr,lev):
            if type(tr[0]) == str:      # single node: leaf 
                if lev == 0:                    # current level
                    return tr[0]                # value of the node
                return " "*tr[1]                # this is below leaf: empty                              
            lis = tr[0]                 # list of nodes: interior
            if type(lis[0][0]) != str:      # head is composite
                s = self.level(lis[0], lev)+" " # head values to the left
                if lev == 0:                    # this level is head
                    return s + " "*tr[1]        # left side and padding to the right
            else:                           # head is symbol
                s = ""      
                if lev == 0:                   # this level is head
                    return lis[0][0]+" "*(tr[1]-len(lis[0][0]))# head + padding
                                        # this level is below head
            return s + " ".join([self.level(x,lev-1) for x in lis[1:]])      
        def line(self,tr,lev):
            if type(tr[0]) == str:      # single node: leaf 
                if lev == 0:                    # current level
                    return '_'*tr[1]            # lines here
                return ' '*tr[1]                # this is below leaf: space
            lis = tr[0]                 # list of nodes
            if type(lis[0][0]) != str:      # head is composite
                s = self.line(lis[0],lev)+" "   # head values to the left
                if lev == 0:
                    return s[:-1]+"_"*(tr[1]+1) # spaces to the right
            else:                           # head is symbol
                s = ""      
                if lev == 0:                    # this level is head
                    return '_'*tr[1]            # lines here
            t = [self.line(x,lev-1) for x in lis[1:]] 
            if t[0][0] == '_':                  # check for lines
                if t[-1] == "":
                    t = t[:-1]
                    t[-1] = t[-1][:-1]+" "
                else :
                    t[-1]=' '*(len(t[-1])-1)    # replaces last by spaces
                return s+'|'+'_'.join(t)
            return s + " ".join(t)
         
    class Integer(Expression):
        def __init__(self,value):
            self.val = int(value)
        def typ(self):
            return "Integer"
        def show(self):
            return str(self.val)
  
    class Real(Expression):
        def __init__(self,value):
            self.val = float(value)
        def typ(self):
            return "Real"
        def show(self):
            return str(self.val)

    class String(Expression):
        def typ(self):
            return "String"
        def show(self):
            return '"'+self.val+'"'     # explicit display of braces for string

    class Symbol(Expression):
        sys = None
        def __init__(self,value):
            if self.sys :
                self.val = self.sys.symbol(value)
            else :
                self.val = value
        def show(self):
            if self.sys :
                return self.val.show()
            else :
                return self.val
        def typ(self):
            return "Symbol"

    class Sequence(Expression):
        relis = pre.regex(r"$\[($(,$)*)?\]")    # regular expression list   
        def __init__(self,value):
            if value:
                self.val = [value]
            else:
                self.val = []
        def typ(self):
            return "Sequence"
        def value(self) :
            return [e.value() for e in self.val]
        def prepend(self,value):
            self.val.insert(0,value)
        def pop(self,pos=-1):
            self.val.pop(pos)        
        def head(self):
            return self.val[0]
        def show(self):
            return self.showList(self.relis,[e.show() for e in self.val])
        def tree(self):
            s = [e.tree() for e in self.val]
            w = sum(map(lambda x:x[1],s[1:])) + len(s)-2
            if w < s[0][1] and type(s[0][0])== str:
                s.append( (" "*(s[0][1]-w-1),s[0][1]-w-1) )
                w = s[0][1]
            return (s,w)          
        def showList(self,relis,shwlis) :
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
                    res2 = self.showItem(item,shwlis)
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
        def showItem(self,item,shwlis):
            if type(item) == list :         
                return self.showList(item,shwlis)
            if item == '$' :                # this represents full expression
                if shwlis[0] < len(shwlis) :
                    shwlis[0] += 1
                    return shwlis[shwlis[0]-1]
            else :
                return item                 # item copied to output

