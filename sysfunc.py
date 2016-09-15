# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:56:51 2016

@author: danilobassi
"""

"""
    SMARTS
    
    System Function Definitions
    
"""

import tokenizer as tk
import parser    as ps
import expr



def ToExpr(st,h=None) :  # ToExpr coverts string into an expression
    tok = tk.Token(st)
    if h == 1 :                                 # Looking for one expression
        exp = ps.parseExpr(tok)
        if exp :
            return exp
        else :
            return expr.Symbol("Null")
    elif type(h) == str :                       # Looking for all expressions
        exp = expr.Compound(expr.Symbol(h))     # Compound expression head h
    else :
        exp = []                                # List of expressions
    while tok.size() :
        exp.append(ps.parseExpr(tok))
    return exp
    
def ReadStr(flname) :           # ReadStr reads file into a string    
    fl = open(flname)
    return fl.read()            # returns string read
    
def Read(flname,h=None):
    return ToExpr(ReadStr(flname),h)
    
def Eval(exp) :                 # Evaluation of expression
    return exp

    

    