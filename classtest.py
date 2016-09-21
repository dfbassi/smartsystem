# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:50:47 2016

@author: danilobassi
"""

class A(object):
    def __init__(self,v):
        print "initial A", v
        self.value = v
        
class B(list):
    def __init__(self,v):
        print "initial B:", v
        self.value = [v]
    def lis(self):
        return self.value