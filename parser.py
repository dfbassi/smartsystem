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
    while True:
        e = parsePrim(tk)               # try parsing a primitive type
        if e :
            break
        e = parseSymb(tk)               # try parsing a symbol type
        if e :
            break
        e = parseGroup(tk)              # try parsing a group type
        if e :
            break
        return None
    return parseInfix(e,tk)             # try parsing an infix expression
                                        # if no infix, e is returned
  
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

def parseGroup(tk): 
    if tk.val()== '(' :                 # try parsing an open parenthesis
        tk.popVal()                     # delimiter '(' is popped
        e = parseExpr(tk)               # parsing expression
        if e and tk.val()== ')' :       # parsing 
            tk.popVal()                 # delimiter ')' is popped
            return e
 
def parseInfix(f,tk):                   # f contains first expression
    if tk.typ() != "oper" :             # no infix
        return f
    e = expr.Symbol(tk.popVal())        # Infix: parsed as a Symbol
    g = parseExpr(tk)                   # try parsing next expression
    if g :
        if g.isCompound() and g.head().val == e.val :
            g.insert(f,1)               # inserting first expression
            return g
        e = expr.Compound(e)            # put as head compound expression
        e.append(f)                     # adding first expression
        e.append(g)                     # adding second  expression
        return e           
         
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



