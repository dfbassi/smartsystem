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

# Function that coverts string into an expression

def sysToExpr(st,h=None) :
    tok = tk.Token(st)
    if h == 1 :                                 # Looking for one expression
        return ps.parseExpr(tok)
    elif type(h) == str :                       # Looking for all expressions
        exp = expr.Compound(expr.Symbol(h))     # Compound expression head h
    else :
        exp = []                                # List of expressions
    while tok.size() :
        exp.append(ps.parseExpr(tok))
    return exp
    
def sysRead(fl) :
    pass

def 
    

    