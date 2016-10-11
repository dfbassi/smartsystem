# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:56:51 2016

@author: danilobassi
"""

"""
    SMARTS
    
    System Function Definitions
    
"""

expre = None                    # pointer to Expr object
stm   = None                    # pointer to System object

def ReadStr(flname) :           # ReadStr reads file into a string    
    fl = open(flname)
    s = fl.read()
    fl.close()
    return s                    # returns the string read
    
def ToExpr(e) :                 # ToExprNE converts a string into expression
    return stm.strToExpr(e.toBase())

def Assign(e) :                 # assign expression e: lhs=rhs
    h= e[1]
    if h.typ() == "Sequence":
        h = h.finalHead()
    print "h : ",h.show()
    if h.typ() != "Symbol":
        print "Cannot assign non symbol"
    elif h.val.isProtected():
        print "Cannot assign protected symbol: ",h.val.show()
    else:                       # add rul to symbol
        e.replpart(expre.rulaft,0,0)
        h.val.addrul(e)
    return expre.null
        
def AssignRes(e) :              # assign expression e: lhs=rhs
    Assign(e)
    return e[2]
           
def Clear(e) :                  # clear a symbol
    if e.typ() == "Symbol" and not e.val.isProtected():
        e.val.clrrul()
    return expre.null
       
def Evaluate(e) :
    e.evalExpr()

        

        
    