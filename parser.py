# -*- coding: utf-8 -*-
"""
    Created on Fri Aug 19 18:56:45 2016
    
    @author: danilobassi
"""

"""
    SMARTS
    Symbolic Expression Classes

"""
import expr

def parseExpr(tk):
    e = parsePrim(tk)           # Try parsing a primitive type
    if e :
        return e
    e = parseSymb(tk)           # Try parsing a primitive type
    if e :
        return e
    if tk.val()== '(' :         # Parsing a group expression
        tk.popVal()             # Delimiter is popped
        e = parseExpr(tk)
        tk.popVal()             # Delimiter is popped: ')'
        return e

def parsePrim(tk):
    if tk.typ() == "number" :
        return expr.Number(tk.popVal())
    if tk.typ() == "string" :
        return expr.String(tk.popVal())

def parseSymb(tk):
    h = parseSymbFirst(tk)
    if h :
        return parseSymbTail(h,tk)

def parseSymbFirst(tk):
    e = parseName(tk)
    if e :
        return e
    return parseList(tk)        # List

def parseName(tk):
    if tk.typ() == "name" :
        return expr.Symbol(tk.popVal())

def parseSymbTail(h,tk) :   # h is the head, so far
    e = parseLimSeq('[',tk) # Bracket for argument list
    if e :                  # compound expresion
        e.prepend(h)
        return parseSymbTail(e,tk)
    e = parseLimSeq('[[',tk) # Double Bracket for part list
    if e :
        e.prepend(h)
        e.prepend(expr.Symbol("Part"))
        return parseSymbTail(e,tk)
    return h                # SymbTail is nil

def parseList(tk) :
    e = parseLimSeq('{',tk)
    if e :
        e.prepend(expr.Symbol("List"))
        return e

def parseLimSeq(dl,tk) :
    if tk.val()== dl :      # Open delimiter comparison
        tk.popVal()         # Delimiter is popped
        e = parseSeq(tk)
        tk.popVal()
        return e

def parseSeq(tk):
    return parseSeqTail(expr.Compound(parseExpr(tk)),tk)

def parseSeqTail(e,tk):
    while tk.val()== ',' :  # Delimiter comparison
        tk.popVal()         # Delimiter is popped
        e.append(parseExpr(tk))
    return e



