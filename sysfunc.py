# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:56:51 2016

@author: danilobassi
"""

"""
    SMARTS
    
    System Function Definitions
    
"""



def ReadStr(flname) :           # ReadStr reads file into a string    
    fl = open(flname)
    s = fl.read()
    fl.close()
    return s                    # returns string read
    
def Eval(exp) :                 # Evaluation of expression
    return exp

    

    