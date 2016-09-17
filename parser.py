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
import symbol as sym

def parseExpr(tk,pr=0):
    if tk.typ()== "newline" :           # leading newline eliminated
        tk.popVal()
        print "parser found newline...."
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
        return None                     # nothing to parse: the end
    if tk.typ()== "newline" :           # newline breaks search of infix oper.
        return e
    return parseInfix(tk,e,pr)          # try parsing an infix expression
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
    return parseSymbTail(tk,e)          # try parsing symbol tail

def parseName(tk):
    if tk.typ() == "name" :             # parsing symbol name
        return expr.Symbol(tk.popVal())

def parseList(tk) :
    e = parseLimSeq(tk,'{','}')         # try parsing a list:{e1,e2,..}
    if e :
        e.prepend(expr.Symbol("List"))  # converting into expression List
        return e

def parseSymbTail(tk,h) :               # h is the head, so far
    e = parseLimSeq(tk,'[',']')         # try parsing argument list: [e1,e2,..]
    if e :                              # is compound expresion
        e.prepend(h)
        return parseSymbTail(tk,e)      # try parsing symbol tail (current exp)
    e = parseLimSeq(tk,'[[',']]')       # try parsing part list: [[n1,n2,...]]
    if e :
        e.prepend(h)
        e.prepend(expr.Symbol("Part"))
        return parseSymbTail(tk,e)      # try parsing symbol tail (current exp)
    return h                            # no tail: returning head (h)

def parseLimSeq(tk,left,right) :
    if tk.val()== left :                # comparing with left delimiter
        tk.popVal()                     # left delimiter is popped
        e = parseSeq(tk)                # parsing a sequence
        if e and tk.val()== right :     # comparing with right delimiter 
            tk.popVal()                 # right delimiter is popped
        else :                          # syntax error!
            print "Syntax error, parsing "+left+"..."
        return e                        # sequence returned
        
def parseSeq(tk):
    return parseSeqTail(tk,expr.Compound(parseExpr(tk)))

def parseSeqTail(tk,e):
    while tk.val()== ',' :              # delimiter comparison
        tk.popVal()                     # delimiter is popped
        f = parseExpr(tk)               # try parsing an expression
        if f :
            e.append(f)                 # item expression is appended
        else :
            print "Syntax error, parsing sequence, missing expression"
    return e 

def parseGroup(tk): 
    if tk.val()== '(' :                 # try parsing open parenthesis
        tk.popVal()                     # delimiter '(' is popped
        e = parseExpr(tk)               # parsing expression
        if e and tk.val()== ')' :       # parsing 
            tk.popVal()                 # delimiter ')' is popped
        else :                          # syntax error!
            print "Syntax error, parsing (..."
        return e
            
def parseInfix(tk,e,pr):                # e contains possible first expression
    op = getInfixPrior(tk,pr)           # next operator (if priority ≥ pr )
    while op :
        s = parseExpr(tk,sym.prior(op.val)+1)   # try parsing second expression
        if s :
            if e.head().val!=op.val or not op.isAssoc():
                f = e                           # e becomes first expression     
                e = expr.Compound(op)           # op head of compound expression
                e.append(f)                     # adding first expression  
            e.append(s)                         # adding second  expression
        else :
            print "Syntax error, missing expression afer: "+op.val              
        op = getInfixPrior(tk,pr)       # next operator (if priority ≥ pr )
    return e

def getInfixPrior(tk,pr):
    if tk.impliedProd() and sym.prior("*") >= pr:
        return expr.Symbol("*")         # getting product with empty token
    if tk.typ() == "infix" and sym.prior(tk.val()) >= pr:
        return expr.Symbol(tk.popVal()) # getting next operator

