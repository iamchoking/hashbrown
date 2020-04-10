from math import *

class FunctionError(Exception):
    pass

class Function:
    def __init__(self,f,var,name = 'Function'):
        self.name = name
        self.f = f
        self.var = int(var)
    
    def f(self,*x): # f usually consists of t,x1,x2,....
        if len(x) != self.var:
            raise FunctionError('\n\nInvalid number of variables for %s: %d required, %d entered'%(self.name,self.var,len(x)))
        
        return self.f(*x)
    
    def minus(self,name = None):
        if name != None:
            Function(lambda *x: -self.f(*x),self.var,name = name)            
        return Function(lambda *x: -self.f(*x),self.var,name = self.name)

def invSign(f): #f is assumed to be a tuple of Function Objects
    x = []
    for i in f:
        x.append(i.minus())
    return tuple(x)