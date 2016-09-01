# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 17:15:30 2016

@author: danilobassi
"""

metachars = "$.?*+[]()|"
operators = "?+*|"

def str2expr(st,exp) :
    while len(st):
        tk = st.pop(0)
        if tk == '\\' :                 # escape char.
            print "escape..."+st[0]
            exp.append(st.pop(0))
            continue
        if tk == "(" or tk == "[" :     # starts group
            exp1 = []
            str2expr(st,exp1)
            exp.append(exp1)
            continue
        if tk == ")":
            break
        if tk == "]": 
            exp.insert(0,'|')
            break
        if tk in operators:
            if type(exp[-1])!=list:
                exp[-1] = [exp[-1]]
            exp[-1].insert(0,tk)
            continue
        exp.append(tk)
        
def regex(st):
    exp = []
    str2expr(list(st),exp)
    return exp
        
        
            