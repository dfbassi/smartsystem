# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:56:51 2016

@author: danilobassi
"""

"""
    SMARTS
    
    System Function Definitions
    
"""



def ReadStr(flname) :           # ReadStr reads file into a string    
    fl = open(flname)
    s = fl.read()
    fl.close()
    return s                    # returns string read
    
def Assign(e) :                 # assign expression e: lhs=rhs
    h= e[1]
    if h.typ() == "Sequence":
        h = h.finalHead()
    if h.typ() != "Symbol":
        print "Cannot assign non symbol"
    else:
        h.val.addrul(e)         # add rul to symbol
        
def AssignRes(e) :              # assign expression e: lhs=rhs
    Assign(e)
    return e[2]
           
def Clear(e) :                  # clear a symbol
    if e.typ() == "Symbol":
        e.val.clrrul()
        
def Evaluate(e) :
    e.evalExpr()

        

        
    