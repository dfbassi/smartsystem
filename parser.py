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
        e = parseNumber(tk)             # try parsing a number
        if e :
            break
        e = parseString(tk)             # try parsing a string
        if e :
            break
        e = parseSymb(tk)               # try parsing a symbol expression
        if e :
            break
        e = parseGroup(tk)              # try parsing a group expression
        if e :
            break
        return None
    return parseInfix(e,tk)             # try parsing an infix expression
                                        # if no infix, e is returned

def parseNumber(tk):
    if tk.typ() == "number" :           # parsing a number
        if '.' in tk.val() :            # test for float
            return expr.Real(tk.popVal())
        return expr.Integer(tk.popVal())
        
def parseString(tk):
    if tk.typ() == "string" :           # parsing a string
        return expr.String(tk.popVal())

def parseSymb(tk):
    while True:
        e = parseName(tk)               # try parsing symbol name
        if e :
            break
        e = parseList(tk)               # try parsing a list
        if e :
            break
        return None        
    return parseSymbTail(e,tk)          # try parsing symbol tail

def parseName(tk):
    if tk.typ() == "name" :             # parsing symbol name
        return expr.Symbol(tk.popVal())

def parseList(tk) :
    e = parseLimSeq('{','}',tk)         # try parsing a list:{e1,e2,..}
    if e :
        e.prepend(expr.Symbol("List"))  # converting into expression List
        return e

def parseSymbTail(h,tk) :               # h is the head, so far
    e = parseLimSeq('[',']',tk)         # try parsing argument list: [e1,e2,..]
    if e :                              # is compound expresion
        e.prepend(h)
        return parseSymbTail(e,tk)      # try parsing symbol tail (current exp)
    e = parseLimSeq('[[',']]',tk)       # try parsing part list: [[n1,n2,...]]
    if e :
        e.prepend(h)
        e.prepend(expr.Symbol("Part"))
        return parseSymbTail(e,tk)      # try parsing symbol tail (current exp)
    return h                            # no tail: returning head (h)

def parseLimSeq(left,right,tk) :
    if tk.val()== left :                # comparing with left delimiter
        tk.popVal()                     # left delimiter is popped
        e = parseSeq(tk)                # parsing a sequence
        if e and tk.val()== right :     # comparing with right delimiter 
            tk.popVal()                 # right delimiter is popped
        else :                          # syntax error!
            print "Syntax error, parsing "+left+"..."
        return e                        # sequence returned
        
def parseSeq(tk):
    return parseSeqTail(expr.Compound(parseExpr(tk)),tk)

def parseSeqTail(e,tk):
    while tk.val()== ',' :              # delimiter comparison
        tk.popVal()                     # delimiter is popped
        f = parseExpr(tk)               # try parsing an expression
        if f :
            e.append(f)                 # item expression is appended
        else :
            print "Syntax error, parsing sequience, missing expression"
    return e 

def parseGroup(tk): 
    if tk.val()== '(' :                 # try parsing an open parenthesis
        tk.popVal()                     # delimiter '(' is popped
        e = parseExpr(tk)               # parsing expression
        if e and tk.val()== ')' :       # parsing 
            tk.popVal()                 # delimiter ')' is popped
        else :                          # syntax error!
            print "Syntax error, parsing (..."
        return e
            
def parseInfix(f,tk):                   # f contains first expression
    if tk.typ() != "infix" :            # no infix
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
    else :
        print "Syntax error, missing expression afer: "+e.val         
    return f
        



