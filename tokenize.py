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
    name   = r'[a-zA-Z$][\w-]*'                 # Regular expression for differen tokens
    strg   = r'\"[^\"]*\"'
    number = r'\d+\.?\d*'
    oper   = r'[-^+*/!]|:=|\|{1,2}|&{1,2}|<=?|>=?|={1,3}'
    delim  = r'[(){},;]|\[{1,2}|\]{1,2}'
    tokregex = name +"|"+strg+"|"+number+"|"+delim+"|" + oper
    
    def __init__(self,input):                   # input is string to be parsed
        self.q = Queue()                        # a queue is used
        self.tokens = re.findall(self.tokregex,input)
        for t in self.tokens:
            if re.match('[a-zA-Z$]', t[0]):     # Id name starts with letter
                self.q.enqueue((t,'name'))
            elif re.match(r'\d', t[0]):         # Number starts with digit
                self.q.enqueue((t,'number'))
            elif re.match(r'\"', t[0]):         # String starts with "
                self.q.enqueue((t[1:-1],'string'))
            elif re.match(r'[(){},;\[\]]', t[0]):
                self.q.enqueue((t,'delim'))
            else :
                self.q.enqueue((t,'oper'))      # Rest of tokens are operators

def val(self):                      # Actual token (top)
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

