# -*- coding: utf-8 -*-
"""
    Created on Wed Aug 17 17:27:16 2016
    
    @author: danilobassi
"""
"""
    SMARTS
    Tokenizer
"""

import re

class Queue:                            # A queue is used to process tokens
    def __init__(self):
        self.items = []                 # List as base structure
    def isEmpty(self):
        return self.items == []
    def enqueue(self,item):
        self.items.insert(0,item)       # Elements enqueued at initial position of list
    def dequeue(self):
        return self.items.pop()         # Elements dequeued at final position of list
    def size(self):
        return len(self.items)
    def top(self):
        return self.items[-1]

class Token(object):
    name   = r'[a-zA-Z$][\w]*'                 # Regular expression for different tokens
    strg   = r'\"[^\"]*\"'
    number = r'\d+\.?\d*'
    oper   = r'[-^+*/!;]|:=|\|{1,2}|&{1,2}|<=?|>=?|={1,3}'
    delim  = r'[(){},]|\[{1,2}|\]{1,2}|\n(?!\Z|\n)'
    alltok = name +"|"+strg+"|"+number+"|"+delim+"|" + oper
    prefix = ["-","!"]
    infix  = [";","|", "=", ":=", "+=", "-=", "*=", "/=","~~","||","&&", \
              "==","===","!=","<","<=",">",">=","+","-","*", "/",".","^","<>"]
    postfix= ["!","&"]
    ledelim= ["(","{",r"[",r"[["]
    ridelim= [")","}",r"]",r"]]"]
    opers  = postfix+infix+prefix
    nonprod= opers+ridelim+[',','\n']
     
    def __init__(self,input):                   # input is string to be parsed
        self.q = Queue()                        # a queue is used
        self.tokens = re.findall(self.alltok,input)
        for t in self.tokens:
            if re.match('[a-zA-Z$]', t[0]):     # Id name starts with letter
                self.q.enqueue((t,'name'))
            elif re.match(r'\d', t[0]):         # Number starts with digit
                self.q.enqueue((t,'number'))
            elif re.match(r'\"', t[0]):         # String starts with "
                self.q.enqueue((t[1:-1],'string'))
            elif re.match(r'[(){},\[\]]', t[0]):# delimiter
                self.q.enqueue((t,'delim'))
            elif re.match(r'\n', t[0]):         # new line
                self.q.enqueue((t,'newline'))            
            elif t in self.infix:               # infix operator
                self.q.enqueue((t,'infix'))
            elif t in self.pefix:               # prefix operator
                self.q.enqueue((t,'prefix'))
            elif t in self.postfix:             # postfix operator
                self.q.enqueue((t,'postfix'))
    def val(self):                      # Actual token (top of queue)
        if not self.q.isEmpty() :
            return self.q.top()[0]
    def typ(self):                      # Actual token type
        if not self.q.isEmpty() :
            return self.q.top()[1]
    def popVal(self):                   # Top token is popped and given
        if not self.q.isEmpty() :
            return self.q.dequeue()[0] 
    def size(self):
        return self.q.size()
    def impliedProd(self):
        return not self.q.isEmpty() and self.val() not in self.nonprod
