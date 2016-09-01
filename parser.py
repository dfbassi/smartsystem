# -*- coding: utf-8 -*-
"""
    Created on Fri Aug 19 18:56:45 2016
    
    @author: danilobassi
"""

"""
    SMARTS
    
    Parser Functions Definition

"""
import expr

def parseExpr(tk):
    e = parsePrim(tk)                   # try parsing a primitive type
    if e :
        return e
    e = parseSymb(tk)                   # try parsing a symbol type
    if e :
        return e
    if tk.val()== '(' :                 # try parsing a group expression
        tk.popVal()                     # Delimiter is popped
        e = parseExpr(tk)               # Parsing expression
        tk.popVal()                     # Delimiter is popped: ')'
        return e

def parsePrim(tk):
    if tk.typ() == "number" :           # try parsing a number
        return expr.Number(tk.popVal())
    if tk.typ() == "string" :           # try parsing a string
        return expr.String(tk.popVal())

def parseSymb(tk):
    h = parseSymbFirst(tk)              # try parsing first symbol (head)
    if h :
        return parseSymbTail(h,tk)      # try parsing symbol tail

def parseSymbFirst(tk):
    e = parseName(tk)                   # try parsing symbol name
    if e :
        return e
    return parseList(tk)                # try parsing a list

def parseName(tk):
    if tk.typ() == "name" :             # parsing symbol name
        return expr.Symbol(tk.popVal())

def parseSymbTail(h,tk) :               # h is the head, so far
    e = parseLimSeq('[',tk)             # try parsing argument list (starting [)
    if e :                              # is compound expresion
        e.prepend(h)
        return parseSymbTail(e,tk)
    e = parseLimSeq('[[',tk)            # try parsing argument list (starting [[)
    if e :
        e.prepend(h)
        e.prepend(expr.Symbol("Part"))
        return parseSymbTail(e,tk)
    return h                            # symbol tail nil: returning head (h)

def parseList(tk) :
    e = parseLimSeq('{',tk)             # try parsing a list (starting {)
    if e :
        e.prepend(expr.Symbol("List"))  # converting into expression List
        return e

def parseLimSeq(dl,tk) :
    if tk.val()== dl :                  # comparing with specified delimiter
        tk.popVal()                     # initial delimiter is popped
        e = parseSeq(tk)                # parsing a sequence
        tk.popVal()                     # final delimiter is popped
        return e

def parseSeq(tk):
    return parseSeqTail(expr.Compound(parseExpr(tk)),tk)

def parseSeqTail(e,tk):
    while tk.val()== ',' :              # delimiter comparison
        tk.popVal()                     # delimiter is popped
        e.append(parseExpr(tk))         # item expression is appended
    return e



