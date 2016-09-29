# -*- coding: utf-8 -*-
"""
    Created on Fri Aug 19 18:56:45 2016
    
    @author: danilobassi
"""

"""
    SMARTS
    
    Parser Class

"""

class Parse(object):
    def __init__(self,s):
        self.sys = s                        # system instantiation: token, expr
        print "List :", self.sys.expre.list
        print "Null :", self.sys.expre.null
        
    def parse(self,par):
        if type(par) == str :               # string as parameter
            par = self.sys.token(par)
        exp = self.parseExpr(par)           # expression is parsed
        if exp :                            # verification
            return exp
        else:
            return self.sys.expre.null

    def parseExpr(self,tk,pr=0):
        if tk.typ()== "newline" :           # leading newline eliminated
            tk.popVal()
        while True:
            e = self.parseNumber(tk)        # try parsing a number
            if e :
                break
            e = self.parseString(tk)        # try parsing a string
            if e :
                break
            e = self.parseSymb(tk)          # try parsing a symbol expression
            if e :
                break
            e = self.parseGroup(tk)         # try parsing a group expression
            if e :
                break
            return None                     # nothing to parse: the end
        if tk.typ()== "newline" :           # newline breaks search of infix oper.
            return e
        return self.parseInfix(tk,e,pr)     # try parsing an infix expression
                                            # if no infix, e is returned
    def parseNumber(self,tk):
        if tk.typ() == "number" :           # parsing a number
            if '.' in tk.val() :            # test for float
                return self.sys.expre.Real(float(tk.popVal()))
            return self.sys.expre.Integer(int(tk.popVal()))
        
    def parseString(self,tk):
        if tk.typ() == "string" :           # parsing a string
            return self.sys.expre.String(tk.popVal())

    def parseSymb(self,tk):
        while True:
            e = self.parseName(tk)          # try parsing symbol name
            if e :
                break
            e = self.parseList(tk)          # try parsing a list
            if e :
                break
            return None        
        return self.parseSymbTail(tk,e)     # try parsing symbol tail

    def parseName(self,tk):
        if tk.typ() == "name" :             # parsing symbol name
            return self.sys.expre.Symbol(tk.popVal())

    def parseList(self,tk) :
        e = self.parseLimSeq(tk,'{','}')    # try parsing a list:{e1,e2,..}
        if e!=None :
            e.prepend(self.sys.expre.list)  # converting into expression List
            return e

    def parseSymbTail(self,tk,h) :          # h is the head, so far
        e = self.parseLimSeq(tk,'[',']')    # try parsing argument list: [e1,e2,..]
        if e != None :                      # is expresion sequence
            e.prepend(h)
            return self.parseSymbTail(tk,e) # try parsing symbol tail (current exp)
        e = self.parseLimSeq(tk,'[[',']]')  # try parsing part list: [[n1,n2,...]]
        if e != None :
            e.prepend(h)
            e.prepend(self.sys.expre.part)
            return self.parseSymbTail(tk,e) # try parsing symbol tail (current exp)
        return h                                # no tail: returning head (h)

    def parseLimSeq(self,tk,left,right) :
        if tk.val()== left :                # comparing with left delimiter
            tk.popVal()                     # left delimiter is popped
            e = self.parseSeq(tk)           # parsing a sequence
            if e!= None and tk.val()== right :     # comparing with right delimiter 
                tk.popVal()                 # right delimiter is popped
            else :                          # syntax error!
                print "Syntax error, parsing "+left+"..."
            return e                        # sequence returned
        
    def parseSeq(self,tk):
        e = self.parseExpr(tk)
        if e!=None :
            return self.parseSeqTail(tk,self.sys.expre.Sequence([e]))
        else :
            return self.sys.expre.Sequence([ ])

    def parseSeqTail(self,tk,e):
        while tk.val()== ',' :              # delimiter comparison
            tk.popVal()                     # delimiter is popped
            f = self.parseExpr(tk)          # try parsing an expression
            if f :
                e.append(f)                 # item expression is appended
            else :
                print "Syntax error, parsing sequence, missing expression"
        return e 

    def parseGroup(self,tk): 
        if tk.val()== '(' :                 # try parsing open parenthesis
            tk.popVal()                     # delimiter '(' is popped
            e = self.parseExpr(tk)          # parsing expression
            if e and tk.val()== ')' :       # parsing 
                tk.popVal()                 # delimiter ')' is popped
            else :                          # syntax error!
                print "Syntax error, parsing (..."
            return e
            
    def parseInfix(self,tk,e,pr):           # e contains possible first expression
        op = self.nextOp("Infix",tk,pr)     # next operator (if priority ≥ pr )
        while op :                              # try parsing second expression
            s = self.parseExpr(tk,self.sys.prior(op.val)+1) 
            if s :
                if e.head().val!=op.val or not self.sys.isAssoc(op.val):
                    f = e                       # e becomes first expression     
                    e = self.sys.expre.Sequence([op])# op head of expression sequence
                    e.append(f)                 # adding first expression  
                e.append(s)                     # adding second  expression
            else :
                print "Syntax error, missing expression afer: "+op.show()              
            op = self.nextOp("Infix",tk,pr)     # next operator (if priority ≥ pr )
        return e

    def nextOp(self,typ,tk,pr):
#        print "trying nextOp : first"
        if tk.impliedProd() and self.sys.prior("*") >= pr:
            return self.sys.expre.Symbol("*")   # getting product with empty token
        if self.sys.isOperator(tk.val(),typ) and self.sys.prior(tk.val()) >= pr:
            return self.sys.expre.Symbol(tk.popVal()) # getting next operator
